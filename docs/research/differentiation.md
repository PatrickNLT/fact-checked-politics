# Differentiation: what this project has that observatoire2027.fr and larroumec.fr do not, and whether licensing takes it away

**Status:** analysis note, 2026-09-07. **Not legal advice.** Written in answer to a question Patrick asked directly: several 2027 projects already exist and look decent, so is the full transcript a real differentiator, or only an artefact of not having checked the licensing yet?

Two kinds of statement are mixed below and are marked as such: **checked** facts (read from a primary source, or from an existing file in this repository, on the date given) and **judgement** (an argument from those facts, which is contestable). Nothing here is a decision; decisions go in `docs/adr/`.

The two comparators were re-read on **2026-09-07**. The wider landscape is not re-surveyed here: `docs/research/prior-art.md` (2026-09-05) covers the other comparators, the reusable building blocks and the international precedents, and this note does not repeat it.

---

## 1. The licensing question is already settled, and it does not remove the full transcript

**Checked** (`docs/research/legal-france.md`, `docs/research/vie-publique.md`, ADR 0002, ADR 0003):

- The broadcaster's neighbouring right (CPI L.216-1) covers **the programme and its signal**, not a text derived from it. A transcript does not engage it. This is why "never host media, embed or deep-link only" turns the one red light in the traffic-light table into the CJEU linking case (Svensson, BestWater, VG Bild-Kunst).
- What a verbatim transcript does engage is the **speaker's own copyright** on improvised words, where original (L.112-1, L.112-2 2°, reproduction under L.122-3), and marginally the journalist's in their questions.
- The political-speech exception (L.122-5 3° c) fits a rally speech **while it is news**. It does not fit a studio debate or a one-to-one interview, and it does not cover a permanent archive.
- Against that: DILA has published full verbatim transcripts of ministers' BFMTV/RTL/France Inter interviews on vie-publique.fr for twenty years, journalists' questions included, and did so for opposition candidates in 2002–2004, with no licence from broadcasters or speakers and no recorded challenge.
- Section 9.4 of the legal file states the limit of that precedent: it is evidence that transcript *text* is treated in practice as public information, not evidence that a private archive of candidates' full transcripts is lawful. Hence the standing amber.

**Judgement.** The premise of the question — "maybe I won't be able to expose the full transcript" — does not survive the file. There is no licence to be refused and no gate to fail: nobody grants permission for this and nobody has to. What exists is a risk carried personally, as *directeur de la publication* (loi 82-652 art. 93-2), against which ADR 0002 sets attribution, a takedown channel, a corrections log, a published method, media never hosted, and machine text labelled until verified. The realistic failure mode is a notice, not an injunction, and section 9.4 expects the first notices to concern the *labels* (v3/v4 verdicts and tags) rather than copyright.

**Judgement, and the sharper point.** The legal exposure and the differentiator are **the same object, not two things to be traded off**. ADR 0002 publishes the full text because the data files are public in the repository anyway, so any display that hides it is theatre. The corollary runs backwards too: retreating from full text would also mean closing the repository, which removes the open corpus, the public diffs and the auditable corrections — that is, items 1 to 3 of section 3 below. There is no configuration that keeps the differentiator and drops the risk. The intermediate posture (segments shown only when attached to a note) was considered and rejected in ADR 0002, and its rejection reasons still hold: v1 has no analysis to attach to.

**Checked, and worth separating.** The weaker legal point is not publication but **acquisition**: downloading the working copy from Sources that have opted out of text-and-data mining (`docs/research/source-terms.md`; every large French broadcaster except Public Sénat and LCP). ADR 0003 records that exposure as contractual — a platform download clause, or terms never accepted — rather than as a copyright claim, and notes that the step is invisible to the Source. It also keeps two fallbacks that need no download at all (stream capture, transcripts typed by ear), so a Source's objection degrades throughput rather than stopping the corpus.

---

## 2. What the two named comparators actually do

Read on 2026-09-07.

| | observatoire2027.fr | larroumec.fr |
|---|---|---|
| Scope | 16 candidates, 33 subjects, **4,766** sourced position "relevés" (3,796 on 2026-09-03 per `prior-art.md`, so roughly a thousand added in four days) | One Appearance: the MEDEF/LCI debate of 2026-08-27, 7 candidates, 3 h 07 |
| Method | Manual sourcing; "chaque entrée renvoie à une citation et sa source"; left-right placement by "estimations analytiques" | Whisper large-v3-turbo transcription, speaker attribution by voice fingerprint (ECAPA-TDNN), 80 claims checked against INSEE, COR, Eurostat, Sénat, Cour des comptes, RTE |
| Verbatim anchoring | Positions cite a source; none is tied to a timestamp in a recording | Every statistic, quotation and claim carries a horodatage into the LCI YouTube replay |
| Full transcript published | No | **No.** A full transcript was produced and is not exposed: the site points to the replay ("l'intégralité du débat est disponible sur le replay officiel LCI") and states "en cas de doute sur une citation, l'enregistrement original fait foi" |
| Open data / code / licence | None found; licence unstated; no API | None found; licence unstated |
| Operator | Not named on the site | Not named on the site |
| Cadence | Continuously updated | "Verdicts et statistiques figés au 28 août 2026" |
| Community correction | Error reports only (per `prior-art.md`) | None |

**Judgement.** The most useful fact here is that larroumec **built** the full transcript and **chose not to publish it**. That splits the assumed differentiator in two: producing a transcript is not the scarce thing — the prototype (`docs/research/transcription-prototype.md`) measures 14 minutes of machine time per audio hour on free open weights, and larroumec did the same debate in a weekend — whereas *publishing* it, standing behind it, and letting anyone correct it is what nobody has done.

**Judgement.** The two sites show two different ways this class of project fails, and both are worth naming as things to design against: larroumec is thorough and frozen (one burst, no data, no continuation); observatoire2027 is sustained and unauditable (no named operator, no licence, no open data, no way to check a "relevé" against the moment it came from). Neither failure mode is an accident of effort; each follows from a structural choice this project has already made differently.

---

## 3. Where the differentiation actually sits

Ranked by how well each holds up against a competent imitator. All **judgement**, argued from the files cited.

1. **An open, correctable, citable corpus with permanent per-Segment ids.** This, rather than "full transcripts", is the asset. Full text is a display choice; the durable thing is ADR 0005's per-Appearance id counter that is never renumbered or reused, the file-based model a non-developer can edit, the Licence Ouverte 2.0 on everything Patrick authors (ADR 0002), and corrections as pull requests (ADR 0001). It compounds with every import and it cannot be retrofitted: a competitor starting in 2027 cannot manufacture a citable history of the 2026 debates.
2. **Verifiability.** A published word error rate, a `draft`/`verified` status per Segment on text and on attribution, a public corrections log, and a *mechanical* seed rule (ADR 0004: every Confrontation since 27 August 2026, no per-person quota, no editorial pick). Neither comparator can be audited at all. This holds up because it does not depend on being first — but it is rewarded by journalists and researchers, rarely by readers.
3. **Being substrate rather than product.** Observatoire 2027, MonVote2027 and Droit à l'Info can consume this project's Segment ids and timestamps; none of them can be consumed in return, because none publishes data. This is what makes "why work on it" answerable even if traffic is small, and it is the realistic route to partnership rather than competition (`prior-art.md`, gaps and reuse map).
4. **Positions and claims anchored to an exact verbatim moment** (v2, v3). `prior-art.md` found none of the eight live 2027 comparators linking a position to a verbatim timestamp. Genuinely open ground, but it only becomes real once item 1 exists at scale — it is a consequence of the corpus, not an independent bet.
5. **The rhetoric layer** (v4). `prior-art.md` found no deployed French product anywhere, only research assets (SemEval-2023 Task 3, MAFALDA, DISPUTool 3.0). First-of-a-kind, and also the most legally exposed (`legal-france.md` section 4.4 on per-person aggregates), the most attackable as partisan, and the furthest away in time.

### Not differentiators

- **Fact-checking itself.** Eight-plus French outlets are active and better resourced (`prior-art.md`, area 1); a ninth verdict on the same claim adds nothing. The gap named in that file is a *structured, open, per-utterance* claim registry, which is item 4, not fact-checking.
- **Using ASR or LLMs.** Commodity, and larroumec is the proof for this exact debate.
- **Publishing the source code.** Nobody reads a site because of its repository. The repository matters as the correction and audit mechanism (items 1 and 2), not as a claim in itself.
- **Claiming non-partisanship.** Every comparator claims it. What differs is that ADR 0004 makes it checkable by a rule over a class of Appearances rather than by assertion — and ADR 0004's 2026-09-07 amendment deliberately removed the per-Candidate counts that would have looked like proof.

---

## 4. What cuts against all of it

**Checked.** The transcription is not the bottleneck: 14 minutes per audio hour, 1.1 percent measured WER (0.5 percent net of spelling conventions), both models open-weight and free. But the same file concludes the output is **not good enough to publish uncorrected**, for two named defects — silent ASR drops and misattribution in cross-talk (about 2 percent of sample words after the current merge rule, inside the 2.5 percent flagged as overlap). Correction is human time, per Appearance, and it is the real unit cost of the corpus.

**Checked.** The seed catalogue (2026-09-06) holds 2 core multi-candidate debates and 2 borderline ones since 27 August 2026, plus 3 announced. The corpus grows with the campaign, not with effort.

**Checked.** ADR 0002 stops imports after the second round; the site then stays online as an archive with corrections open.

**Judgement.** Three consequences. The differentiator is *operational*, not technical: it is sustained correction plus a risk position, both of which a well-staffed newsroom could copy in a month if it wanted to — the reason none has is a risk appetite, not a capability gap. The single point of failure is one person who is criminally answerable as *directeur de la publication* and has decided not to consult a lawyer (`legal-france.md`, recommended risk posture). And the archive has a natural shelf life of roughly eighteen months unless item 3 comes true and something else is built on it.

---

## 5. The question this note does not answer

**Judgement.** Whether the project is differentiated is settled above: it is, on items 1 to 4, and `prior-art.md` finds nothing in France occupying that ground. The open question is a different one, and it decides how much of the plan matters:

> Who is measurably worse off if this does not exist?

If the answer is *journalists, researchers and other 2027 tools, who today cannot cite what a candidate said at a precise second and cannot check anyone's citation against a corpus* — then items 1 to 3 are the project, item 4 is the payoff, and reader traffic is not the measure of success. If the answer is *readers*, the comparators already serve them, and this is a slower product entering a crowded field.

The two answers imply different launch checklists, different success measures and a different attitude to the risk in section 1. `docs/launch-checklist.md` currently assumes neither.

---

## Sources

Internal (this repository):

- `docs/research/legal-france.md` — sections 1, 2, 4, 9 and the traffic-light table and risk posture
- `docs/research/vie-publique.md` — DILA's twenty-year practice
- `docs/research/source-terms.md` — TDM opt-outs per broadcaster
- `docs/research/prior-art.md` (2026-09-05) — the wider comparator landscape
- `docs/research/transcription-prototype.md` — wall-clock, WER, defects, verdict
- `data/catalogue/seed.md` (2026-09-06) — corpus size
- ADR 0001, 0002, 0003, 0004, 0005

External, read 2026-09-07:

- https://observatoire2027.fr/
- https://www.larroumec.fr/
