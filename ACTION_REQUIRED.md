# Action Required Before Final Submission

**Submission Status:** `READY AFTER MANUAL ACTIONS`  
See full audit breakdown in [`FINAL_SUBMISSION/FINAL_STATUS_REPORT.md`](./FINAL_SUBMISSION/FINAL_STATUS_REPORT.md).

All analytical, statistical, graphical, and documentation deliverables are 100% complete, verified, and synchronized in [`FINAL_SUBMISSION/`](./FINAL_SUBMISSION/). In accordance with scientific integrity rules, no live experiment evidence or video media has been fabricated.

The candidate must perform the following manual actions before delivering the package:

---

## 1. Execute Seven Manual Deepgram Playground Runs
Follow the exact protocol in [`FINAL_SUBMISSION/Q2/Samarth_Kapdi_Proof/MANUAL_EXPERIMENT_EXECUTION_GUIDE.md`](./FINAL_SUBMISSION/Q2/Samarth_Kapdi_Proof/MANUAL_EXPERIMENT_EXECUTION_GUIDE.md):
- **5 Baseline Runs:** Model `nova-3`, language `en`, `diarize=true`, `utterances=true` on recordings:
  1. `D20260825_S003_015_5SPK_IN_EN` (worst failure, 0 words in workbook)
  2. `D20260825_S003_014_5SPK_IN_EN` (severe failure 2)
  3. `D20260826_S001_03_4SPK_IN_EN` (severe failure 3)
  4. `D20260825_S004_31_2SPK_IN_EN` (good in-person control)
  5. `O20260826_S010_04_01_4SPK_US_EN` (good online control)
- **2 Alternative Runs on Worst Recording (`D20260825_S003_015_5SPK_IN_EN`):**
  6. Alternative 1: Model `nova-3`, language `multi`
  7. Alternative 2: Model `nova-2`, language `en` (or hosted `whisper-large`)
- **Capture & Log:**
  - Save full-window screenshots and raw response JSON files into `FINAL_SUBMISSION/Q2/Samarth_Kapdi_Proof/evidence/`.
  - In `FINAL_SUBMISSION/Supporting_Work/playground_run_log.xlsx`, enter captured Deepgram Request IDs, UTC timestamps, screenshot file paths, and update status to `COMPLETE`.

---

## 2. Record Two 2–3 Minute Walkthrough Videos
Follow the prepared scripts with visual cues and timing breakdowns:
- **Video 1 (Q1 Benchmark):** Follow [`FINAL_SUBMISSION/Q1/Q1_Walkthrough_Script_and_Checklist.docx`](./FINAL_SUBMISSION/Q1/Q1_Walkthrough_Script_and_Checklist.docx).
  - Screen share: `Q1_One_Page_Report.pdf`, `Q1_Main_Research_Document.pdf`, and `Q1_Leaderboard_Mockup.png`.
- **Video 2 (Q2 Root-Cause Investigation):** Follow [`FINAL_SUBMISSION/Q2/Q2_Walkthrough_Script_and_Checklist.docx`](./FINAL_SUBMISSION/Q2/Q2_Walkthrough_Script_and_Checklist.docx).
  - Screen share: `Samarth_Kapdi_Report.pdf`, `q2_poor_good_evidence.png`, and `ROOT_CAUSE_EVIDENCE_MATRIX.md`.
- Save recorded MP4 files into `FINAL_SUBMISSION/videos/` (or upload to YouTube/Loom and add links in `FINAL_SUBMISSION_CHECKLIST.md`).

---

## 3. Original Assessment PDF (Optional Check)
If the original assessment PDF is available, confirm that candidate naming conventions match instructions.
