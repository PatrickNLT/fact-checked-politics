# Site skeleton — throwaway prototype (map ticket #17)

**This is not production code and must not be merged into `main`.** No tests, no error
handling, no accessibility pass. It exists to answer one question: *what does v1 look and
feel like on a real transcript?*

**Variant D is the answer the ticket settled on**; A, B and C are the three originals it
was assembled from, kept for comparison. All of them read the real MEDEF debate of
27 August 2026 — 1 595 Segments, 3 h 04, produced by the transcription prototype of
ticket #13.

## Run it

```sh
cd prototypes/site
npm install
npm run dev          # http://127.0.0.1:4321
```

It opens on variant D. The switcher is the black bar at the bottom: `←` / `→`, or the
arrow keys, or `?variant=D|A|B|C` in the URL. It only works on the dev server (the pages
are rendered on demand for exactly that reason).

The embedded player needs YouTube to be reachable; without it the transcript still works
and clicking a timestamp opens the replay in a new tab instead.

## The variants

**D — Studio + repérage** is the one that won, built from Patrick's reaction to the other
three: B's layout, A's turn grouping, C's ribbon. On top of those:

- The page is a **fixed shell** — only the transcript column scrolls. The site footer is
  hidden here and its notice moved into the aside, because a fixed shell has no room for
  one.
- The ribbon names the Speaker in a **popover on hover**. Names inside the bands were
  tried first and do not fit (only 1 of 412 bands is wide enough at 1 440 px; the median
  turn is 2.1 s), and so was one lane per Speaker with names in a gutter — it cost 210 px
  of height and lost the single left-to-right read.
- **No speaking time anywhere**, per ADR 0004 as amended. The cast list is split into
  Candidat·es and autres, sorted by surname with particles kept on the surname.

The three it came from:

| | Name | Puts first | Shape |
|---|---|---|---|
| **A** | Lecture | reading | One narrow column of prose. Consecutive Segments of one Speaker are fused into a turn. The replay is a slim sticky strip you unfold if you want it. Reads like an article. |
| **B** | Studio | the replay | Two columns: large sticky player and metadata on the left, one row per Segment on the right, following playback and scrolling itself. Each Segment shows both its statuses, its permalink and a "correct this" link. The reading view and the correction view at once. |
| **C** | Repérage | finding | A speaking-time ribbon across the whole three hours doubles as the navigation; a rail of participants filters the transcript to one voice; the text is a dense log. Player reduced to a small panel. |

The other two pages have one shape each, on purpose — the design question the ticket
raises is the transcript page, and they are here so the transcript page can be judged with
something around it:

- `/candidats/<id>` — a Candidate profile. Nothing editorial: no biography, no photo, no
  summary of positions. Their Appearances and their longest recorded Segments, that's all.
- `/recherche` — search over every Segment, client-side. What matters here is what a
  *result* is: a Segment, attributed, timestamped, carrying its review state, linking to
  the exact spot in the transcript.

## Where the data comes from

`scripts/build-data.mjs` converts the transcription prototype's output into the ADR 0005
file layout, and `data/` holds the result (committed). The site reads only those files, so
what you see is the data model being exercised, not a mock.

To regenerate, fetch the two inputs from the pipeline branch first:

```sh
git show origin/claude/issue-13-1a8681:prototypes/transcription/out/transcript.json \
  > scripts/input-transcript.json
git show origin/claude/issue-13-1a8681:prototypes/transcription/out/sample/attribution-check.txt \
  > scripts/input-attribution-check.txt
npm run data
```

The converter is not the importer. Writing the real one is the bridge ticket (#15).

### Liberties taken, so nothing here is mistaken for fact

- **Almost everything is a draft, and that is real.** The only human review that exists is
  the attribution check of ticket #13 (Segments 992–1024), so 34 Segments have a verified
  speaker and every other status is `draft`. The page had to look right in that state,
  which is the state every Appearance is in the day it is imported.
- **One correction is applied**, the one `docs/data-model.md` itself predicts: `s1092`
  ("C") was cut off Marine Tondelier's turn by boundary slop, the attribution check says it
  is hers, so it is re-attributed and merged into `s1093`. Lower id survives, `s1093` is
  retired. That is the only Segment with verified text, and it is what makes the
  retired-id redirect testable (`…#s1093` lands on `#s1092`).
- **Speaker colours** are the prototype's invention. Nothing in the data model gives a
  Speaker a colour; whether the site colours voices at all is a spec question.
- Registry entries for the questioners and the candidacy fields were filled from
  `data/catalogue/seed.md`, read on 2026-09-05.
- **Sorting by surname is a guess.** ADR 0005 stores only a display `name`, so
  `surnameKey()` in `src/lib/data.js` derives the surname with a particle list and treats
  a non-person (a voice-over, an unnamed questioner's label) as having none. A real site
  should store the sort key instead of deriving it.
