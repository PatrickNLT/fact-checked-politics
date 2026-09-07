# File-based data model for v1

Resolves map ticket #14. The decisions and their reasons are in `docs/adr/0005-file-based-data-model.md`;
this file is the shape itself: directory layout, the Segment grammar and the field list of each file.
Glossary terms (Appearance, Speaker, Role, Segment, Overlap, Timeline, Validation status, Acquisition basis)
are as `CONTEXT.md` defines them. The example rows are taken from the MEDEF debate of 27 August 2026 as
the transcription prototype emitted it (`docs/research/transcription-prototype.md`).

## Layout

```
data/
  appearances/
    2026-08-27-lci-debat-medef/
      appearance.json     metadata, participants, Timeline and replay copies, acquisition, pipeline, cluster map, id counter
      transcript.md       the Segments, the only file correctors edit
      words.json          machine sidecar: word timings and probabilities for Segments whose text is still draft
  speakers/
    marine-tondelier.json
    amelie-carrouer.json
  sources/
    lci.json
    medef.json
schemas/
  appearance.schema.json  speaker.schema.json  source.schema.json  words.schema.json
  transcript-grammar.md   the Segment grammar below, plus the parser's rules
```

Every JSON file carries `"schema": "fcp/1"`. A CI check validates every data file against `schemas/` and
parses every `transcript.md`; a pull request that breaks either does not merge.

Nothing derived is stored: whether an Appearance is a Confrontation (two or more Candidates among its
participants, roles as known today), a Transcript's state (from its Segments), a Speaker's `candidate`
Role in an Appearance (from the registry), the corrections log (from git) are all computed at build time.

## Identifiers

| Thing | Form | Example | Rule |
|---|---|---|---|
| Appearance | `YYYY-MM-DD-<source>-<slug>` | `2026-08-27-lci-debat-medef` | Chosen once at import, never renamed; the catalogue row is a field. |
| Speaker (registry) | name slug | `marine-tondelier` | Suffix on collision (`-2`). |
| Speaker (Appearance-scoped) | `<role>-<n>` inside one Appearance | `questioner-2` | Unnamed voice; promoted to a registry id when identified, the Segments then rewritten in one commit. |
| Source | slug | `lci`, `public-senat`, `medef` | |
| Segment | `s` + counter, unique within the Appearance | `s1093` | From `segments.next_id`; never renumbered or reused; permalink `<appearance>#s1093`. |
| Cluster | the diarizer's label | `SPEAKER_14` | Appears only in `appearance.json`'s cluster map, never in `transcript.md`. |

## `transcript.md`

Front matter, then one block per Segment in Timeline order (overlapping Segments in start order).

```
---
schema: fcp/1
appearance: 2026-08-27-lci-debat-medef
---

### s1092 amelie-carrouer 02:08:54.440 --> 02:08:54.740 text:draft speaker:draft overlap
C

### s1093 marine-tondelier 02:08:54.740 --> 02:09:10.020 text:draft speaker:draft overlap
'est assez impressionnant ce que vous venez de faire parce que madame nous dit moi je suis embêtée par les bulletins de paye et par toutes les règles qu'on me met en général elle n'a absolument pas parlé de normes environnementales et vous, vous me regardez moi en disant que c'est de ma faute alors qu'elle n'a parlé d'autres

### s1094 amelie-carrouer 02:09:10.020 --> 02:09:10.920 text:draft speaker:draft overlap
normes environnementales Non,
```

Header grammar, fields in this fixed order and nothing else on the line:

```
### <segment-id> <speaker-id> <start> --> <end> text:<draft|verified> speaker:<draft|verified> [overlap]
```

- `<start>` and `<end>` are `HH:MM:SS.mmm` on the Appearance's Timeline; `end` is greater than or equal to `start`.
- Both statuses are always written, so a corrector sees what they change. `overlap` is present or absent.
- The text is one paragraph, verbatim, no speaker names, no stage directions; a blank line ends the block.
- A Segment has exactly one Speaker. Two people at once are two Segments with overlapping ranges, both flagged `overlap`.
- What a correction may do: change the text; change the speaker; set a status to `verified` after checking against the replay at the timestamp (the speaker status independently of the text status); split a Segment within one Speaker's turn (the second part takes `segments.next_id`, which the same commit increments); merge adjacent Segments of the same Speaker (the lower id survives, the other is added to `segments.retired`); split where two Speakers were wrongly joined. A human edit not checked against the replay leaves the status `draft`.
- What a correction may not do: renumber, reuse a retired id, join two Speakers in one Segment, reorder blocks out of Timeline order.

The example above is the machine output: `s1092` and `s1093` are one word cut on a boundary-slop speaker change, and the first correction will merge them into the presenter's "C'est assez" and Tondelier's "impressionnant ce que…" with the right boundary.

## `words.json`

Machine-only. One entry per Segment whose text is `draft`; the entry is deleted in the same pull request that sets the text to `verified` (the CI check enforces that no `verified` Segment has words).

```json
{"schema": "fcp/1", "appearance": "2026-08-27-lci-debat-medef",
 "segments": {"s1093": [{"w": "'est", "s": 7734.74, "e": 7735.10, "p": 0.55, "overlap": true}, {"w": "assez", "s": 7735.10, "e": 7735.40, "p": 0.99}]}}
```

Times in seconds on the Timeline; `p` is the recogniser's word probability; `overlap` is present when the word sits under two diarization turns. The site may use it for correction hints (low-probability words, overlap) and nothing else; v3 Statements attach to a Segment id and character offsets in its text, never to word times.

## `appearance.json`

```json
{
  "schema": "fcp/1",
  "id": "2026-08-27-lci-debat-medef",
  "catalogue_row": "D1",
  "title": "Débat MEDEF (REF 2026) des candidats à la présidentielle 2027",
  "date": "2026-08-27",
  "start_time": "16:45",
  "language": "fr",
  "source": "lci",
  "medium": "tv",
  "programme": "Le grand débat du Medef sur LCI",
  "organiser": "medef",
  "venue": "Court Philippe-Chatrier, Roland-Garros, Paris",
  "participants": [
    {"speaker": "gabriel-attal"}, {"speaker": "raphael-glucksmann"}, {"speaker": "marine-le-pen"},
    {"speaker": "jean-luc-melenchon"}, {"speaker": "edouard-philippe"}, {"speaker": "bruno-retailleau"},
    {"speaker": "marine-tondelier"},
    {"speaker": "amelie-carrouer", "role": "journalist"},
    {"speaker": "patrick-martin", "role": "host"},
    {"speaker": "eric-malenfer", "role": "questioner"},
    {"speaker": "questioner-2", "role": "questioner", "label": "Chef d'entreprise, deuxième question"},
    {"speaker": "lci-voix-off", "role": "narration"}
  ],
  "timeline": {"platform": "youtube", "video_id": "rpURHoN54bQ", "url": "https://www.youtube.com/watch?v=rpURHoN54bQ",
               "uploader": "LCI", "duration_s": 11055},
  "replays": [
    {"platform": "youtube", "video_id": "z0gJwsrODEw", "url": "https://www.youtube.com/watch?v=z0gJwsrODEw",
     "uploader": "MEDEF", "carrier": "medef", "offset_s": null, "embeddable": true, "embedded": true,
     "embed_check": {"method": "playableInEmbed", "result": true, "checked_on": "2026-09-05"},
     "tdm_signals": "none published by MEDEF; YouTube ToS", "cgu_version": null, "expiry": null},
    {"platform": "youtube", "video_id": "rpURHoN54bQ", "url": "https://www.youtube.com/watch?v=rpURHoN54bQ",
     "uploader": "LCI", "carrier": "lci", "offset_s": 0, "embeddable": false, "embedded": false,
     "embed_check": {"method": "playableInEmbed", "result": false, "checked_on": "2026-09-05"},
     "tdm_signals": "TF1 CGU art. 9, tdmrep", "cgu_version": "TF1 Info CGU 2025-10-27", "expiry": null},
    {"platform": "tf1plus", "video_id": null, "url": null, "uploader": "TF1", "carrier": "tf1", "offset_s": null,
     "embeddable": false, "embedded": false, "account_wall": true, "expiry": "days to weeks"}
  ],
  "acquisition": {"basis": "tolerated", "fetch_date": "2026-09-06",
                  "method": "download", "tool": "yt-dlp 2026.08.19, logged out, format 140 audio only",
                  "media_sha256": "c57f025ec87d456a64365db9b7c715660987df1199d0b89d6ae39c842ca26f9a",
                  "media_bytes": 178787602, "deletion_date": "held, prototype stage (ADR 0003 amendment of 2026-09-06)"},
  "pipeline": {"asr": {"model": "mlx-community/whisper-large-v3-mlx", "library": "mlx-whisper 0.4.3", "run_at": "2026-09-06T14:22:09Z"},
               "diarization": {"model": "pyannote/speaker-diarization-3.1", "library": "pyannote.audio 4.0.7", "run_at": "2026-09-07T06:13:48Z", "speaker_count_hint": null},
               "merge": {"rule": "most-overlap-ties-shorter/1", "run_at": "2026-09-07T10:26:28Z"},
               "gaps_repaired": 12, "segments_removed": {"noise": 2, "hallucination": 1}},
  "clusters": {"SPEAKER_14": {"speaker": "marine-tondelier", "confirmed": true, "cue": "conseillère régionale des Hauts-de-France; addressed as Tondelier at 02:08:37"},
               "SPEAKER_13": {"speaker": "amelie-carrouer", "confirmed": true, "cue": "moderates throughout"},
               "SPEAKER_10": {"speaker": "questioner-2", "confirmed": false, "cue": "question at 01:03:18"},
               "SPEAKER_15": {"speaker": null, "confirmed": true, "cue": "jingle noise, removed"}},
  "segments": {"next_id": 1607, "retired": {}}
}
```

Field notes:

- `participants[].role` is one of `journalist`, `host`, `questioner`, `narration`, `other`; absent for a Speaker whose Candidate role the registry gives (the build derives `candidate`). `label` is the display name of an Appearance-scoped Speaker.
- `timeline` is the copy that was transcribed (`acquisition` says how it was fetched). Its `offset_s` in `replays` is `0` by definition when it also appears there.
- `replays[]` lists the embedded copy (`embedded: true`, exactly one, or none when the replay has gone) and every other carrier known. `offset_s` is the signed number such that replay time = Segment time + `offset_s`, measured once at import on a cue, `null` until measured. The embed check fields are those of `docs/research/source-terms.md`. A replay that disappears keeps its entry with `expiry` set to the date noticed and `embedded` flipped to `false`.
- `acquisition` is ADR 0003's provenance record; `basis` is the Appearance's own Acquisition basis (it may differ from the Source's default after a notice).
- `pipeline` records what produced the draft: models and library versions, run dates, the merge rule version, gaps re-transcribed, Segments removed as noise or hallucination.
- `clusters` is the cluster-to-Speaker map, human-confirmed once per Appearance; a cluster with `speaker: null` was removed. An unconfirmed mapping leaves the concerned Segments' speaker status `draft`.
- `segments.next_id` is the counter; `segments.retired` maps a merged-away id to the surviving one so the old permalink redirects.

## `speakers/<id>.json`

```json
{
  "schema": "fcp/1",
  "id": "marine-tondelier",
  "name": "Marine Tondelier",
  "kind": "person",
  "party": "Les Écologistes",
  "candidacy": {"contest": "primaire de la gauche unie", "listed_on": "2026-09-05",
                "reference": {"list": "wikipedia-fr", "url": "https://fr.wikipedia.org/wiki/Candidatures_à_l'élection_présidentielle_française_de_2027"},
                "read_on": "2026-09-05", "ended_on": null, "end_reason": null},
  "links": {"wikipedia": "https://fr.wikipedia.org/wiki/Marine_Tondelier"}
}
```

- `kind` is `person` or `narration` (a broadcaster's voice-over, for instance `lci-voix-off`).
- `candidacy` is present only for a Candidate and is the dated role of ADR 0004: `contest` is `election` or the primary's name, `reference.list` is `lcp` or `wikipedia-fr` (`conseil-constitutionnel` once the official list exists), `end_reason` one of `withdrawal`, `primary-lost`, `not-on-official-list`, `dropped-from-references`.
- `party` as the reference list states it. No biography, no photo, nothing editorial.
- Appearance-scoped Speakers (`questioner-2`) have no registry file; their `label` lives on the participant entry.

## `sources/<id>.json`

```json
{
  "schema": "fcp/1",
  "id": "lci",
  "name": "LCI",
  "group": "TF1",
  "kind": "tv",
  "default_acquisition_basis": "tolerated",
  "tdm_opposition": {"status": "express", "where": "CGU TF1 Info art. 9; CG TF1+ I.10; tdmrep.json", "checked_on": "2026-09-05"},
  "embed_policy": {"own_player": "personal sites only", "platform_copies": "YouTube, embeddable per video"},
  "replay_durability": "TF1+ days to weeks; YouTube open-ended",
  "notice": null
}
```

- `kind` is one of `tv`, `radio`, `press`, `organiser`, `party`, `platform`.
- `notice` records a stop-transcribing request if one ever arrives: `{"received_on", "asked", "effect"}`; ADR 0003 then flips `default_acquisition_basis` to `by-ear` for future imports.

## Deliberately not designed yet

- A piecewise offset for a replay copy with cuts (the fog of the map): a single `offset_s` per copy until such a copy appears.
- Where v2 Topics and v3 Statements live (their own files keyed by `<appearance>#<segment-id>` and character offsets is the expectation, not a decision).
