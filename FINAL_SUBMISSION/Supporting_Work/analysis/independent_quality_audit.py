from pathlib import Path
import json
import zipfile

import numpy as np
import pandas as pd


ROOT = Path(r"D:\AllProjects\Josh Talks assignment")
DATA = ROOT / "Deepgram_Failure_Analysis_Data.xlsx"
RTTM = ROOT / "Supporting_Work" / "rttm_source" / "Deepgram_Failure_RTTM_Files"
WORK = ROOT / "Supporting_Work"
TABLES = WORK / "tables"
Q2 = ROOT / "deliverables" / "Q2"


def sheet(name):
    raw = pd.read_excel(DATA, sheet_name=name, header=None)
    header = next(i for i, row in raw.iterrows() if row.astype(str).str.strip().eq("Session ID").any())
    frame = raw.iloc[header + 1:].copy()
    frame.columns = raw.iloc[header].astype(str).str.strip()
    return frame.dropna(how="all").reset_index(drop=True)


def parse(path):
    rows = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.strip():
            fields = line.split()
            if len(fields) >= 8 and fields[0] == "SPEAKER":
                rows.append((float(fields[3]), float(fields[4]), fields[7]))
    return rows


def main():
    sessions = sheet("Sessions")
    results = sheet("Results")
    for c in [
        "Nova-3 DER %",
        "Nova-3 missed speech %",
        "Nova-3 false alarm %",
        "Nova-3 speaker confusion %",
        "Speech covered by Nova-3 (%)",
    ]:
        results[c] = pd.to_numeric(results[c], errors="coerce")

    components = results["Nova-3 missed speech %"] + results["Nova-3 false alarm %"] + results["Nova-3 speaker confusion %"]
    results["component_sum"] = components
    results["component_delta"] = results["Nova-3 DER %"] - components
    results[["Session ID", "Nova-3 DER %", "component_sum", "component_delta"]].to_csv(
        TABLES / "independent_component_check.csv", index=False
    )

    workbook_ids = set(results["Session ID"]) | set(sessions["Session ID"])
    rttm_ids = set(p.stem for kind in ("reference", "deepgram_nova3", "silero_vad") for p in (RTTM / kind).glob("*.rttm"))
    nova_empty = sorted(p.stem for p in (RTTM / "deepgram_nova3").glob("*.rttm") if not p.read_text(encoding="utf-8", errors="replace").strip())
    extra_ids = sorted(rttm_ids - workbook_ids)
    worst = results.sort_values("Nova-3 DER %", ascending=False).head(5)

    summary = {
        "recordings": int(len(results)),
        "mean_der": float(results["Nova-3 DER %"].mean()),
        "median_der": float(results["Nova-3 DER %"].median()),
        "worst_five_ids": worst["Session ID"].tolist(),
        "worst_five_der": worst["Nova-3 DER %"].tolist(),
        "worst_five_coverage": worst["Speech covered by Nova-3 (%)"].tolist(),
        "component_delta_max_abs": float(results["component_delta"].abs().max()),
        "component_delta_nonzero_count": int((results["component_delta"].abs() > 0).sum()),
        "empty_nova_rttm": nova_empty,
        "extra_rttm_ids": extra_ids,
        "reference_rttm_count": len(list((RTTM / "reference").glob("*.rttm"))),
        "nova_rttm_count": len(list((RTTM / "deepgram_nova3").glob("*.rttm"))),
        "vad_rttm_count": len(list((RTTM / "silero_vad").glob("*.rttm"))),
    }
    (WORK / "independent_audit_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    checklist = ["# Seven-run playground execution checklist", "", "All rows are intentionally marked `NOT PERFORMED` until genuine output and screenshots are supplied.", ""]
    poor = results.sort_values("Nova-3 DER %", ascending=False).head(3)["Session ID"].tolist()
    good = results.sort_values("Nova-3 DER %", ascending=True).head(2)["Session ID"].tolist()
    run_rows = [(x, "baseline", "nova-3") for x in poor + good] + [
        (poor[0], "alternative 1", "record actual model/language"),
        (poor[0], "alternative 2", "record actual model/language"),
    ]
    session_links = sessions.set_index("Session ID")["Audio link"].to_dict()
    for n, (rid, kind, model) in enumerate(run_rows, 1):
        checklist += [
            f"## Run {n}: {kind}",
            f"- Recording ID: `{rid}`",
            f"- Audio link: {session_links.get(rid, 'not found')}",
            f"- Selected model: `{model}`",
            "- Language: record selected value; do not assume",
            "- Diarization: ON",
            "- Utterances: ON",
            "- Required screenshot: complete configuration, audio/input, output and request ID if displayed",
            "- Output comparison: compare returned words, speaker labels, timestamps and coverage against the workbook/RTTM evidence",
            "- Request ID: not captured",
            "- Completion status: **NOT PERFORMED**",
            "",
        ]
    (Q2 / "Samarth_Kapdi_Proof" / "SEVEN_RUN_CHECKLIST.md").write_text("\n".join(checklist), encoding="utf-8")

    matrix = """# Root-cause evidence matrix

| Hypothesis | Evidence supporting | Evidence against | Validation performed | Current conclusion | Confidence |
|---|---|---|---|---|---|
| Nova-3 omits speech/output | Five worst rows have 0–9.8% coverage; two Nova-3 RTTMs are empty; missed speech is 93.75–100.00% in four of the five worst rows | Supplied files do not expose the original API response for every row | Workbook word counts, coverage, RTTM emptiness and API-check fields audited | Strongly supported for this sample; mechanism not yet isolated | High |
| Speaker assignment is the primary failure | Some rows have fewer speakers found than reference | Severe rows are already dominated by missed speech, not confusion; D20260825_S003_015 has no output | Compared speakers found and confusion components | Not primary explanation for the worst failures | High |
| Word-to-RTTM conversion loses timeline content | Nova RTTM contains very few segments/seconds in several severe rows; README documents a word-joining conversion rule | No raw word JSON or converter source supplied | Segment counts, durations, speaker IDs and empty files audited | Plausible and strongly coupled to output omission; not proven independently | Medium |
| Human reference is wrong | Published scores can differ because an earlier reference build was used | Reference files are parseable, paired for all workbook IDs, and contain valid positive timings | RTTM syntax, IDs and timing validity checked | Version mismatch is a limitation, not evidence that the supplied reference is erroneous | Low |
| Silero VAD removes the speech | VAD coverage is lower than reference for some rows | VAD coverage remains high (for example 95.5% and 99%) in severe rows; Nova-specific output is much lower | Compared workbook VAD coverage with Nova coverage | Not supported as the primary explanation by supplied evidence | Low |
| Audio channel/format issue | Severe rows include station/date clusters and audio-quality variation | All audited API rows report mono WAV/16 kHz where available; several comparable files perform well | Checked format, channels, lengths and reported lengths | Plausible station/input interaction; not ruled out | Low |
| Language/accent configuration | Worst rows are Indian English in-person sessions | Many Indian-English rows perform materially better; online Vietnamese-accented English is not a failure | Compared setting/accent groups descriptively | Accent alone is not supported; configuration interaction remains untested | Low |
| API warning/configuration problem | Configuration is an obvious failure surface | Workbook warnings are `none` in inspected rows and model/diarizer fields are consistent where present | Audited API check and settings sheets | No supplied evidence of a warning/config mismatch; raw replay required | Medium-low |
| Evaluation settings/overlap treatment | Reference contains overlaps and benchmark scores use overlap-inclusive, no-collar settings | Cannot reproduce the earlier reference build exactly; component deltas are rounding-scale | README and workbook definitions reviewed; file pairing checked | Exact benchmark reproduction is not established | High |
"""
    (Q2 / "ROOT_CAUSE_EVIDENCE_MATRIX.md").write_text(matrix, encoding="utf-8")

    action = """# ACTION_REQUIRED

This submission is **not fully complete**. The following items remain:

1. Provide the missing assessment PDF and verify the final checklist against its exact wording.
2. Execute the five baseline playground runs and two alternative-setting runs in [SEVEN_RUN_CHECKLIST.md](./Q2/Samarth_Kapdi_Proof/SEVEN_RUN_CHECKLIST.md).
3. Capture genuine screenshots, outputs, request IDs (if available), timestamps and configuration details for all seven runs.
4. Replace the placeholder run-log rows in `Supporting_Work/playground_run_log.xlsx` with the captured evidence.
5. Record the exact Voice Arena leaderboard values, position, access date and URL if the live page is available; do not infer them from the 15-recording sample.
6. If exact benchmark reproduction is required, obtain the benchmark's earlier reference build or document why it cannot be reproduced. The supplied README makes exact equality impossible from the current files alone.
7. Record the required 2–3 minute videos; scripts are prepared, but video files are not present.

Completed and independently audited: workbook metrics, sample mean/median, worst recordings, speech coverage, component rounding, RTTM pairing/emptiness, extra RTTM IDs, file validity, Q1/Q2 written deliverables and social-post consistency.
"""
    (ROOT / "ACTION_REQUIRED.md").write_text(action, encoding="utf-8")

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
