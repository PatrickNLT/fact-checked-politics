"""PROTOTYPE: disagreement between two ASR models on the sample window, as a WER *proxy*
(lower bound on the true error: both models share Whisper's training and blind spots)."""
import json, sys
import jiwer
from pipeline import _norm
start, length = 7600.0, 300.0
def text(path):
    d = json.load(open(path))
    return _norm(" ".join(s["text"] for s in d["segments"] if s["end"] > start and s["start"] < start + length))
a, b = text("out/asr.json"), text("out/turbo/asr-clip-7600.json")
m = jiwer.process_words(a, b)
print(json.dumps({"ref_model": "large-v3 (full run)", "hyp_model": "large-v3-turbo (clip)", "ref_words": len(a.split()),
                  "hyp_words": len(b.split()), "wer": round(m.wer, 4), "sub": m.substitutions, "del": m.deletions,
                  "ins": m.insertions}, indent=1))
print(jiwer.visualize_alignment(m, show_measures=False)[:3000])
