# Reproducibility README

## Inputs

- `Deepgram_Failure_Analysis_Data.xlsx`
- `Supporting_Work/rttm_source/Deepgram_Failure_RTTM_Files/`

The assessment PDF is not present in the workspace. The RTTM README is retained beside the extracted files and is the authority for the supplied RTTM format and scoring caveat.

## Environment

Python packages used:

- pandas
- numpy
- matplotlib
- openpyxl
- reportlab
- python-docx

## Run the analysis

From the workspace root:

```powershell
python Supporting_Work\analysis\analyze_dataset.py
python Supporting_Work\analysis\independent_quality_audit.py
python Supporting_Work\analysis\generate_deliverables.py
```

The scripts regenerate consolidated tables, selected recordings, RTTM validation, charts, audit summaries and written deliverables. They do not modify the original workbook or source RTTM files.

## Interpretation rules

- The workbook contains 15 recordings.
- The RTTM package contains 20 recording IDs and 60 RTTM files. Five IDs are package-only and are excluded from workbook-level summary statistics.
- The workbook's published Nova-3 DER is used for the 15-recording analysis.
- File-based RTTM parsing validates syntax, positive timing, speaker IDs, pairing and empty outputs. It does not claim exact benchmark DER reproduction because the RTTM README says published scores used an earlier reference build.
- Playground runs and screenshots are manual evidence and remain unperformed until genuine evidence is supplied.
