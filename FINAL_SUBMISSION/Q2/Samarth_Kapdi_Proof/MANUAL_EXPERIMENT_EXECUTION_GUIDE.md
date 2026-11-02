# Manual Deepgram Playground Experiment Execution Guide

This guide provides exact step-by-step instructions for executing the seven manual Deepgram playground experiments required by the assignment.
**Current Status:** All seven experiments remain `NOT PERFORMED - manual run required`. No experimental evidence is fabricated.

---

## 1. Required Experiments Overview

The assignment requires exactly seven manual playground runs:
- **Five Baseline Runs (Runs 1 to 5):** Model `nova-3`, `diarize=true`, `utterances=true`, default English / auto language.
- **Two Alternative Configuration Runs (Runs 6 & 7):** On the worst-performing recording, test alternate models/languages to isolate the speech omission mechanism.

---

## 2. Detailed Run Specifications

### Run 1: Baseline — Worst Failure Case (0 words in workbook)
- **Recording ID:** `D20260825_S003_015_5SPK_IN_EN`
- **Audio URL:** `https://storage.googleapis.com/delivery_team_data/diarization/platform_test/platform_transcripts_energy_edges_sept5/D20260825_S003_015_5SPK_IN_EN/merged.wav`
- **Configuration to Select:** Model: `Nova-3` (`general-nova-3`), Language: `English` (`en` or default)
- **Settings to Enable:** Diarization: **ON**, Utterances: **ON**, Smart Format: Default, Punctuate: Default
- **Workbook Comparison:** Workbook reports 0 words, 0.0% coverage, 100.0% DER. Nova-3 RTTM is completely empty.

### Run 2: Baseline — Severe Failure Case 2
- **Recording ID:** `D20260825_S003_014_5SPK_IN_EN`
- **Audio URL:** `https://storage.googleapis.com/delivery_team_data/diarization/platform_test/platform_transcripts_energy_edges_sept5/D20260825_S003_014_5SPK_IN_EN/merged.wav`
- **Configuration to Select:** Model: `Nova-3`, Language: `English` (`en`)
- **Settings to Enable:** Diarization: **ON**, Utterances: **ON**
- **Workbook Comparison:** Workbook reports 34 words, 1.7% coverage, 99.14% DER.

### Run 3: Baseline — Severe Failure Case 3
- **Recording ID:** `D20260826_S001_03_4SPK_IN_EN`
- **Audio URL:** `https://storage.googleapis.com/delivery_team_data/diarization/platform_test/platform_transcripts_energy_edges_sept5/D20260826_S001_03_4SPK_IN_EN/merged.wav`
- **Configuration to Select:** Model: `Nova-3`, Language: `English` (`en`)
- **Settings to Enable:** Diarization: **ON**, Utterances: **ON**
- **Workbook Comparison:** Workbook reports 114 words, 5.5% coverage, 98.59% DER.

### Run 4: Baseline — Good In-Person Control
- **Recording ID:** `D20260825_S004_31_2SPK_IN_EN`
- **Audio URL:** `https://storage.googleapis.com/delivery_team_data/diarization/platform_test/platform_transcripts_day3_2person_full_pad30_split_none/D20260825_S004_31_2SPK_IN_EN/merged.wav`
- **Configuration to Select:** Model: `Nova-3`, Language: `English` (`en`)
- **Settings to Enable:** Diarization: **ON**, Utterances: **ON**
- **Workbook Comparison:** Workbook reports 788 words, 97.4% coverage, 15.13% DER.

### Run 5: Baseline — Good Online Control
- **Recording ID:** `O20260826_S010_04_01_4SPK_US_EN`
- **Audio URL:** `https://storage.googleapis.com/delivery_team_data/diarization/platform_test/platform_transcripts_online_pad30_split_none/O20260826_S010_04_01_4SPK_US_EN/merged.wav`
- **Configuration to Select:** Model: `Nova-3`, Language: `English` (`en`)
- **Settings to Enable:** Diarization: **ON**, Utterances: **ON**
- **Workbook Comparison:** Workbook reports 2,453 words, 94.6% coverage, 26.81% DER.

### Run 6: Alternative 1 — Multilingual Nova-3 on Worst Failure
- **Recording ID:** `D20260825_S003_015_5SPK_IN_EN`
- **Audio URL:** Same as Run 1
- **Configuration to Select:** Model: `Nova-3`, Language: `Multilingual` (`multi`)
- **Settings to Enable:** Diarization: **ON**, Utterances: **ON**
- **Workbook Comparison:** Settings sheet reports 465 words returned, 93.06% DER (proves English acoustic pipeline collapse).

### Run 7: Alternative 2 — Alternate Architecture / Nova-2 on Worst Failure
- **Recording ID:** `D20260825_S003_015_5SPK_IN_EN`
- **Audio URL:** Same as Run 1
- **Configuration to Select:** Model: `Nova-2` (`general-nova-2`) or hosted `Whisper-Large`
- **Settings to Enable:** Diarization: **ON**, Utterances: **ON**
- **Workbook Comparison:** Settings sheet reports Nova-2 returns 28 words (98.97% DER), while Whisper-Large returns 1,661 words (64.95% DER).

---

## 3. What to Capture During Execution

For every single run, capture:
1. **Full-Window Screenshot:** Showing audio URL/upload, model dropdown, language setting, diarization toggle, utterances toggle, and the returned response window.
2. **Raw API Response JSON:** Save the complete response JSON including `results.channels[0].alternatives[0].words`, `utterances`, and `metadata`.
3. **Deepgram Request ID:** Copy the `request_id` from the JSON response or UI header (e.g. `metadata.request_id`).
4. **Execution Timestamp:** Record exact UTC date and time of request submission.
5. **Returned Metrics:** Count of words returned, number of unique speaker labels assigned, and total speech timeline duration.

---

## 4. Evidence Storage Structure

Save all captured artifacts into:
```
deliverables/Q2/Samarth_Kapdi_Proof/evidence/
  ├── run1_D20260825_S003_015_baseline.png
  ├── run1_D20260825_S003_015_baseline_response.json
  ├── run2_D20260825_S003_014_baseline.png
  ├── run2_D20260825_S003_014_baseline_response.json
  ├── run3_D20260826_S001_03_baseline.png
  ├── run3_D20260826_S001_03_baseline_response.json
  ├── run4_D20260825_S004_31_baseline.png
  ├── run4_D20260825_S004_31_baseline_response.json
  ├── run5_O20260826_S010_04_baseline.png
  ├── run5_O20260826_S010_04_baseline_response.json
  ├── run6_D20260825_S003_015_alt1_multi.png
  ├── run6_D20260825_S003_015_alt1_multi_response.json
  ├── run7_D20260825_S003_015_alt2_nova2.png
  └── run7_D20260825_S003_015_alt2_nova2_response.json
```

---

## 5. Updating the Run Log

Once genuine runs are executed, open `Supporting_Work/playground_run_log.xlsx` and update:
- `request_id`: Captured Deepgram request ID string.
- `run_datetime`: ISO-8601 timestamp (e.g. `2026-11-02T14:30:00Z`).
- `screenshot_path`: Path to saved PNG.
- `status`: Change from `NOT PERFORMED - manual run required` to `COMPLETE`.
