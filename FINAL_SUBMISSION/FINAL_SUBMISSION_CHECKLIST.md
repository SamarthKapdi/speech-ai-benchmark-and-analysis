# Final Submission Checklist

Audit Date: 2026-11-02

## Evidence Status

No new Deepgram playground screenshots, raw API JSON outputs, request IDs, or completed live run metadata were found in the workspace.
To strictly prevent scientific fabrication:
- All seven rows in `Supporting_Work/playground_run_log.xlsx` remain explicitly marked `NOT PERFORMED - manual run required`.
- A comprehensive execution protocol is provided in `Q2/Samarth_Kapdi_Proof/MANUAL_EXPERIMENT_EXECUTION_GUIDE.md`.
- No experimental findings or mock screenshots are fabricated.

## Included in `FINAL_SUBMISSION/`

| Requirement | Path in `FINAL_SUBMISSION/` | Status |
|---|---|---|
| Q1 Main Research Document | `Q1/Q1_Main_Research_Document.pdf` | Complete; 10 systems, committed zero-collar/overlap policy, 100 hr dataset, device matrix, 10 metrics, paired bootstrap CI |
| Q1 One-Page Executive Report | `Q1/Q1_One_Page_Report.pdf` | Complete; 1-page executive briefing for leadership |
| Q1 Leaderboard Mockup | `Q1/Q1_Leaderboard_Mockup.png` | Complete; high-res 180 DPI graphic with filters, 14-column table, and detail drill-down card |
| Q1 Walkthrough Script & Checklist (DOCX) | `Q1/Q1_Walkthrough_Script_and_Checklist.docx` | Complete; 2-3 minute script with exact timestamps and visual cue instructions |
| Q1 Walkthrough Script & Checklist (MD) | `Q1/Q1_Walkthrough_Script_and_Checklist.md` | Complete; markdown version of video walkthrough script |
| Q1 Video Script | `Q1/Q1_Video_Script.md` | Complete; synchronized with walkthrough script |
| Q2 Research Report | `Q2/Samarth_Kapdi_Report.pdf` | Complete; 4-page publication-grade report with 15-row overview, contrast table, and settings sheet re-runs |
| Q2 Social Drafts | `Q2/Samarth_Kapdi_Posts.docx` | Complete; X thread (5 posts) & LinkedIn post with deliverable links, zero placeholder strings |
| Q2 Walkthrough Script & Checklist (DOCX) | `Q2/Q2_Walkthrough_Script_and_Checklist.docx` | Complete; 2-3 minute script with exact timestamps and visual cue instructions |
| Q2 Walkthrough Script & Checklist (MD) | `Q2/Q2_Walkthrough_Script_and_Checklist.md` | Complete; markdown version of video walkthrough script |
| Q2 Video Script | `Q2/Q2_Video_Script.md` | Complete; synchronized with walkthrough script |
| Q2 Root-Cause Evidence Matrix | `Q2/ROOT_CAUSE_EVIDENCE_MATRIX.md` | Complete; tripartite hypothesis classification with confidence scores |
| Q2 Manual Experiment Execution Guide | `Q2/Samarth_Kapdi_Proof/MANUAL_EXPERIMENT_EXECUTION_GUIDE.md` | Complete; step-by-step protocol for 7 manual playground runs |
| Q2 Seven-Run Checklist | `Q2/Samarth_Kapdi_Proof/SEVEN_RUN_CHECKLIST.md` | Complete; all 7 rows marked NOT PERFORMED |
| Q2 Contrast Evidence Chart | `Supporting_Work/charts/q2_poor_good_evidence.png` | Complete; verified against workbook values |
| Q2 Coverage Scatter Chart | `Supporting_Work/charts/der_vs_speech_coverage.png` | Complete; DER vs speech coverage correlation |
| Workspace Technical Audit | `Workspace_Audit.pdf` | Complete; independent audit of all data sources and file pairings |
| Correction Log | `CORRECTION_LOG.md` | Complete; 25 audited corrections and technical enhancements |
| Reproducibility Instructions | `Supporting_Work/reproducibility_README.md` | Complete; CLI execution instructions for Python pipelines |
| Pre-populated Playground Run Log | `Supporting_Work/playground_run_log.xlsx` | Complete; pre-populated targets, status NOT PERFORMED |
| Consolidated Datasets & Tables | `Supporting_Work/tables/` | Complete; 6 consolidated and validation CSV tables |
| Reusable Analysis Pipeline | `Supporting_Work/analysis/` | Complete; 3 Python analysis and deliverable scripts |

## Audited & Mathematically Verified

- Workbook contains 7 sheets and 15 analyzed conversational sessions.
- Independent Python audit confirms mean DER `64.450666...%`, median DER `86.02%`.
- Five worst recordings and their `0.0% to 9.8%` Nova-3 speech coverage range confirmed.
- Two empty Nova-3 RTTM files confirmed: `D20260825_S003_015_5SPK_IN_EN` (in workbook) and `D20260825_S003_012_5SPK_IN_EN` (in RTTM package, outside workbook).
- DER component sum identity (`DER = Miss % + FA % + Conf %`) verified within 0.01% rounding across all 15 rows.
- All PDF files verified: valid headers, non-zero sizes, clean ASCII typography, 0 replacement glyphs (`\ufffd`), professional table styling.
- All DOCX files verified: valid Office XML ZIP containers, zero placeholder strings (`[link]`, `TODO`, `TBD`, `canvas`).
- All PNG images verified: valid headers, non-empty, high-DPI rendering.

## Remaining Manual Actions Before Final Submission

1. **Seven Manual Playground Runs:**
   - Execute the 5 baseline and 2 alternative Deepgram playground runs following `Q2/Samarth_Kapdi_Proof/MANUAL_EXPERIMENT_EXECUTION_GUIDE.md`.
   - Capture screenshots and raw JSON responses into `deliverables/Q2/Samarth_Kapdi_Proof/evidence/`.
   - Update `Supporting_Work/playground_run_log.xlsx` with captured Request IDs, timestamps, and mark status `COMPLETE`.
2. **Two Walkthrough Videos:**
   - Record the two 2-3 minute walkthrough videos following `Q1/Q1_Walkthrough_Script_and_Checklist.docx` and `Q2/Q2_Walkthrough_Script_and_Checklist.docx`.
   - Save video MP4 files into `FINAL_SUBMISSION/videos/` (or upload to YouTube/Loom and add links).
3. **Assessment PDF Requirement:**
   - If available, verify final deliverables against the original assignment specification PDF.
