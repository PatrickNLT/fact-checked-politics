# Identifying check-worthy claims in a French debate transcript: prototype findings (issue #37)

Question answered: can the check-worthy factual claims in a French televised debate be
**identified** well enough to seed a human review queue, and how many are there in one debate?
The answer the go/no-go gate (#29) needs is one of two: identification is a **triage aid** (a
human reads a ranked shortlist) or it collapses into a **full manual read** (a human reads every
Segment anyway). Prototype code, the drawn sample and the labelling page live on branch
`claude/prototype-37-dfwphs` under `prototypes/claim-identification/` (throwaway, not merged;
paths below are relative to that directory). Non-goal: verifying any claim, which is #38.

**Status on 2026-09-07: the probe is built and the experiment is designed, drawn and
pre-registered; the two measurements that need a human and an API key are not yet made.**
Done: the population is characterised, the gold sample of 250 Segments is drawn and its
labelling page is ready to open, the annotation guideline is written, the zero-cost lexical
floor has been run over the whole debate, and the decision rule is fixed below before any
result exists. Pending: Patrick's blind labelling of round 1, the four model arms, round 2 on
the ranked shortlist, and therefore every precision, recall, kappa and volume figure.

## Setup

| Item | Value |
|---|---|
| Appearance | D1, MEDEF debate of 2026-08-27 on LCI, seven Candidates, 3 h 04 |
| Input | `out/transcript.json` of the transcription prototype (#13), branch `claude/issue-13-1a8681` |
| Text quality | `draft` throughout, at a measured 1.1 percent WER on the one corrected five-minute window (#13) |
| Unit | the Segment, as `CONTEXT.md` defines it, judged with its immediate neighbours visible |
| Gold set | 250 Segments, uniform without replacement over all 1 607, seed 20260907, drawn before any model ran |
| Annotator | Patrick, blind: no machine output appears anywhere on the labelling page |
| Label | three-way `oui` / `limite` / `non`, plus a claim kind for the positives |
| Arms | `rules` (regex floor), Haiku 4.5, Sonnet 5, Opus 5, and one open-weights model on the Mac |
| Compared against | `docs/research/evidence-base.md` section E |

## What is already known

### The transcript holds 1 607 Segments, not 1 470

Issue #37 and `docs/research/transcription-prototype.md` both say 1 470 Segments. The file
itself holds **1 607** (ids `s0` to `s1606`, none retired), which is also what
`docs/data-model.md` records as `segments.next_id`. The word count in the same sentence, 35 468,
is right. The 1 470 looks like a figure taken before the gap-repair step added its Segments and
never updated; the two documents should be corrected. Everything below uses 1 607, so the
volume estimate is a share of the real population.

The shape of that population matters for what the queue costs: 32 percent of Segments are
under eight words and 12 percent are under three, because diarization cuts on speaker change
(#13). A fifth of the debate is "allez-y" and "Non," — cheap to label, cheap to skip, but they
are in the denominator, so a prevalence measured on a filtered sample would overstate the
queue by a lot. This is why the draw is unfiltered.

### The lexical floor flags 22 percent of the debate

`detect --arm rules` — a regex for digits, years, shares, quantities and a short list of
economic nouns — flags **355 of 1 607 Segments (22.1 percent)** and marks 723 spans, at zero
cost in 0.1 seconds. Its per-Speaker rates are already interpretable: Bruno Retailleau 36.5
percent and Marine Le Pen 31.2 percent of their own Segments, against 16.8 for Édouard Philippe
and 9.6 for the presenter. Whatever else it is, this is the number every LLM arm has to beat:
if a model's shortlist is no better than "the Segment contains a number", it has bought
nothing. CheckThat! 2024's official baseline on English debate sentences scored F1 0.307.

### Cost is not going to be the constraint

Estimated from the transcript's ~53 000 tokens of French, 134 batched requests with the
guideline cached: about **$0.45 per three-hour debate on Haiku 4.5, $0.90 on Sonnet 5, $2.24 on
Opus 5**, halved again by the Batch API. Across a seed corpus of every Confrontation of the
campaign this stays in the tens of dollars. The probe records the measured figure, tokens and
wall-clock, and the estimate here is only to say what the decision is *not* about: it is about
quality, which is why the probe runs four arms against one gold set instead of picking a model
up front.

## Method

### Two rounds, because F1 is not the question

Round 1 is a uniform seeded draw of 250 Segments. Uniform is what makes the **prevalence**
unbiased, and prevalence times 1 607 is the volume number that sizes the v3 queue — the number
the issue notes is in no published source. It also gives precision, recall, F1 and Cohen's
kappa against each arm's binary flag.

Round 1 cannot answer the triage question, though. "A human reads a ranked shortlist" is
**precision@k**, and a uniform 250 of 1 607 covers only about a sixth of any top-100 — a dozen
or so labelled items, far too thin. So round 2 labels the shortlist itself: the top 100 of the
best arm's ranking, shuffled and stripped of every score, in the same blind page. ClaimBuster
reported P@100 = 0.96 on English US debates while its full-sentence classification sat at
precision 0.72 / recall 0.67; that gap between ranking and classification is the entire reason
the two rounds are separate, and it is what section E means by "ranking the top claims is easy;
classifying all sentences is not".

### One guideline, read by both sides

`guideline.md` defines check-worthy as a span that is asserted as fact, checkable in principle
against a public source, and consequential if false. It is rendered into the labelling page and
interpolated into every model's system prompt, so the human and the machines answer the same
question; each run records the guideline's hash, and runs against different hashes are not
comparable. Seven worked examples drawn from this debate (`calibration.json`) are shown before
labelling starts and are excluded from both samples.

### The label is soft, and the scoring says so

Section E's binding caveat is that annotators of the English CheckThat! 2023 test set agreed at
Cohen's kappa **0.49** — moderate — and that the Spanish set, the only one annotated by
professional fact-checkers, was consistently the hardest. Reporting one binary F1 against a
single annotator would be false precision. So the label is three-way and every figure is
reported twice: **strict** counts `limite` as not check-worthy, **lenient** counts it as
check-worthy. The gap between the two is the honest width of the answer, and the kappa between
Patrick and each machine is directly comparable to that published 0.49.

One annotator remains the design's real limit. It measures agreement between Patrick and a
model, not the reliability of the label itself; separating "the model is wrong" from "the label
is soft" needs a second annotator, which is part of the ≥1 000-sentence, two-annotator,
published-kappa setup section E sets as the minimum credible **v3** benchmark. This probe is
deliberately smaller: a feasibility read, not that benchmark.

### The arms

| Arm | Model | Why it is in |
|---|---|---|
| `rules` | — | the zero-cost floor; what an LLM has to beat to be worth anything |
| `haiku` | `claude-haiku-4-5` | the cost floor; if it holds up, v3 is affordable at corpus scale |
| `sonnet` | `claude-sonnet-5` | the likely production choice |
| `opus` | `claude-opus-5` | the ceiling; how much headroom a better model buys |
| `local` | an open-weights model on the Mac | answers the issue's "locally or hosted" directly |

Each arm returns, per Segment, a boolean, a graded confidence (which is what the ranking uses)
and the verbatim spans it would hand a checker. The gold set is shared, so an arm added later
costs no further human time — the reason to benchmark rather than choose in advance.

### The record shape (measurement 4)

`docs/data-model.md` says v3 Statements attach to a Segment id and character offsets into the
Segment text, never to word times. A model cannot count characters, so each arm returns a span
copied verbatim and the probe locates it: exact match first, then an accent- and
punctuation-folded match that maps back to original offsets. `score` reports the
exact / normalised / lost split, which is the finding: whether "Segment id plus character
offsets" is a shape a model can actually be made to fill. The emitted record is
`{segment, start, end, text, kind, located}` per claim, under a Segment id in the `s1093` form
the data model uses — enough to confirm the v1 model does not preclude v3, which is all the
issue asks; the v3 attachment files themselves stay undesigned.

## The decision rule, fixed before the results exist

Written now so the verdict cannot be argued backwards from whatever the numbers turn out to be.
On the best arm whose cost is acceptable, judged on round 2 for precision and round 1 for
recall, at the threshold that maximises F1:

- **Triage aid** — precision@100 at least 0.60 lenient **and** recall at least 0.70 lenient. A
  human reading a ranked hundred finds mostly real claims and is not missing most of the debate.
- **Full manual read** — precision@100 below 0.40 **or** recall below 0.50. The shortlist is
  not worth reading in preference to the transcript, and v3's identification layer has to be
  the fine-tuned French setup section E describes, or a human pass.
- **Between the two** — a triage aid with a stated caveat: usable to order a human's reading,
  not to bound it. Say which of precision or recall is the binding constraint, because they
  imply different fixes.

Section E's expectation for French is F1 nearer 0.6–0.7 than 0.9, so the middle band is the
likely outcome and the interesting question is which side of it the numbers land.

## What is left

1. Patrick labels round 1 (250 Segments) in `out/gold/round1.html` and commits the export.
2. Run the four arms; run `local` on the Mac to settle the hosted-or-local question.
3. `shortlist` the best arm, label round 2 (100 Segments), score both rounds.
4. Fill in the numbers above, state the verdict against the rule, and hand it to #29.
5. Correct the 1 470 Segment count in issue #37 and in `docs/research/transcription-prototype.md`.
