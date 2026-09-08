# What counts as check-worthy (annotation guideline, issue #37)

The same words are read to Patrick in the labelling page and to every model in the detector's
system prompt. Changing this file changes both, so a run is only comparable with runs made
against the same version of it.

A **Statement** is a checkable factual claim (`CONTEXT.md`). A Segment is **check-worthy**
(`oui`) when it contains at least one span that is all three of:

1. **Asserted as fact** — presented as how the world is or was, not as a preference, a value,
   an intention or a proposal.
2. **Checkable in principle** — someone could settle it against a public source: a statistic,
   an official record, a published text, a dated event, or something a named person is on
   record as having said or done. It does not have to be easy, only possible.
3. **Worth the queue's time** — a reader who took it at face value would be misled if it were
   false. Trivia nobody would act on does not qualify.

**Not check-worthy** (`non`):

- Questions, including rhetorical ones, and the presenter's turn-taking ("allez-y", "je termine").
- Opinions and value judgements: "c'est une mauvaise politique", "je trouve ça scandaleux".
- Promises, intentions and programme: "je baisserai les impôts", "nous ferons".
- Pure exhortation, greetings, applause, interjections.
- Speech that carries no assertion at all because the Segment is a fragment cut mid-phrase.

**Borderline** (`limite`) — use it, do not force a decision:

- Factual in form but too vague to check: "beaucoup d'entrepreneurs nous disent que…",
  "tout le monde sait que…".
- A prediction resting on a factual base: "avec cette réforme le déficit atteindra 6 %".
- A claim whose truth turns entirely on a definition ("la France est le pays le plus taxé"
  — on which measure?).
- A factual claim so widely agreed that checking it is pointless, yet it is a claim.

The `limite` band exists because the label is soft: annotators of the English CheckThat! 2023
set agreed only at Cohen's kappa 0.49 (`docs/research/evidence-base.md` section E). Scoring
reports F1 twice — **strict** (`limite` counted as `non`) and **lenient** (`limite` counted as
`oui`) — and the gap between the two is the honest width of the answer.

## Claim kind, for a check-worthy Segment

One kind per Segment, the dominant one:

| Kind | French cue | Example |
|---|---|---|
| `numerical` | a figure about the past or the present: a share, a rate, a count, a sum, a ranking | "la dette dépasse 3 300 milliards d'euros" |
| `historical` | a dated past event or decision where no figure is the point | "en 2017 nous avons supprimé l'ISF" |
| `attributive` | what a named person or body said, did, voted or wrote | "vous avez voté contre ce texte au Parlement européen" |
| `predictive` | a claim about the future, figure or no figure | "cette mesure coûtera 9 milliards en année pleine" |
| `other` | a checkable factual claim that is none of the above | |

**Pick the kind on what a checker would go and verify**, not on which words appear. A costed
future measure is `predictive` even though it has a number in it, because the costing is what
gets checked; a dated figure about the past is `numerical`, not `historical`, because the figure
is what gets checked. (QuanTemp and CheckThat! 2025 Task 3 both treat numbers as the hard
class, and French debates are full of them, so the numerical share is worth reading closely.)

## Context

Each Segment is judged **with its neighbours visible** — the Segment before and the Segment
after — because a v3 human queue would have them too, and diarization cuts mid-sentence often
enough (`docs/research/transcription-prototype.md`) that judging a bare Segment would measure
the transcript's segmentation rather than the claim. The judgement is about the **target
Segment's own words**: a claim that lives entirely in a neighbour does not make the target
check-worthy.

## The transcript is draft

Text outside the five-minute corrected window is machine output at a measured 1.1 percent WER,
so names and numbers are sometimes wrong ("Marie-Tourdelier", "CPN" for "CPAM"). Judge whether
the Segment **carries a checkable claim**, not whether the transcription of it is correct.
