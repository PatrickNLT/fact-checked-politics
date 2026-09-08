# Check-worthiness probe (issue #37)

**Throwaway.** Answers one question: can the check-worthy factual claims in a French televised
debate be identified well enough to seed a human review queue, and how many are there in one
debate? The verdict it must reach is **triage aid** (a human reads a ranked shortlist) or
**full manual read** (a human reads every Segment anyway) — those imply very different v3
efforts, and that difference is what the go/no-go gate (#29) needs. Not the production
pipeline; the validated decisions go to `docs/research/claim-identification-prototype.md`
and this code stays on this branch.

Non-goal: verifying any claim. That is #38.

## Get the input

The transcript is the output of the transcription prototype (#13), on its own throwaway branch:

```bash
mkdir -p input
git show origin/claude/issue-13-1a8681:prototypes/transcription/out/transcript.json > input/transcript.json
```

It is not copied into this branch (3.4 MB, and #13 already keeps it as a primary source).

## Run

```bash
uv run probe.py sample                 # seeded uniform draw of 250 Segments + the labelling page
open out/gold/round1.html              # Patrick labels; Export writes labels-round1.json

uv run probe.py detect --arm rules     # free, no API, the lexical floor
uv run probe.py detect --arm haiku     # ANTHROPIC_API_KEY, or `ant auth login`
uv run probe.py detect --arm sonnet
uv run probe.py detect --arm opus
uv run probe.py detect --arm local --model <id> --base-url http://localhost:1234/v1

uv run probe.py score --gold out/gold/labels-round1.json
```

Then round 2, once the best arm is known — this is the one that answers the triage question:

```bash
uv run probe.py shortlist --arm sonnet --k 100   # top-100, shuffled, no scores shown
open out/gold/round2-sonnet.html
uv run probe.py score --gold out/gold/labels-round1.json out/gold/labels-round2-sonnet.json
```

`volume --arm X` prints one arm's distributions without needing any labels.

## Why it is shaped like this

- **The sample is drawn before any model runs**, uniformly over all 1 607 Segments, seeded
  (`SEED`/`ROUND1_N` in `probe.py`). Uniform and unfiltered is what makes the prevalence
  honest, and prevalence times 1 607 is the volume number that sizes the v3 queue — a number
  that is in no published source. Two-word interjections stay in; they cost one keystroke.
- **The labelling is blind and the gold set is shared.** Patrick's judgements are the only
  expensive input and they are model-agnostic, so one labelling session scores every arm, and
  an arm added later costs no extra human time. That is the whole reason to benchmark rather
  than pick a model up front.
- **Three-way labels** (`oui` / `limite` / `non`), scored twice: strict counts `limite` as no,
  lenient as yes. Annotators of the English CheckThat! 2023 set agreed only at Cohen's kappa
  0.49 (`docs/research/evidence-base.md` section E), so a single binary number would be
  false precision. The gap between strict and lenient is the honest width of the answer.
- **Round 2 exists because F1 is not the question.** Round 1 is uniform, so barely a sixth of
  any top-100 falls in it — too thin for precision@k, which is exactly what "does a human read
  a ranked shortlist" means. Round 2 labels the shortlist itself, shuffled and stripped of
  scores. ClaimBuster reached P@100 0.96 on English US debates; that is the comparison.
- **`rules` is the floor, not filler.** CheckThat! 2024's official baseline scored F1 0.307,
  and QuanTemp's finding is that political claims are numerical. An LLM arm that cannot beat
  a regex for digits and years is not buying anything.
- **Character offsets are measured, not assumed.** `docs/data-model.md` says v3 Statements
  attach to a Segment id and character offsets into the Segment text, never to word times. A
  model cannot count characters, so it returns a verbatim span and `locate()` finds it;
  `score` reports the exact / normalised / lost split. How often that works is a finding about
  the record shape, which is measurement 4 of the issue.
- **The guideline is one file, read by both sides.** `guideline.md` goes into the labelling
  page and into every model's system prompt, so the human and the machines are answering the
  same question. A run is only comparable with runs made against the same `guideline_sha`.

## Files

| Path | What |
|---|---|
| `probe.py` | the whole probe: `sample`, `page`, `detect`, `shortlist`, `score`, `volume` |
| `guideline.md` | the definition of check-worthy, shared by annotator and models |
| `calibration.json` | seven worked examples shown before labelling; never scored |
| `labeller.template.html` | the labelling page; `sample` bakes the data into a copy |
| `out/gold/round1.json` | the drawn sample (committed — it is the experiment's design) |
| `out/gold/round1.html` | the double-clickable labelling page (committed) |
| `out/detect/<arm>.json` | one arm's full pass: Statements, tokens, cost, wall-clock |
| `out/findings.json` | what `score` computes; the prose reading of it is in `docs/research/` |

Labels export as `labels-<sample>.json` — **commit them**, they are the primary source.
