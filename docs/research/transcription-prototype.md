# Local transcription pipeline on the Mac: prototype findings (issue #13)

Question answered: what does a real transcript of one multi-candidate Appearance look like when
produced on Patrick's Apple Silicon Mac, and is the quality good enough to seed community
correction? Prototype code: `prototypes/transcription/` (throwaway; the validated decisions are
below and feed tickets #14 and #15).

Status on 2026-09-07: speech recognition and diarization both ran on the whole debate, and the
five-minute sample's **text was hand-corrected** (WER measured). The speaker reference was not
corrected: fixing an RTTM with sub-second fragments in cross-talk proved unreasonable to ask, so
DER stays unmeasured and a segment-level attribution check is offered instead (see "What is left").

## Setup

| Item | Value |
|---|---|
| Machine | Apple M5, 32 GiB unified memory, macOS 27.0 |
| Appearance | D1, MEDEF debate of 2026-08-27 on LCI, seven candidates, 3 h 04 min 15 s |
| Media | `~/fact-checked-politics-media/rpURHoN54bQ.m4a`, AAC-LC 128 kbit/s 44.1 kHz stereo, 178 787 602 bytes, sha256 `c57f025e…a26f9a` (verified again before the run) |
| Acquisition | yt-dlp 2026.08.19, logged out, no account, LCI's own YouTube upload, about one minute, no platform friction (issue #28) |
| Speech recognition | Whisper large-v3 on MLX (`mlx-community/whisper-large-v3-mlx`, mlx-whisper 0.4.3), French forced, word timestamps, `condition_on_previous_text=False`, short French initial prompt |
| Diarization | pyannote `speaker-diarization-3.1` (segmentation-3.0 + wespeaker embeddings + agglomerative clustering, the published 3.1 config) through pyannote.audio 4.0.7 on MPS, no speaker-count hint |
| Environment | `uv` project, Python 3.13, ffmpeg 9 for the 16 kHz mono conversion; models cached under `~/.cache/huggingface` (3 GB for large-v3, 1.6 GB for turbo, 30 MB for pyannote) |
| Deletion | Not deleted: ADR 0003 amendment of 2026-09-06 holds prototype-stage recordings; provenance says "held, prototype stage" |

Platform friction met, all worked around in `pipeline.py` and none needing a paid service:

- The pyannote models are **gated**: a free Hugging Face account, the terms accepted on two model
  pages, and `hf auth login` on the Mac. One-time.
- pyannote.audio 4 fills the 3.1 config's missing PLDA with its own default, hosted in a third
  gated repository (`speaker-diarization-community-1`); 3.1 never uses a PLDA, so the pipeline is
  built by hand from the published 3.1 config with the PLDA loader bypassed. Pinning
  pyannote.audio 3.x instead is not possible with torch 2.14.
- pyannote 4 decodes audio through torchcodec, which does not load against Homebrew's ffmpeg 9;
  the waveform is read with the standard library and handed over in memory (documented option).

## Wall-clock

| Step | Wall-clock | Per audio hour |
|---|---|---|
| Download (issue #28) | about 1 min | 20 s |
| m4a to 16 kHz mono wav (ffmpeg) | 10.6 s | 3.5 s |
| Whisper large-v3 model download, first time only | 1 min 34 s | |
| Whisper large-v3, word timestamps, whole debate | 29.8 min | **9.7 min** (about 6x real time) |
| Gap repair (12 gaps re-transcribed) | 22 s | 7 s |
| pyannote 3.1 diarization, whole debate, MPS | 11.4 min | **3.7 min** |
| Merge, sample, evaluation | seconds | |
| **Whole pipeline** | **42 min** | **13.6 min** |
| Whisper large-v3-turbo on 5 min (cross-check only) | 12 s | 3.0 min |

The M5 was otherwise idle, on mains power, with the display on. Both long steps ran in the
background and finished without intervention. Bridge ticket #15 can plan on **about 14 minutes
per audio hour**, so a three-hour debate lands in under an hour; the two long steps are
independent and could overlap.

## Output shape (input to ticket #14)

`out/transcript.json` (3.4 MB for three hours, 35 468 words, 1 470 Segments) and
`out/transcript.txt`, a readable rendering of the same. Top level:

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
              "diarization": {"model": "pyannote/speaker-diarization-3.1", "wall_s": 683.8, "run_at": "…",
                              "num_speakers_hint": null},
              "merge_run_at": "…"},
 "speakers": {"SPEAKER_00": {"participant": null}, "…": {}},
 "segments": [
  {"id": 1001, "speaker": "SPEAKER_14", "start": 7734.98, "end": 7750.92,
   "text": "impressionnant ce que vous venez de faire parce que madame nous dit …",
   "words": [{"w": "impressionnant", "s": 7734.98, "e": 7737.72, "p": 0.998}, …],
   "overlap_words": 5,
   "validation": {"text": "draft", "speaker": "draft"}}
 ]
}
```

What the real run taught about the shape:

- **Segments are made by the merge, not by Whisper.** Whisper's own segments are caption lines
  (median 2.3 s, 9 words). The merge assigns each word the diarization speaker covering it (nearest
  turn within 1 s when none does), then cuts on speaker change, sentence end or a pause over 1.5 s.
  **Speaker change is the primary segment boundary**: without diarization the same window came out
  as one 82-second Segment holding four turns. The Segment id cannot be Whisper's.
- **Word timestamps are cheap and usable.** Every word carries start, end and a probability.
  Probability is a useful correction hint: 541 words of 35 468 (1.5 percent) are under 0.5, and
  spot checks find them on proper nouns ("Carouèr", "Tourdelier", "Lecouf" for Lecoufle) and
  numbers. The data model should keep word times and the probability at least until a Segment is
  `verified`.
- **Speaker labels are cluster ids** (`SPEAKER_14`), and the mapping to a Participant is a human
  step recorded once per Appearance in `speakers`. On this debate the mapping is a five-minute job
  (see the cluster table below). Non-candidate speakers (presenter, MEDEF president, five business
  owners) need Speaker entries too: they are a third of the sample's words.
- **Overlap is a per-word flag** rolled up as `overlap_words` per Segment: 888 words of 35 468
  (2.5 percent) sit under two diarization turns at once, concentrated in the exchanges.
- **Two Validation statuses per Segment**, `text` and `speaker`, both `draft` at emit time, as
  decided in #10.
- Segment times are offsets into the official replay's audio track; the download is the replay
  itself, so no offset mapping was needed for D1. It will be needed for a stream capture.

## Quality

### Word error rate: 1.1 percent measured, 0.5 percent net of spelling conventions

The five-minute evaluation window is **02:06:40 to 02:11:40** (window `7600 300`): the presenter's
question on simplification, a business owner's question on payslips, and the exchange between the
presenter and Marine Tondelier on environmental norms, with overlapping speech. Four speakers,
1 094 reference words. Patrick corrected `out/sample/reference-text.txt` against the clip on
2026-09-07; `uv run pipeline.py evaluate --ref-corrected` gives:

| | Count |
|---|---|
| Reference words | 1 094 |
| Substitutions | 11 |
| Deletions | 0 |
| Insertions | 1 |
| **WER** | **1.1 percent** |

Of the 12 errors, 7 are spelling conventions the scorer cannot tell from mistakes ("paye" for
"paie" six times, "Châtrier" for "Chatrier"). The genuine recognition errors are five: "simplifier"
for "simplifiez", "Lecouf" for "Lecoufle", "Marie-Tourdelier" for "Marine Tondelier", "CPN" for
"CPAM", and an extra "le". Net of spelling conventions the window's WER is **0.5 percent**, and every
real error is a proper noun, an acronym or a verb ending: the shape the correction interface should
optimise for. This is far below the 4 to 6 percent published for French read speech and the 8 to 15
percent estimated for debates in `evidence-base.md` section H; the window has one cross-talk
passage and three articulate speakers, so it is a favourable but not exceptional sample, and a
debate-wide figure needs more windows.

For comparison, the **cross-model disagreement** on the same window (Whisper large-v3 against
large-v3-turbo) was 6.6 percent, six times the measured WER: the turbo model drops words that
large-v3 gets right, so disagreement is not a usable proxy for large-v3's error.

Systematic errors seen while reading the whole transcript:

- **Proper nouns**: "Amélie Carouèr" (Carrouër), "Marie-Tourdelier" (Marine Tondelier),
  "Colombe Lecouf" (Lecoufle), "Éric Malenfer". A per-Appearance vocabulary in the initial prompt
  (participants, presenter, questioners) is the obvious fix and costs nothing.
- **Numbers**: "20 à 5,5" is right, but "un quart de la dépense" style figures are the place to
  check first; the correction interface should surface every digit.
- **Punctuation and casing** are Whisper's own and vary between passages (some minutes come out
  all lower-case, comma-less). Fine for search, not for quotation without correction.

### Dropped speech: the real ASR defect

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

### Diarization: clusters map cleanly to people

pyannote 3.1 found **17 clusters** in 1 023 turns with no speaker-count hint. Speech time per
cluster, with the identity read off the transcript (first words, content):

| Cluster | Speech | Words | Who (from the text) |
|---|---|---|---|
| SPEAKER_09, 14, 12, 16, 07, 06, 02 | 20.5 to 23.0 min each | 3 700 to 5 000 each | the seven candidates (Tondelier is 14; the others are a five-minute mapping job) |
| SPEAKER_13 | 14.6 min | 2 950 | Amélie Carrouër, presenter |
| SPEAKER_01 | 2.6 min | 402 | Patrick Martin, MEDEF president, opening |
| SPEAKER_03, 11, 00, 10, 05 | 0.9 to 2.5 min each | 160 to 470 | the five business owners' questions |
| SPEAKER_04 | 0.6 min | 75 | LCI voice-over of the opening |
| SPEAKER_15, 08 | under 0.5 min | 11, 36 | jingle noise, the hallucinated caption credit |

Seven near-equal candidate shares is what a moderated debate should produce, and no cluster
splits or merges a person as far as reading shows: 14 real speakers, 3 noise clusters. The
`speakers` mapping in the output is exactly this table, to be filled once per Appearance.

### Attribution in cross-talk: the real diarization defect

Diarization is right about who speaks when, as far as reading the turns shows (the readable
rendering `out/sample/speakers-readable.txt` lists every turn with the words in it). The errors
arise in the **merge of words onto turns**, in two ways:

- **Boundary slop**: Whisper's word timestamps drift by a word or two, and the word lands in the
  neighbour's turn ("Non, je n'ai pas" goes to Tondelier, "dit que c'était de sa faute" to the
  presenter, who said all of it).
- **Nested turns**: when a short interjection sits inside a longer turn, both turns cover the
  words and the merge has to choose. pyannote had "Non, aucune récrimination. L'occasion pour
  vous de répondre…" as a 4-second presenter turn inside a 17-second Tondelier turn; the merge
  gave the words to Tondelier. A "prefer the shorter covering turn" rule would fix this case and
  should be tested against the attribution check before being adopted.

In calm passages neither matters. In the sample window's cross-talk the exchange comes out as
alternating short Segments, most flagged `[chevauchement]`, with about one boundary in three
carrying the wrong first or last words. This is the misattribution in heated exchanges that the
evidence file predicted, and it is where the `speaker` Validation status earns its place: the
overlap flags point a corrector at exactly these Segments (888 words in the whole debate). No
speaker-count hint (`--speakers 14`) was tried; it would not change either mechanism.

**DER is not measured.** Correcting the RTTM (39 turns in the window, many under a second in the
cross-talk) was judged unreasonable by the corrector, rightly: it is a research-benchmark format,
not a correction workflow. What the site needs is the per-Segment answer "is this speaker
right?", so the `sample` step now writes `out/sample/attribution-check.txt`, one emitted Segment
per line (33 in the window), where the corrector marks each as right, wrong (with the right
label) or genuinely both; `evaluate` turns it into a Segment- and word-level attribution error
rate. The diarization hypothesis marks 4.5 percent of the window's speech time as overlapped, in
line with the 6 to 10 percent published for French TV debates.

### Excerpt of the sample window, as emitted

```
[02:08:37.120] SPEAKER_13: Lecouf alors je vous ai entendu, Marie -Tourdelier vous disiez je termine
toujours, je suis toujours à la fin vous allez commencer, parce que quand même, on le sait, vous le
savez très certainement, souvent quand on parle de normes il y a beaucoup d'entrepreneurs qui nous
disent l'écologie c'est beaucoup de normes et puis si vous arrivez au pouvoir il y en aura
certainement encore plus alors qu'est-ce que vous...
[02:08:54.440] SPEAKER_13 [chevauchement]: C'est assez
[02:08:54.980] SPEAKER_14 [chevauchement]: impressionnant ce que vous venez de faire parce que madame
nous dit moi je suis embêtée par les bulletins de paye et par toutes les règles qu'on me met en
général elle n'a absolument pas parlé de normes environnementales et vous, vous me regardez moi en
disant que c'est de ma faute alors qu'elle n'a parlé d'autres normes environnementales Non, je n'ai pas
[02:09:10.920] SPEAKER_13 [chevauchement]: dit que c'était de sa faute que c'était votre faute pour
les fiches de paye Mais la question
[02:09:14.340] SPEAKER_14 [chevauchement]: ne portait absolument pas sur les normes environnementales
Vous savez très bien que je parlais
[02:09:16.860] SPEAKER_13 [chevauchement]: des normes en général et que c'est vrai que beaucoup
d'entrepreneurs nous ont dit Non, vous vous êtes
[02:09:20.300] SPEAKER_14 [chevauchement]: retournée à moi en tant qu'écologiste en disant c'est vous.
Et je précise par ailleurs que je n'ai jamais été au gouvernement et que mon parti n'y a pas été
très longtemps.
[02:09:28.100] SPEAKER_14: Donc si vous avez des récriminations à apporter...
[02:09:31.040] SPEAKER_14 [chevauchement]: Non, aucune récrimination. L'occasion pour vous de répondre
à ce que disent beaucoup d'entrepreneurs, c'est que les
[02:09:35.760] SPEAKER_13 [chevauchement]: normes, souvent
[02:09:36.200] SPEAKER_14 [chevauchement]: écologiques,
[02:09:36.780] SPEAKER_13 [chevauchement]: sont un
[02:09:37.080] SPEAKER_14 [chevauchement]: peu...
[02:09:37.180] SPEAKER_14 [chevauchement]: Vous voulez qu'on parle des normes environnementales?
[02:09:38.720] SPEAKER_14: Mais vous répondez à la question que vous voulez.
```

SPEAKER_13 is the presenter, SPEAKER_14 Marine Tondelier. "Non, aucune récrimination. L'occasion
pour vous de répondre…" reads as the presenter's and is attributed to 14; the "Non, je n'ai pas /
dit que" split and the interleaved "normes, souvent / écologiques, / sont un / peu..." show the
boundary slop. The text of the same passage is essentially right. (Read from the text, not
checked against the audio: the hand-corrected RTTM settles it.)

## Verdict

- **Good enough to seed correction: yes.** Measured WER of 1.1 percent on the sample (0.5 percent
  net of spelling conventions), every real error a name, an acronym or a verb ending; calm
  passages carry the right speaker. A corrector's work is names, numbers, punctuation and the
  cross-talk, and the word probabilities and overlap flags point at most of it.
- **Not good enough to publish uncorrected**, as expected from ADR 0002 and the evidence file, for
  two reasons: silent 30-second drops in ASR (repaired by the gap step, which is mandatory) and
  boundary misattribution in cross-talk (2.5 percent of words flagged, to be human-verified).
- **Runtime is a non-issue** for the bridge: 14 minutes per audio hour on the M5, in the
  background, both models open weights and free.
- **Model choice**: Whisper large-v3 on MLX and pyannote 3.1 are enough for v1. Voxtral, WhisperX
  alignment and Parakeet were not run; the case for them would be boundary accuracy and the
  30-second drops, both of which a gap step and diarization-driven segmentation address more
  cheaply. Worth revisiting once the hand-corrected WER exists.

## What is left

1. Attribution check: in `out/sample/attribution-check.txt`, replace the leading `?` of each of
   the 33 lines with `ok`, the right speaker label, or `both`; then `uv run pipeline.py evaluate
   --ref-corrected` reports the Segment- and word-level attribution error rate, the number that
   replaces DER above.
2. Fill the `speakers` mapping for D1 (the table above) and hand the shape to #14, the runtime to
   #15. The 5-minute corrected sample is the first verified span of the corpus and the baseline for
   the running WER the site is meant to publish.
