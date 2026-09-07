---
status: accepted
---

# File-based data model: edited text apart from machine timing, one Speaker per Segment, permanent ids, one Timeline per Appearance

The transcription prototype (`docs/research/transcription-prototype.md`) emits one JSON per Appearance in which every Segment carries its text, its word timings and probabilities and its two Validation statuses, and the first real import already had its audio taken from one replay copy (LCI's upload, 3 h 04 min) while the embeddable copy is another (MEDEF's, 3 h 12 min). Corrections arrive as pull requests from readers who are not developers (ADR 0001), v2 and v3 must attach to Segments without a migration, and the audio is deleted after the run (ADR 0003), so nothing can be re-aligned later. We decided that each Appearance is a directory holding a metadata file (`appearance.json`), a Segment file humans edit (`transcript.md`, a strict one-line header per Segment followed by its text) and a machine-only word sidecar (`words.json`) that is dropped Segment by Segment as text is verified; that a Segment has exactly one Speaker and Overlap is two Segments with overlapping time ranges; that Segment ids come from a per-Appearance counter and are never renumbered or reused; and that Segment times are counted on one Timeline per Appearance, the transcribed copy, with every replay copy carrying an offset to it. Speakers and Sources are registries, one JSON file each. The full field lists and the grammar are in `docs/data-model.md`.

## Considered options

- **One JSON per Appearance with everything inside**, as the prototype emits. Rejected: a one-word correction diffs against a word array that the correction has just made stale, and a reviewer cannot see the change for the noise.
- **JSON Lines or a pretty-printed JSON array for the Segments.** Rejected: one-line diffs at the price of text tangled with structure; the GitHub web editor is the correction tool, and a Markdown paragraph is what a non-developer can edit without breaking the file. The grammar is enforced by a schema check in CI rather than trusted.
- **Keeping word timings forever**, with a stale flag once the text is corrected. Rejected: a timing known to be wrong is worse than none, and it would tempt v3 to attach Statements to word times; they attach to a Segment and character offsets instead.
- **A Segment with two Speakers** for simultaneous speech. Rejected: a Statement must have one author, and the passages where two people talk at once are exactly where "who said this" matters most.
- **Segment ids from the start time**, or content hashes. Rejected: both change when a corrector moves a boundary or fixes a word, and v2 Topics and v3 Statements point at these ids.
- **Rebasing Segment times onto the embedded copy** at import. Rejected: the embed can be swapped when a copy disappears, and a swap would rewrite every Segment; an offset per copy is one number.
- **YAML or front-matter metadata.** Rejected in favour of JSON: the metadata is pipeline-written and rarely hand-edited, and JSON Schema validation is native.

## Consequences

- A correction pull request is a diff on a text paragraph, or on the header line when a Segment is verified, split or merged. CI validates every data file against `schemas/` and rejects a `transcript.md` the parser cannot read.
- Correctors may split or merge Segments within one Speaker's turn and must split where two Speakers were wrongly joined; a split takes a fresh id from the counter, a merge keeps the lower id and records the retired one so its permalink redirects.
- Speaker attribution is a mapping from machine clusters to Speaker ids recorded once per Appearance with a `confirmed` flag; Segments reference Speaker ids, never cluster labels. Unnamed voices are Appearance-scoped Speakers; a broadcaster's voice-over is a Speaker of kind `narration`; noise clusters are removed at import and counted in provenance.
- Word timings and probabilities exist only for Segments whose text is still `draft`; Segment start and end are the only durable timing. Nothing downstream may depend on word times.
- Swapping the embedded replay means measuring one offset, never touching the Transcript. A piecewise offset for a cut copy is deliberately not designed until such a copy appears.
- Raw ASR and diarization outputs stay on the Mac; the repository holds the merged result and the provenance and pipeline records only.
- Every data file carries a `schema` field (`fcp/1`); v2 and v3 bump the version rather than migrate.
