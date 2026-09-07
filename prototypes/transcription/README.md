# Transcription pipeline prototype (issue #13)

**Throwaway.** Answers one question: what does a real transcript of one multi-candidate
Appearance look like when produced on Patrick's Apple Silicon Mac, and is the quality good
enough to seed community correction? The validated decisions go to the data-model and
Mac-to-repo bridge tickets; this code is not the production pipeline.

Run everything (media file from issue #28, never copied into the repo):

```bash
uv run pipeline.py all
```

Or step by step: `prepare`, `asr`, `diarize` (needs `hf auth login` and the accepted terms of
`pyannote/speaker-diarization-3.1` + `pyannote/segmentation-3.0`), `merge`, `sample`, then
hand-correct `out/sample/reference-text.txt` and fill `out/sample/attribution-check.txt` (the RTTM is optional) and run
`uv run pipeline.py evaluate --ref-corrected`.

Outputs in `out/`: `transcript.json` (first-cut structured output), `transcript.txt`
(readable rendering), `sample/evaluation.json` (WER, DER, overlap, hallucination flags,
wall-clock per audio hour). Intermediate wav files live in `~/fact-checked-politics-media/work/`.
