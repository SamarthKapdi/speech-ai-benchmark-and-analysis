# Question 2 - 2-3 Minute Walkthrough Video Script & Checklist
## Recording Objective & Technical Setup
Video Duration: 2 to 3 minutes (120 to 180 seconds target).
Screen Recording: 1080p full-screen capture showing deliverables/Q2/Samarth_Kapdi_Report.pdf and Supporting_Work/charts/q2_poor_good_evidence.png.
Audio Setup: Quiet room, external microphone, professional presentation tone.
Pre-recording Checklist: Open Samarth_Kapdi_Report.pdf to Section 1 (Executive Summary), Section 4 (Overview Table), Section 5 (Poor vs Good Chart), and Section 6 (Settings Re-Runs).

## 0:00 - 0:35: Scope Clarification & Metric Hygiene
Show on Screen: Samarth_Kapdi_Report.pdf (Section 1: Executive Summary & Section 2: Dated Leaderboard Note).
Talking Points: Begin with strict scope hygiene: the assessment's historical 139-recording benchmark reports 67.1% DER. We audited a separate 15-recording workbook sample that yields mean DER 64.45% and median DER 86.02%. Never confuse these scopes. Clarify that Voice Arena separately reports 71.89% cpWER for Nova-3 on a combined diarization+ASR track; DER and cpWER are distinct metrics and must never be combined.

## 0:35 - 1:15: Severe Output Under-Coverage & Poor vs Good Contrast
Show on Screen: q2_poor_good_evidence.png and Table 5 in Samarth_Kapdi_Report.pdf.
Talking Points: Present the empirical core: five severe failures suffered 97-100% DER with catastrophic speech coverage of 0.0% to 9.8%, dominated by missed speech. Name the two empty Nova-3 RTTMs: D20260825_S003_015 (workbook) and S003_012 (package-only). Contrast this against good rows: an in-person 2-speaker session scored 15.13% DER with 97.4% coverage, and an online meeting scored 26.81% DER. Point out that Silero VAD achieved >91% coverage across all rows, proving acoustic speech energy was present.

## 1:15 - 1:55: Deepgram Settings Sheet Diagnostic Re-Runs
Show on Screen: Samarth_Kapdi_Report.pdf (Section 6: Tables 1 & 2).
Talking Points: Walk through the workbook's 8 recording re-runs across 9 settings. Show that Nova-3 with language=en, en-IN, en-US, and auto-detect fails identically (0 words on S003_015). But switching to language=multi recovers 465 words, and Whisper-large recovers 1,661 words. Mention that non-acoustic parameters changed DER by <=2 points. Explain that these workbook re-runs differ from the 7 manual playground runs, which require live execution.

## 1:55 - 2:30: Root-Cause Synthesis & Proof Gate
Show on Screen: ROOT_CAUSE_EVIDENCE_MATRIX.md and Section 7 of Samarth_Kapdi_Report.pdf.
Talking Points: Present the tripartite root-cause synthesis: established facts vs inferred speech omission vs unresolved converter loss. Discuss the conditional diagnostic check for diarize_model=latest and metadata.diarize_info. Note that exact benchmark reproduction is impossible because the benchmark author used an earlier reference build. Confirm that all 7 manual runs are preserved as NOT PERFORMED without fabrication.

## 2:30 - 3:00: Engineering Recommendations & Conclusion
Show on Screen: Samarth_Kapdi_Report.pdf (Section 9: Recommendations).
Talking Points: Summarize actionable recommendations for Deepgram (zero-output diagnostic alert, raw JSON retention, multi-talker table acoustic tuning) and Voice Arena (audio hashes, reference builds, coverage reporting). Close on the importance of evidence-backed, reproducible benchmarking.

