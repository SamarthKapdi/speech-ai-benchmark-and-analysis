# Question 1 - 2-3 Minute Walkthrough Video Script & Checklist
## Recording Objective & Technical Setup
Video Duration: 2 to 3 minutes (120 to 180 seconds target).
Screen Recording: 1080p full-screen capture showing deliverables/Q1/Q1_Main_Research_Document.pdf and Q1_Leaderboard_Mockup.png.
Audio Setup: Quiet environment, external microphone, clear delivery.
Pre-recording Checklist: Open Q1 Main Research PDF to Section 2 (System Table) and Section 4 (Primary Policy); open Q1_Leaderboard_Mockup.png in high-res viewer.

## 0:00 - 0:30: Introduction & Strategic Purpose
Show on Screen: Q1_One_Page_Report.pdf (Executive Briefing).
Talking Points: Introduce the core objective: designing a rigorous, fair, multi-dimensional speaker diarization benchmark for conversational Indian audio. Emphasize that single aggregate scores fail enterprise buyers because meeting intelligence, contact center QA, and speech tech vendors face different trade-offs across overlap, hardware, latency, and cost.

## 0:30 - 1:10: Evaluation Shortlist & Committed Primary Scoring Policy
Show on Screen: Q1_Main_Research_Document.pdf (Section 2: 10 Systems Table & Section 4: Primary Policy).
Talking Points: Walk through the 10 representative systems across self-hosted neural diarizers (pyannote 3.1, NVIDIA NeMo) and leading commercial APIs (Deepgram, AssemblyAI, Google Cloud, Azure Speech, AWS Transcribe, Speechmatics, Gladia, ElevenLabs). Clarify that AWS 'speaker labels' is evaluated strictly as diarization clustering, not biometric recognition. Commit unambiguously to the primary scoring policy: zero-collar (0.0s), overlap included, Hungarian optimal mapping per session, and unconstrained/autonomous speaker counting.

## 1:10 - 1:50: Stratified 100-Hour Indian Corpus & Hardware Cross-Tabulation
Show on Screen: Q1_Main_Research_Document.pdf (Section 6: Corpus Matrix & Section 7: Device Matrix).
Talking Points: Explain the exact 100.0-hour allocation across 4 strata: 40 hrs Indian English, 25 hrs Hindi/Hinglish, 20 hrs Regional code-switching (Tamil, Telugu, Marathi, Bengali), and 15 hrs stress cases. Highlight the hardware cross-tabulation table cross-referencing smartphone tabletop mics, laptop array mics, conference room boundary mics, and wearables.

## 1:50 - 2:30: Public Leaderboard Walkthrough & Detail Inspection
Show on Screen: Q1_Leaderboard_Mockup.png.
Talking Points: Walk through the interactive mockup: filter controls (accent, speakers, setting, overlap), the 14-column leaderboard table showing DER with 95% bootstrap confidence intervals, JER, Miss %, FA %, Conf %, Overlap DER, Speaker Count Error, RTF, Latency, Cost/hr, and Failure Rate. Point to the model drill-down card showing granular SNR and condition curves.

## 2:30 - 3:00: Statistical Uncertainty, QA & Strategic Reflection
Show on Screen: Q1_Main_Research_Document.pdf (Section 9: Annotation QA & Section 10: Bootstrap).
Talking Points: Summarize the two-stage annotation adjudication QA and paired stratified bootstrap confidence intervals (B=2,000). Conclude with the core takeaway: zero-collar overlap-inclusive evaluation is tough but essential for conversational Indian speech, turning reproducibility into a product feature.

