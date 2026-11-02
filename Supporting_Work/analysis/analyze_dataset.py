from pathlib import Path
import zipfile
import json
import re

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


ROOT = Path(r"D:\AllProjects\Josh Talks assignment")
WORK = ROOT / "Supporting_Work"
DATA = ROOT / "Deepgram_Failure_Analysis_Data.xlsx"
RTTM = WORK / "rttm_source" / "Deepgram_Failure_RTTM_Files"
TABLES = WORK / "tables"
CHARTS = WORK / "charts"
TABLES.mkdir(parents=True, exist_ok=True)
CHARTS.mkdir(parents=True, exist_ok=True)


def read_sheet(sheet: str) -> pd.DataFrame:
    raw = pd.read_excel(DATA, sheet_name=sheet, header=None)
    header_row = next(
        i for i, row in raw.iterrows()
        if row.astype(str).str.strip().eq("Session ID").any()
    )
    frame = raw.iloc[header_row + 1:].copy()
    frame.columns = raw.iloc[header_row].astype(str).str.strip()
    return frame.dropna(how="all").reset_index(drop=True)


def parse_rttm(path: Path) -> dict:
    records = []
    invalid = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        if not line.strip():
            continue
        fields = line.split()
        if len(fields) < 8 or fields[0] != "SPEAKER":
            invalid.append({"line": line_no, "reason": "invalid RTTM line"})
            continue
        try:
            start = float(fields[3])
            duration = float(fields[4])
        except ValueError:
            invalid.append({"line": line_no, "reason": "non-numeric timing"})
            continue
        if start < 0 or duration <= 0:
            invalid.append({"line": line_no, "reason": "non-positive timing"})
            continue
        records.append(
            {
                "start": start,
                "duration": duration,
                "end": start + duration,
                "speaker": fields[7],
            }
        )
    overlaps = 0
    by_speaker = {}
    for record in records:
        by_speaker.setdefault(record["speaker"], []).append(record)
    for speaker_records in by_speaker.values():
        speaker_records.sort(key=lambda x: x["start"])
        overlaps += sum(
            1 for left, right in zip(speaker_records, speaker_records[1:])
            if right["start"] < left["end"]
        )
    return {
        "kind": path.parent.name,
        "recording_id": path.stem,
        "segment_count": len(records),
        "speaker_count": len({r["speaker"] for r in records}),
        "speech_seconds": sum(r["duration"] for r in records),
        "overlap_pairs_same_speaker": overlaps,
        "invalid_lines": len(invalid),
        "empty": len(records) == 0,
    }


def main() -> None:
    sessions = read_sheet("Sessions")
    results = read_sheet("Results")
    audio = read_sheet("Audio quality")
    api = read_sheet("Deepgram API check")
    settings = read_sheet("Deepgram settings")

    for frame in (sessions, results, audio, api, settings):
        frame.columns = [str(c).strip() for c in frame.columns]
    ids = set(sessions["Session ID"].dropna()) | set(results["Session ID"].dropna())
    consolidated = sessions.merge(results, on="Session ID", how="outer", suffixes=("", " (results)"))
    if "Session ID" in audio:
        consolidated = consolidated.merge(audio, on="Session ID", how="left", suffixes=("", " (audio)"))
    if "Session ID" in api:
        consolidated = consolidated.merge(api, on="Session ID", how="left", suffixes=("", " (api)"))
    consolidated.to_csv(TABLES / "consolidated_recordings.csv", index=False)

    # Keep classifications data-led: lower DER is better, with the six worst and
    # three best retained for inspection.
    consolidated["Nova-3 DER %"] = pd.to_numeric(consolidated["Nova-3 DER %"], errors="coerce")
    for column in consolidated.columns:
        if column not in ("Session ID", "Setting", "Accent", "Recording date", "Recording station", "File format", "Model reported", "Diarizer reported", "Warnings", "Audio link"):
            converted = pd.to_numeric(consolidated[column], errors="coerce")
            if converted.notna().sum() >= max(3, len(consolidated) // 2):
                consolidated[column] = converted
    ordered = consolidated.sort_values("Nova-3 DER %", ascending=False)
    selected = pd.concat([ordered.head(6), ordered.tail(3)]).drop_duplicates("Session ID")
    selected.to_csv(TABLES / "selected_recordings.csv", index=False)

    rttm_rows = []
    for kind in ("reference", "deepgram_nova3", "silero_vad"):
        for path in sorted((RTTM / kind).glob("*.rttm")):
            rttm_rows.append(parse_rttm(path))
    rttm = pd.DataFrame(rttm_rows)
    rttm.to_csv(TABLES / "rttm_validation.csv", index=False)

    numeric = consolidated.select_dtypes(include=np.number)
    corr = numeric.corr(numeric_only=True)["Nova-3 DER %"].sort_values(ascending=False)
    corr.rename("pearson_r").to_csv(TABLES / "der_correlations.csv")

    plt.figure(figsize=(10, 6))
    plt.scatter(consolidated["Speech covered by Nova-3 (%)"], consolidated["Nova-3 DER %"])
    for _, row in consolidated.iterrows():
        plt.annotate(str(row["Session ID"])[-8:], (row["Speech covered by Nova-3 (%)"], row["Nova-3 DER %"]), fontsize=7)
    plt.xlabel("Speech covered by Nova-3 (%)")
    plt.ylabel("Nova-3 DER (%)")
    plt.title(f"Nova-3 DER vs speech coverage (n={len(consolidated)})")
    plt.tight_layout()
    plt.savefig(CHARTS / "der_vs_speech_coverage.png", dpi=180)
    plt.close()

    summary = {
        "workbook": str(DATA),
        "sheet_names": pd.ExcelFile(DATA).sheet_names,
        "recording_count": int(len(ids)),
        "rttm_file_count": int(len(rttm)),
        "published_der_mean": float(consolidated["Nova-3 DER %"].mean()),
        "published_der_median": float(consolidated["Nova-3 DER %"].median()),
        "empty_nova_rttm": int(rttm.query("kind == 'deepgram_nova3' and empty").shape[0]),
        "missing_workbook_ids_in_rttm": sorted(ids - set(rttm["recording_id"])),
        "rttm_ids_not_in_workbook": sorted(set(rttm["recording_id"]) - ids),
    }
    (WORK / "analysis_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    print("\nSelected recordings:")
    print(selected[["Session ID", "Nova-3 DER %", "Nova-3 missed speech %", "Nova-3 false alarm %", "Nova-3 speaker confusion %"]].to_string(index=False))


if __name__ == "__main__":
    main()
