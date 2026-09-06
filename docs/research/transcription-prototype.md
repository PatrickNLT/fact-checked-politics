# Local transcription pipeline on the Mac: prototype findings (issue #13)

Question answered: what does a real transcript of one multi-candidate Appearance look like when
produced on Patrick's Apple Silicon Mac, and is the quality good enough to seed community
correction? Prototype code: `prototypes/transcription/` (throwaway; the validated decisions are
below and feed tickets #14 and #15).

Status on 2026-09-06: speech recognition ran on the whole debate. **Diarization has not run**
(the pyannote models are gated behind a Hugging Face login that does not exist on the Mac yet), and
the **hand-corrected reference is not written yet**, so the error rates below are proxies, marked
as such. Both are one command away once the two human steps are done (see "What is left").

## Setup

| Item | Value |
|---|---|
| Machine | Apple M5, 32 GiB unified memory, macOS 27.0 |
| Appearance | D1, MEDEF debate of 2026-08-27 on LCI, seven candidates, 3 h 04 min 15 s |
| Media | `~/fact-checked-politics-media/rpURHoN54bQ.m4a`, AAC-LC 128 kbit/s 44.1 kHz stereo, 178 787 602 bytes, sha256 `c57f025e…a26f9a` (verified again before the run) |
| Acquisition | yt-dlp 2026.08.19, logged out, no account, LCI's own YouTube upload, about one minute, no platform friction (issue #28) |
| Speech recognition | Whisper large-v3 on MLX (`mlx-community/whisper-large-v3-mlx`, mlx-whisper 0.4.3), French forced, word timestamps, `condition_on_previous_text=False`, short French initial prompt |
| Diarization | pyannote `speaker-diarization-3.1` through pyannote.audio 4.0.7 on MPS, not yet run (gated model) |
| Environment | `uv` project, Python 3.12, ffmpeg 9 for the 16 kHz mono conversion; models cached under `~/.cache/huggingface` (3 GB for large-v3, 1.6 GB for turbo) |
| Deletion | Not deleted: ADR 0003 amendment of 2026-09-06 holds prototype-stage recordings; provenance says "held, prototype stage" |

## Wall-clock

| Step | Wall-clock | Per audio hour |
|---|---|---|
| Download (issue #28) | about 1 min | 20 s |
| m4a to 16 kHz mono wav (ffmpeg) | 10.6 s | 3.5 s |
| Whisper large-v3 model download, first time only | 1 min 34 s | |
| Whisper large-v3, word timestamps, whole debate | 29.8 min | **9.7 min** (about 6x real time) |
| Gap repair (12 gaps re-transcribed) | 22 s | 7 s |
| Whisper large-v3-turbo on 5 min (cross-check only) | 12 s | 3.0 min |
| pyannote 3.1 diarization | not run | model card order of magnitude: a few minutes per hour on GPU |

The M5 was otherwise idle, on mains power, with the display on. The ASR run was launched in the
background and finished without intervention. Bridge ticket #15 can plan on **under 15 minutes
per audio hour for ASR plus diarization**, so a three-hour debate lands in under an hour.

## Output shape (input to ticket #14)

`out/transcript.json` (3.3 MB for three hours, 35 468 words) and `out/transcript.txt`, a readable
rendering of the same. Top level:

```json
{
 "schema": "fcp-transcript-prototype/0",
 "appearance": {"catalogue_row": "D1", "title": "…", "date": "2026-08-27", "source": "LCI (TF1 group)",
                "official_replay": "https://www.youtube.com/watch?v=rpURHoN54bQ", "participants": ["…"],
                "presenter": "Amélie Carrouër", "acquisition_basis": "tolerated"},
 "provenance": {"fetch_date": "2026-09-06", "fetch_method": "yt-dlp 2026.08.19, logged out, …",
                "media_sha256": "c57f…a26f9a", "media_bytes": 178787602,
                "deletion_date": "held, prototype stage (ADR 0003 amendment of 2026-09-06)"},
 "pipeline": {"asr": {"model": "mlx-community/whisper-large-v3-mlx", "wall_s": 1788.2, "run_at": "…"},
              "diarization": null, "merge_run_at": "…"},
 "speakers": {"SPEAKER_00": {"participant": null}},
 "segments": [
  {"id": 920, "speaker": "SPEAKER_03", "start": 7652.5, "end": 7734.44,
   "text": "puissions les expliquer détailler toutes les lignes …",
   "words": [{"w": "puissions", "s": 7652.5, "e": 7653.0, "p": 0.93}, …],
   "overlap_words": 0,
   "validation": {"text": "draft", "speaker": "draft"}}
 ]
}
```

What the real run taught about the shape:

- **Segments are made by the merge, not by Whisper.** Whisper's own segments are caption lines
  (median 2.3 s, 9 words). The merge regroups words on speaker change, sentence end or a pause over
  1.5 s. Without diarization the only cut is sentence end, and turns run together: the segment
  above is 82 s long and contains a business owner's question, the presenter's hand-over and the
  start of Marine Tondelier's answer. **Speaker change is the primary segment boundary**; the data
  model should assume that, and the Segment id cannot be Whisper's.
- **Word timestamps are cheap and usable.** Every word carries start, end and a probability.
  Probability is a useful correction hint: 541 words of 35 468 (1.5 percent) are under 0.5, and
  spot checks find them on proper nouns ("Carouèr", "Tourdelier", "Lecouf" for Lecoufle) and
  numbers. The data model should keep word times and the probability at least until a Segment is
  `verified`.
- **Speaker labels are cluster ids** (`SPEAKER_03`), and the mapping to a Participant is a human
  step recorded once per Appearance in `speakers`. Non-candidate speakers (presenter, the five
  business owners, Patrick Martin) need Speaker entries too: they are a third of the sample's words.
- **Overlap is a per-word flag** rolled up as `overlap_words` per Segment; it comes from
  diarization only, so it is 0 in this run.
- **Two Validation statuses per Segment**, `text` and `speaker`, both `draft` at emit time, as
  decided in #10.
- Segment times are offsets into the official replay's audio track; the download is the replay
  itself, so no offset mapping was needed for D1. It will be needed for a stream capture.

## Quality

### Word error rate: proxy only, hand correction pending

The five-minute evaluation window is **02:06:40 to 02:11:40** (window `7600 300`): the presenter's
question on simplification, a business owner's question on payslips, and the exchange between the
presenter and Marine Tondelier on environmental norms, with overlapping speech. Four speakers,
1 095 words. The ASR text of that window is in `out/sample/asr-hypothesis.txt`; the file to
hand-correct is `out/sample/reference-text.txt` (a copy, to be edited to the ear against the clip
at `~/fact-checked-politics-media/work/sample-7600-300.wav`); `uv run pipeline.py evaluate
--ref-corrected` then prints WER.

Until then, the only number is a **cross-model disagreement**: Whisper large-v3 against
large-v3-turbo on the same window gives 6.6 percent (11 substitutions, 43 deletions, 18 insertions
over 1 095 words). Both models share Whisper's training and blind spots, so this is a lower bound on
the true error, not a WER. Reading the text (see the excerpt below) suggests the true WER of the
window is in the published 4 to 6 percent band on the calm passages and higher in the overlap,
consistent with the 8 to 15 percent estimate in `evidence-base.md` section H, but that is a reading,
not a measurement.

Systematic errors seen while reading the whole transcript:

- **Proper nouns**: "Amélie Carouèr" (Carrouër), "Marie-Tourdelier" (Marine Tondelier),
  "Colombe Lecouf" (Lecoufle), "Éric Malenfer". A per-Appearance vocabulary in the initial prompt
  (participants, presenter, questioners) is the obvious fix and costs nothing.
- **Numbers**: "20 à 5,5" is right, but "un quart de la dépense" style figures are the place to
  check first; the correction interface should surface every digit.
- **Punctuation and casing** are Whisper's own and vary between passages (some minutes come out
  all lower-case, comma-less). Fine for search, not for quotation without correction.

### Dropped speech: the real defect

Whisper skipped **two whole 30-second windows** of ordinary speech (at 00:25:04 and 02:22:54), with
no sign in its confidence scores: a question by a business owner and Édouard Philippe's reply to
Marine Le Pen simply were not there. Audio level in the holes is the same as everywhere else. Ten
smaller gaps (3 to 10 s) are mostly jingles, applause and turn-taking noise. Re-transcribing each
gap in isolation recovers the speech: the `patch` step added 200 words, 195 of them in the two
holes. This is silent loss, invisible to hallucination checks, and the production pipeline must
run a **gap detector and re-transcribe** as a standard step (or decode from a voice-activity
segmentation as WhisperX does), not as an afterthought.

### Hallucinations

The usual Whisper heuristics (compression ratio, no-speech probability, log-probability, repeated
words, speaking rate, caption boilerplate) flag 16 segments of 2 960. Fifteen are genuine short
interjections whose word timestamps are squeezed into under a second ("Très bien.", "Marine Le
Pen.", "Je ne peux pas mentir."): a timestamp defect, not invented text. **One is a hallucination**:
"Sous-titrage MFP." over the opening jingle, produced by the gap re-transcription on non-speech
audio, the classic Whisper caption-credit artefact. Zero in the main pass, with
`condition_on_previous_text=False`. The 1 percent figure from "Careless Whisper" is not reproduced
on this audio, on a read-through rather than a full audit; a boilerplate blacklist and skipping
gaps that a voice-activity detector marks as non-speech would remove the one found.

### Diarization and overlap: not measured

`out/sample/reference-speakers.rttm` is written by the `sample` step once diarization exists, and
`evaluate` computes DER (no collar, overlap scored, same convention as the pyannote model card) and
the reference's overlapped-speech share. Expected from the evidence file: DER about 8 percent on
French TV, 10 percent of debate speech overlapped. The sample window was chosen to contain overlap
(the Tondelier / Carrouër cross-talk at 02:08:54 to 02:09:40), where the turbo model already
diverges from large-v3.

### Excerpt of the sample window, as emitted (no speaker labels yet)

```
[02:08:54.440] ?: C'est assez impressionnant ce que vous venez de faire parce que madame nous dit
moi je suis embêtée par les bulletins de paye et par toutes les règles qu'on me met en général elle
n'a absolument pas parlé de normes environnementales et vous, vous me regardez moi en disant que
c'est de ma faute alors qu'elle n'a parlé d'autres normes environnementales Non, je n'ai pas dit
que c'était de sa faute que c'était votre faute pour les fiches de paye Mais la question ne portait
absolument pas sur les normes environnementales Vous savez très bien que je parlais des normes en
général et que c'est vrai que beaucoup d'entrepreneurs nous ont dit Non, vous vous êtes retournée
à moi en tant qu'écologiste en disant c'est vous. Et je précise par ailleurs que je n'ai jamais été
au gouvernement et que mon parti n'y a pas été très longtemps.
[02:09:28.100] ?: Donc si vous avez des récriminations à apporter...
[02:09:31.040] ?: Non, aucune récrimination. L'occasion pour vous de répondre à ce que disent
beaucoup d'entrepreneurs, c'est que les normes, souvent écologiques, sont un peu...
[02:09:37.180] ?: Vous voulez qu'on parle des normes environnementales?
[02:09:38.720] ?: Mais vous répondez à la question que vous voulez.
```

The first Segment alone holds four turns (Tondelier, Carrouër, Tondelier, Carrouër) because no
sentence ends between them and there is no speaker signal yet: exactly what diarization must cut.

## Verdict so far

- **Good enough to seed correction: yes for the text, on the evidence read so far.** Calm passages
  read as a clean draft; a corrector's work is names, numbers, punctuation and the cross-talk, and
  the word probabilities point at most of it.
- **Not good enough to publish uncorrected**, as expected from ADR 0002 and the evidence file, and
  for one reason not in the literature review: silent 30-second drops. The gap repair is
  mandatory.
- **Attribution is entirely on diarization.** Without it the emitted Segments cannot be shown next
  to a name at all; the data model must not assume Whisper's segments carry a speaker.
- **Runtime is a non-issue** for the bridge: 10 minutes per audio hour for ASR on the M5, in the
  background.

## What is left (human steps, then one command each)

1. Log in to Hugging Face on the Mac (`uvx --from huggingface_hub hf auth login`, free account),
   after accepting the terms of `pyannote/speaker-diarization-3.1` and `pyannote/segmentation-3.0`.
   Then `uv run pipeline.py diarize --speakers 13` (seven candidates, presenter, five questioners;
   or without the hint to see what the clustering finds), `merge`, `sample --window 7600 300`.
2. Hand-correct `out/sample/reference-text.txt` and `out/sample/reference-speakers.rttm` against
   the clip, then `uv run pipeline.py evaluate --ref-corrected` and replace the proxies above with
   WER, DER and overlap share.
3. Report back to #13; hand the shape to #14 and the runtime to #15.
