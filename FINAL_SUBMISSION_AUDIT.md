# Final Submission Audit

Audit Date: 2026-11-02  
Status: `READY AFTER MANUAL ACTIONS` (See [`FINAL_SUBMISSION/FINAL_STATUS_REPORT.md`](./FINAL_SUBMISSION/FINAL_STATUS_REPORT.md))

## Question 1 Deliverables

| Required Deliverable | Path in `FINAL_SUBMISSION/` | Audit Finding |
|---|---|---|
| Main Research / Design Document | `Q1/Q1_Main_Research_Document.pdf` | **Complete**; 10 systems with official URLs, committed zero-collar/overlap policy, Hungarian mapping, 100 hr dataset, device matrix, 10 metrics, paired bootstrap CI. Zero extraction artifacts. |
| One-Page Executive Report | `Q1/Q1_One_Page_Report.pdf` | **Complete**; 1-page executive briefing for leadership with clean layout and zero artifacts. |
| Leaderboard Mockup | `Q1/Q1_Leaderboard_Mockup.png` | **Complete**; 180 DPI high-res graphic showing filter chips, 14-column leaderboard table, and detail drill-down inspection card. |
| Walkthrough Script & Checklist (DOCX) | `Q1/Q1_Walkthrough_Script_and_Checklist.docx` | **Complete**; 2–3 minute script with exact timestamps and visual cue instructions. |
| Walkthrough Script & Checklist (MD) | `Q1/Q1_Walkthrough_Script_and_Checklist.md` | **Complete**; markdown version. |
| Walkthrough Video | `videos/Q1_Walkthrough.mp4` | **Manual Action Required**; script ready, physical recording needed. |

## Question 2 Deliverables

| Required Deliverable | Path in `FINAL_SUBMISSION/` | Audit Finding |
|---|---|---|
| Research Report | `Q2/Samarth_Kapdi_Report.pdf` | **Complete**; 4-page report with 15-row overview table, contrast table, settings re-runs (DER % & Words), tripartite root-cause classification. Zero extraction artifacts. |
| Social Drafts | `Q2/Samarth_Kapdi_Posts.docx` | **Complete**; X thread (5 posts) and LinkedIn post with deliverable links, zero `[link]` placeholders. |
| Proof Folder & Manual Guide | `Q2/Samarth_Kapdi_Proof/MANUAL_EXPERIMENT_EXECUTION_GUIDE.md` | **Complete**; detailed execution guide for the 7 playground runs. |
| Walkthrough Script & Checklist (DOCX) | `Q2/Q2_Walkthrough_Script_and_Checklist.docx` | **Complete**; 2–3 minute script with exact timestamps and visual cue instructions. |
| Walkthrough Script & Checklist (MD) | `Q2/Q2_Walkthrough_Script_and_Checklist.md` | **Complete**; markdown version. |
| Root-Cause Evidence Matrix | `Q2/ROOT_CAUSE_EVIDENCE_MATRIX.md` | **Complete**; tripartite hypothesis classification with confidence scores. |
| Seven Manual Runs | `Supporting_Work/playground_run_log.xlsx` | **Manual Action Required**; targets pre-populated, status strictly `NOT PERFORMED - manual run required`. |
| Walkthrough Video | `videos/Q2_Walkthrough.mp4` | **Manual Action Required**; script ready, physical recording needed. |

## Technical & Numerical Verification

- Independent Python audit confirms mean DER `64.450666...%` and median DER `86.02%`.
- Historical 139-recording benchmark (67.1% DER) rigorously separated from 15-recording sample and from combined track (71.89% cpWER).
- All 8 settings-sheet re-runs verified and transcribed into Tables 1 and 2 in `Samarth_Kapdi_Report.pdf`.
- Two empty Nova-3 RTTM files confirmed: `D20260825_S003_015_5SPK_IN_EN` and `D20260825_S003_012_5SPK_IN_EN`.
- 100% of PDFs verified: valid headers, 0 replacement glyphs (`\ufffd`), clean formatting.
- 100% of DOCX files verified: valid Office XML ZIP containers, zero placeholder strings.
- 100% of PNG images verified: non-empty, high-DPI rendering.
