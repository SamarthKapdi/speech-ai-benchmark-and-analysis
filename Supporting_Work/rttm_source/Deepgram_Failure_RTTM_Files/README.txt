Deepgram Nova-3 failure analysis: RTTM files

One file per recording (20 recordings, same session IDs as the data sheet).

reference/       Human ground truth. Every vocal sound counts, including fillers and laughter.
                 Speaker labels SPK01, SPK02, ... are the people in the recording.
                 BG = a background voice that is not one of the session speakers.
deepgram_nova3/  Nova-3 output as used in the benchmark. Words from the same Deepgram speaker
                 are joined into one segment when the gap between them is under 0.5 s.
                 An empty file means Nova-3 returned no words for that recording.
silero_vad/      Speech regions found by Silero VAD (threshold 0.5, minimum speech 250 ms,
                 minimum silence 100 ms). One label, "speech", because a VAD does not know speakers.

RTTM format: one segment per line.
  SPEAKER <session> 1 <start seconds> <duration seconds> <NA> <NA> <speaker> <NA> <NA>

Scores in the data sheet are the published benchmark scores. If you recompute DER from these
files you may see differences of a point or two, because the published scores used an earlier
build of the reference. Score with no collar and with overlapping speech included to match.

Please use these files only for the assessment and do not share them.
