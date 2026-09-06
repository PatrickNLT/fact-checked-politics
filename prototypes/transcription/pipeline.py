#!/usr/bin/env python3
"""PROTOTYPE (issue #13): throwaway local transcription pipeline for one Appearance.

Answers: what does a real transcript of the MEDEF debate look like when produced on
Patrick's Apple Silicon Mac, and is the quality good enough to seed community correction?

Not production code. No tests, no error handling beyond what makes it run.

Steps (each a subcommand, each writes into --out):
  prepare   m4a -> 16 kHz mono wav in a work dir, sha256 of the source, provenance stub
  asr       mlx-whisper (Whisper large-v3 on MLX), French, word timestamps -> asr.json
  diarize   pyannote speaker-diarization-3.1 -> diarization.json (needs a Hugging Face token)
  merge     words x speaker turns -> transcript.json (the first-cut structured output)
  sample    cut a 5-minute window, write reference files to hand-correct
  evaluate  WER / DER / hallucination flags of the sample against the corrected references
  all       prepare asr diarize merge sample

Run:  uv run pipeline.py all --media ~/fact-checked-politics-media/rpURHoN54bQ.m4a
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_OUT = HERE / "out"
WORK = Path(os.environ.get("FCP_WORK", Path.home() / "fact-checked-politics-media" / "work"))

APPEARANCE = {
    "catalogue_row": "D1",
    "title": "Débat MEDEF (REF 2026) des candidats à la présidentielle 2027",
    "date": "2026-08-27",
    "source": "LCI (TF1 group)",
    "official_replay": "https://www.youtube.com/watch?v=rpURHoN54bQ",
    "participants": [
        "Gabriel Attal", "Raphaël Glucksmann", "Marine Le Pen", "Jean-Luc Mélenchon",
        "Édouard Philippe", "Bruno Retailleau", "Marine Tondelier",
    ],
    "presenter": "Amélie Carrouër",
    "acquisition_basis": "tolerated",
}

# From issue #28 / the download log alongside the media file.
PROVENANCE = {
    "fetch_date": "2026-09-06",
    "fetch_method": "yt-dlp 2026.08.19, logged out, no account, format 140 (AAC-LC 128 kbit/s m4a), audio only",
    "media_sha256": None,  # filled by `prepare`
    "media_bytes": None,
    "deletion_date": "held, prototype stage (ADR 0003 amendment of 2026-09-06)",
}

ASR_MODEL = "mlx-community/whisper-large-v3-mlx"
DIAR_MODEL = "pyannote/speaker-diarization-3.1"


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256(path, chunk=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while b := f.read(chunk):
            h.update(b)
    return h.hexdigest()


def dump(obj, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=1))
    print(f"wrote {path} ({path.stat().st_size // 1024} KiB)")


def load(path):
    return json.loads(Path(path).read_text())


def fmt_ts(s):
    h, rem = divmod(s, 3600)
    m, s = divmod(rem, 60)
    return f"{int(h):02d}:{int(m):02d}:{s:06.3f}"


# ---------------------------------------------------------------- prepare

def cmd_prepare(a):
    WORK.mkdir(parents=True, exist_ok=True)
    wav = WORK / (Path(a.media).stem + ".16k.wav")
    t0 = time.time()
    if not wav.exists():
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a.media, "-ac", "1", "-ar", "16000",
                        "-c:a", "pcm_s16le", str(wav)], check=True)
    prov = dict(PROVENANCE)
    prov["media_sha256"] = sha256(a.media)
    prov["media_bytes"] = os.path.getsize(a.media)
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                         "-of", "csv=p=0", str(wav)]).strip())
    dump({"appearance": APPEARANCE, "provenance": prov, "wav": str(wav), "duration_s": dur,
          "prepare_wall_s": round(time.time() - t0, 1), "prepared_at": now()}, a.out / "prepare.json")


# ---------------------------------------------------------------- asr

def cmd_asr(a):
    import mlx_whisper
    prep = load(a.out / "prepare.json")
    audio = prep["wav"]
    if a.clip:
        start, length = a.clip
        clip = WORK / f"clip-{int(start)}-{int(length)}.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(start), "-t", str(length), "-i", audio,
                        "-c", "copy", str(clip)], check=True)
        audio = str(clip)
    t0 = time.time()
    res = mlx_whisper.transcribe(
        audio,
        path_or_hf_repo=a.model,
        language="fr",
        task="transcribe",
        word_timestamps=True,
        condition_on_previous_text=False,  # the classic hallucination amplifier; off on purpose
        verbose=False,
        initial_prompt="Débat entre candidats à l'élection présidentielle de 2027, organisé par le MEDEF, diffusé sur LCI.",
    )
    wall = time.time() - t0
    offset = a.clip[0] if a.clip else 0.0
    segs = []
    for s in res["segments"]:
        segs.append({
            "id": s["id"],
            "start": round(s["start"] + offset, 3), "end": round(s["end"] + offset, 3),
            "text": s["text"].strip(),
            "avg_logprob": round(s.get("avg_logprob", 0), 3),
            "no_speech_prob": round(s.get("no_speech_prob", 0), 3),
            "compression_ratio": round(s.get("compression_ratio", 0), 3),
            "words": [{"w": w["word"].strip(), "s": round(w["start"] + offset, 3),
                       "e": round(w["end"] + offset, 3), "p": round(w.get("probability", 0), 3)}
                      for w in s.get("words", [])],
        })
    audio_s = (a.clip[1] if a.clip else prep["duration_s"])
    dump({"model": a.model, "language": res.get("language"), "audio_s": audio_s,
          "wall_s": round(wall, 1), "wall_per_audio_hour_s": round(wall / audio_s * 3600, 1),
          "run_at": now(), "clip": a.clip, "segments": segs},
         a.out / ("asr.json" if not a.clip else f"asr-clip-{int(a.clip[0])}.json"))
    print(f"ASR: {audio_s / 60:.1f} min of audio in {wall / 60:.1f} min wall "
          f"({wall / audio_s * 3600 / 60:.1f} min per audio hour)")


# ---------------------------------------------------------------- patch

def cmd_patch(a):
    """Whisper drops whole 30 s windows now and then (found twice in the MEDEF run, both full of
    speech). Re-transcribe every gap > 3 s in isolation and splice the result in."""
    import mlx_whisper
    prep = load(a.out / "prepare.json")
    asr = load(a.out / "asr.json")
    segs = asr["segments"]
    gaps = [(x["end"], y["start"]) for x, y in zip(segs, segs[1:]) if y["start"] - x["end"] > 3]
    t0 = time.time()
    added, log = [], []
    for g0, g1 in gaps:
        start, length = max(0.0, g0 - 1.0), (g1 - g0) + 2.0
        clip = WORK / "patch.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(start), "-t", str(length), "-i", prep["wav"],
                        "-c", "copy", str(clip)], check=True)
        res = mlx_whisper.transcribe(str(clip), path_or_hf_repo=a.model, language="fr", word_timestamps=True,
                                     condition_on_previous_text=False, verbose=False)
        new = []
        for s in res["segments"]:
            mid = start + (s["start"] + s["end"]) / 2
            if not (g0 <= mid <= g1) or not s["text"].strip():
                continue
            new.append({"id": None, "start": round(start + s["start"], 3), "end": round(start + s["end"], 3),
                        "text": s["text"].strip(), "avg_logprob": round(s.get("avg_logprob", 0), 3),
                        "no_speech_prob": round(s.get("no_speech_prob", 0), 3),
                        "compression_ratio": round(s.get("compression_ratio", 0), 3), "patched": True,
                        "words": [{"w": w["word"].strip(), "s": round(start + w["start"], 3),
                                   "e": round(start + w["end"], 3), "p": round(w.get("probability", 0), 3)}
                                  for w in s.get("words", [])]})
        log.append({"gap": [g0, g1], "seconds": round(g1 - g0, 1), "segments_added": len(new),
                    "words_added": sum(len(s["words"]) for s in new)})
        added += new
    segs = sorted(segs + added, key=lambda s: s["start"])
    for i, s in enumerate(segs):
        s["id"] = i
    asr["segments"] = segs
    asr["patch"] = {"gaps": log, "wall_s": round(time.time() - t0, 1), "run_at": now(),
                    "words_added": sum(l["words_added"] for l in log)}
    dump(asr, a.out / "asr.json")
    print(f"patch: {len(gaps)} gaps, {len(added)} segments / {asr['patch']['words_added']} words added "
          f"in {asr['patch']['wall_s']} s")
    for l in log:
        print(f"  {fmt_ts(l['gap'][0])} +{l['seconds']}s -> {l['words_added']} words")


# ---------------------------------------------------------------- diarize

def cmd_diarize(a):
    import torch
    from pyannote.audio import Pipeline
    prep = load(a.out / "prepare.json")
    token = os.environ.get("HF_TOKEN") or _hf_cached_token()
    if not token:
        sys.exit("diarize: no Hugging Face token (env HF_TOKEN or `hf auth login`); "
                 "accept the terms of pyannote/speaker-diarization-3.1 and pyannote/segmentation-3.0 first")
    t0 = time.time()
    pipe = Pipeline.from_pretrained(a.model, token=token)
    device = "mps" if torch.backends.mps.is_available() and not a.cpu else "cpu"
    pipe.to(torch.device(device))
    load_s = time.time() - t0
    t0 = time.time()
    kw = {}
    if a.speakers:
        kw["num_speakers"] = a.speakers
    out = pipe(prep["wav"], **kw)
    ann = out.speaker_diarization if hasattr(out, "speaker_diarization") else out  # pyannote 4 vs 3 API
    wall = time.time() - t0
    turns = [{"start": round(t.start, 3), "end": round(t.end, 3), "speaker": spk}
             for t, _, spk in ann.itertracks(yield_label=True)]
    dump({"model": a.model, "device": device, "audio_s": prep["duration_s"], "load_s": round(load_s, 1),
          "wall_s": round(wall, 1), "wall_per_audio_hour_s": round(wall / prep["duration_s"] * 3600, 1),
          "num_speakers_hint": a.speakers, "speakers": sorted({t["speaker"] for t in turns}),
          "run_at": now(), "turns": turns}, a.out / "diarization.json")
    print(f"diarization: {len(turns)} turns, {len({t['speaker'] for t in turns})} speakers, "
          f"{wall / 60:.1f} min wall on {device}")


def _hf_cached_token():
    for p in (Path.home() / ".cache/huggingface/token", Path.home() / ".huggingface/token"):
        if p.exists():
            return p.read_text().strip()
    return None


# ---------------------------------------------------------------- merge

def cmd_merge(a):
    prep = load(a.out / "prepare.json")
    asr = load(a.out / "asr.json")
    diar = load(a.out / "diarization.json") if (a.out / "diarization.json").exists() else None
    turns = diar["turns"] if diar else []

    def speakers_at(s, e):
        """All diarization speakers overlapping [s, e], with overlap length."""
        hits = {}
        for t in turns:
            ov = min(e, t["end"]) - max(s, t["start"])
            if ov > 0:
                hits[t["speaker"]] = hits.get(t["speaker"], 0) + ov
        return hits

    # 1. label every word with the speaker owning most of its span; note overlap.
    words = []
    for seg in asr["segments"]:
        for w in seg["words"]:
            hits = speakers_at(w["s"], w["e"]) if turns else {}
            spk = max(hits, key=hits.get) if hits else None
            words.append({**w, "speaker": spk, "overlap": len(hits) > 1, "seg": seg["id"]})

    # 2. group consecutive words into Segments: a new one on speaker change, on an ASR segment
    #    boundary that ends a sentence, or after a gap > 1.5 s.
    segments, cur = [], None
    for w in words:
        new = (cur is None or w["speaker"] != cur["speaker"] or w["s"] - cur["end"] > 1.5
               or (w["seg"] != cur["_seg"] and cur["text"].rstrip()[-1:] in ".?!"))
        if new:
            cur = {"speaker": w["speaker"], "start": w["s"], "end": w["e"], "text": "", "words": [],
                   "overlap_words": 0, "_seg": w["seg"]}
            segments.append(cur)
        cur["end"] = w["e"]
        # Whisper tokens were stripped of their leading space in `asr`; re-join elisions and
        # punctuation without one (l' + État, 20 + %, mot + ,).
        glue = "" if (w["w"][:1] in "'’,.?!;:%)»" or cur["text"][-1:] in "'’(«") else " "
        cur["text"] = (cur["text"] + glue + w["w"]).strip()
        cur["words"].append({k: w[k] for k in ("w", "s", "e", "p")})
        cur["overlap_words"] += int(w["overlap"])
        cur["_seg"] = w["seg"]
    for i, s in enumerate(segments):
        s.pop("_seg")
        s["id"] = i
        s["validation"] = {"text": "draft", "speaker": "draft"}

    speakers = sorted({s["speaker"] for s in segments if s["speaker"]})
    out = {
        "schema": "fcp-transcript-prototype/0",
        "appearance": prep["appearance"],
        "provenance": prep["provenance"],
        "pipeline": {
            "asr": {"model": asr["model"], "wall_s": asr["wall_s"], "run_at": asr["run_at"]},
            "diarization": ({"model": diar["model"], "wall_s": diar["wall_s"], "run_at": diar["run_at"],
                             "num_speakers_hint": diar.get("num_speakers_hint")} if diar else None),
            "merge_run_at": now(),
        },
        # Speaker labels are diarization clusters; mapping to a Participant is a human step.
        "speakers": {spk: {"participant": None} for spk in speakers},
        "segments": segments,
    }
    dump(out, a.out / "transcript.json")
    # Human-readable rendering next to it.
    lines = []
    for s in segments:
        flag = " [chevauchement]" if s["overlap_words"] else ""
        lines.append(f"[{fmt_ts(s['start'])}] {s['speaker'] or '?'}{flag}: {s['text']}")
    (a.out / "transcript.txt").write_text("\n".join(lines))
    print(f"merge: {len(segments)} segments, {len(words)} words, {len(speakers)} speakers, "
          f"{sum(s['overlap_words'] for s in segments)} words in overlap")


# ---------------------------------------------------------------- sample

def cmd_sample(a):
    """Cut the 5-minute evaluation window and write files for hand correction."""
    prep = load(a.out / "prepare.json")
    start, length = a.window
    end = start + length
    sd = a.out / "sample"
    sd.mkdir(parents=True, exist_ok=True)
    # audio of the window, for the human corrector (stays out of git)
    clip = WORK / f"sample-{int(start)}-{int(length)}.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(start), "-t", str(length), "-i", prep["wav"],
                    "-c", "copy", str(clip)], check=True)
    asr = load(a.out / "asr.json")
    segs = [s for s in asr["segments"] if s["end"] > start and s["start"] < end]
    hyp = "\n".join(f"[{fmt_ts(s['start'])}] {s['text']}" for s in segs)
    (sd / "asr-hypothesis.txt").write_text(hyp)
    ref = sd / "reference-text.txt"
    if not ref.exists():
        ref.write_text("# Corrige ce texte à l'oreille (clip : %s). Garde une ligne par segment,\n"
                       "# supprime les timestamps si tu veux, ils sont ignorés. Marque les mots\n"
                       "# inaudibles [inaudible]. Les lignes commençant par # sont ignorées.\n%s\n" % (clip, hyp))
    if (a.out / "diarization.json").exists():
        turns = [t for t in load(a.out / "diarization.json")["turns"] if t["end"] > start and t["start"] < end]
        rttm = "".join(f"SPEAKER sample 1 {max(t['start'], start) - start:.3f} "
                       f"{min(t['end'], end) - max(t['start'], start):.3f} <NA> <NA> {t['speaker']} <NA> <NA>\n"
                       for t in turns)
        (sd / "diarization-hypothesis.rttm").write_text(rttm)
        rref = sd / "reference-speakers.rttm"
        if not rref.exists():
            rref.write_text("# Corrige à l'oreille : un tour par ligne, temps relatifs au début du clip.\n"
                            "# Remplace SPEAKER_xx par le nom du locuteur. Les tours qui se chevauchent\n"
                            "# sont attendus (deux lignes qui se recouvrent).\n" + rttm)
    dump({"window": [start, length], "clip": str(clip), "asr_segments": len(segs)}, sd / "sample.json")
    print(f"sample: window {fmt_ts(start)} +{length}s, {len(segs)} ASR segments; correct {ref}")


# ---------------------------------------------------------------- evaluate

def _norm(text):
    import re
    text = text.lower()
    text = re.sub(r"\[inaudible\]", " ", text)
    text = re.sub(r"[’']", "' ", text)          # l'état -> l' état (elision split, symmetric on both sides)
    text = re.sub(r"[^\w\s']", " ", text)
    return " ".join(text.split())


def _read_ref_lines(path):
    return [l for l in Path(path).read_text().splitlines() if l.strip() and not l.startswith("#")]


def cmd_evaluate(a):
    import re
    import jiwer
    sd = a.out / "sample"
    info = load(sd / "sample.json")
    start, length = info["window"]
    end = start + length
    report = {"window": info["window"], "evaluated_at": now()}

    # --- WER of the sample, ASR vs corrected reference
    strip_ts = lambda l: re.sub(r"^\[\d\d:\d\d:\d\d\.\d+\]\s*", "", l)
    ref = _norm(" ".join(strip_ts(l) for l in _read_ref_lines(sd / "reference-text.txt")))
    hyp = _norm(" ".join(strip_ts(l) for l in _read_ref_lines(sd / "asr-hypothesis.txt")))
    m = jiwer.process_words(ref, hyp)
    report["wer"] = {"wer": round(m.wer, 4), "substitutions": m.substitutions, "deletions": m.deletions,
                     "insertions": m.insertions, "ref_words": len(ref.split()), "hyp_words": len(hyp.split()),
                     "reference_is_hand_corrected": a.ref_corrected}

    # --- DER of the sample, if both RTTMs exist
    if (sd / "reference-speakers.rttm").exists() and (sd / "diarization-hypothesis.rttm").exists():
        from pyannote.core import Annotation, Segment
        from pyannote.metrics.diarization import DiarizationErrorRate

        def rttm(path):
            ann = Annotation()
            for l in _read_ref_lines(path):
                f = l.split()
                ann[Segment(float(f[3]), float(f[3]) + float(f[4]))] = f[7]
            return ann
        r, h = rttm(sd / "reference-speakers.rttm"), rttm(sd / "diarization-hypothesis.rttm")
        der = DiarizationErrorRate(collar=0.0, skip_overlap=False)
        d = der(r, h, detailed=True)
        total = d["total"] or 1
        report["der"] = {"der": round(d["diarization error rate"], 4),
                         "false_alarm": round(d["false alarm"] / total, 4),
                         "missed": round(d["missed detection"] / total, 4),
                         "confusion": round(d["confusion"] / total, 4),
                         "ref_speech_s": round(d["total"], 1),
                         "reference_is_hand_corrected": a.ref_corrected}
        # overlapped speech share in the reference
        from pyannote.core import Timeline
        ov = r.get_overlap()
        report["overlap"] = {"ref_overlap_s": round(ov.duration(), 1),
                             "ref_overlap_share": round(ov.duration() / total, 4)}

    # --- hallucination flags over the whole ASR output (heuristics, not ground truth)
    asr = load(a.out / "asr.json")
    flags = []
    for s in asr["segments"]:
        words = s["text"].split()
        reasons = []
        if s["compression_ratio"] > 2.4:
            reasons.append("compression_ratio>2.4")
        if s["no_speech_prob"] > 0.6:
            reasons.append("no_speech_prob>0.6")
        if s["avg_logprob"] < -1.0:
            reasons.append("avg_logprob<-1.0")
        if len(words) >= 4 and len(set(words)) / len(words) < 0.5:
            reasons.append("repeated words")
        dur = s["end"] - s["start"]
        if dur > 0 and len(words) / dur > 8:  # 6-7 words/s is normal fast French debate speech
            reasons.append("words/s>8")
        if re.search(r"sous-titr|abonn|merci d'avoir regardé|amara\.org", s["text"], re.I):
            reasons.append("caption boilerplate")
        if reasons:
            flags.append({"start": s["start"], "end": s["end"], "text": s["text"], "reasons": reasons})
    report["hallucination_flags"] = {"segments_total": len(asr["segments"]), "flagged": len(flags),
                                     "share": round(len(flags) / max(1, len(asr["segments"])), 4),
                                     "in_sample": [f for f in flags if f["end"] > start and f["start"] < end],
                                     "all": flags}
    report["timing"] = {"asr_wall_per_audio_hour_s": asr["wall_per_audio_hour_s"]}
    if (a.out / "diarization.json").exists():
        report["timing"]["diarization_wall_per_audio_hour_s"] = load(a.out / "diarization.json")["wall_per_audio_hour_s"]
    dump(report, sd / "evaluation.json")
    print(json.dumps({k: v for k, v in report.items() if k != "hallucination_flags"}, indent=1, ensure_ascii=False))
    print(f"hallucination flags: {len(flags)} / {len(asr['segments'])} segments")


# ---------------------------------------------------------------- main

def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("cmd", choices=["prepare", "asr", "patch", "diarize", "merge", "sample", "evaluate", "all"])
    p.add_argument("--media", default=str(Path.home() / "fact-checked-politics-media/rpURHoN54bQ.m4a"))
    p.add_argument("--out", type=Path, default=DEFAULT_OUT)
    p.add_argument("--model", default=None, help="ASR or diarization model override")
    p.add_argument("--clip", nargs=2, type=float, metavar=("START", "LENGTH"), help="asr: only this window (s)")
    p.add_argument("--window", nargs=2, type=float, default=[3600.0, 300.0], metavar=("START", "LENGTH"),
                   help="sample: evaluation window (s)")
    p.add_argument("--speakers", type=int, default=None, help="diarize: number of speakers hint")
    p.add_argument("--cpu", action="store_true", help="diarize: force CPU")
    p.add_argument("--ref-corrected", action="store_true", help="evaluate: the references were hand-corrected")
    a = p.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    steps = ["prepare", "asr", "patch", "diarize", "merge", "sample"] if a.cmd == "all" else [a.cmd]
    for step in steps:
        if step in ("asr", "patch"):
            a.model = a.model if a.cmd != "all" and a.model else ASR_MODEL
        if step == "diarize":
            a.model = a.model if a.cmd != "all" and a.model else DIAR_MODEL
        print(f"== {step}")
        globals()[f"cmd_{step}"](a)


if __name__ == "__main__":
    main()
