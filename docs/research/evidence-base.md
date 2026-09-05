# Evidence base for a French 2027 fact-checking and rhetoric-analysis platform

Research memo, 2026-09-05.
Scope: what peer-reviewed and shared-task literature actually establishes for each layer of the planned platform (v1 transcripts, v2 themes, v3 claim extraction and rating, v4 fallacy / technique tagging, live layer).
Every number below was read at the source (PDF or publisher page) unless marked **UNVERIFIED**. Effect sizes are Cohen's *d* unless stated. "F1" means macro-F1 unless stated.

## Executive summary (what is proven, promising, unsupported)

1. **Proven (v3, corrections work on beliefs):** Fact-checks reliably move factual beliefs in the right direction. Meta-analysis of 30 studies (N = 20,963) gives *d* = 0.29 (Walter et al. 2020); cross-national replications in 4 countries / 22 fact-checks find effects that survive two-plus weeks (Porter & Wood 2021). This holds in France: 2,480 voters exposed to Le Pen's refugee-crisis claims updated their knowledge after fact-checks (Barrera et al. 2020).
2. **Proven (v3, no backfire):** The "backfire effect" (Nyhan & Reifler 2010) has not replicated at scale: 5 experiments, 10,100+ subjects, 52 issues, zero backfires (Wood & Porter 2019); measurement reviews conclude it is not a robust phenomenon (Swire-Thompson et al. 2020; Nyhan 2021 PNAS). Corrections may safely target any partisan group.
3. **Proven but sobering (v3, votes):** Corrections change what people believe, not whom they support. No measurable effect on Trump favourability (Nyhan et al. 2020) or on Le Pen support (Barrera et al. 2020, where fact-checks even raised immigration salience). Belief gains also decay within weeks (Carey et al. 2022).
4. **Format matters (v3):** Truth-scale ("truth-o-meter") formats weaken correction effects on average (Walter 2020) although one experiment found they help in some conditions without partisan backlash (Amazeen et al. 2018); "half-true"-type ratings produce no effect in debates (Wintersieck 2017); professional fact-checkers themselves disagree most in the middle of the scale (Lim 2018). Prefer detailed textual corrections over a scalar verdict.
5. **Promising, thin (politician deterrence):** One field experiment (1,169 US state legislators) cut negative ratings/accuracy criticism from 2.8% to 1.3% (Nyhan & Reifler 2015). A 2023 conceptual replication found only "limited evidence" (Ma et al. 2023). An Italian RCT with Pagella Politica (55 MPs) found fewer incorrect statements but substitution toward unverifiable statements (Mattozzi et al., working paper). Deterrence is plausible, not established, and can produce evasiveness rather than accuracy.
6. **Promising, contested (v4 education / inoculation):** Technique-based prebunking videos raise technique recognition (*d* 0.28-0.68 in RCTs; a 5% gain, *h* = 0.09, on YouTube at scale) (Roozenbeek et al. 2022). But signal-detection reanalyses show the games mainly make people more sceptical of everything (response bias), not better at discriminating (Modirrousta-Galian & Higham 2023; Graham et al. 2023; Seabrooke et al. 2025), while a 2025 SDT meta-analysis of 33 experiments claims genuine discrimination gains. Effects decay within ~2 months without boosters (Maertens et al. 2021) and largely vanish in realistic social-media feeds (Wang et al. 2025). No study tests transfer to real political speech.
7. **Unsupported so far (live layer):** No randomised study of on-screen live corrections during a real televised debate with trust outcomes was found. The one lab experiment (N = 574) shows real-time corrections beat delayed ones overall (+5.2 vs +3.3 accuracy points) but work less well on people predisposed to believe the claim (Garrett & Weeks 2013). Duke's automated live system (Squash) produced 20 pop-ups in a State of the Union of which 6 were "in the ballpark"; it required a human editor.
8. **Achievable now (v3 claim detection):** Check-worthiness detection on US debate sentences reaches F1 ~0.80-0.90 (positive class) in CheckThat! 2023-2024, with the 2024 winner a fine-tuned Llama-2-7B. Human agreement on check-worthiness is only moderate (Cohen's kappa 0.49). No French check-worthiness benchmark exists; expect a drop on French transcripts.
9. **Not achievable unsupervised (v3 verification):** Open-domain verification of real-world claims scores 63% (AVeriTeC 2024, lenient metric) and 33% (AVeriTeC 2025, strict evidence metric). Numerical claims are the worst case: best macro-F1 59.5 on English at CheckThat! 2025 (baseline 58.3), 50.3 on Spanish. LLMs without retrieval fabricate sources (55% of GPT-3.5 and 18% of GPT-4 citations fabricated, Walters & Wilder 2023).
10. **Partly achievable (v4 fallacy tagging):** On US presidential debates, coarse 6-class fallacy classification reaches F1 0.84 with gold argument-structure features (Goffredo et al. 2022) and 0.72-0.86 with argument-guided retrieval (Dore et al. 2026); the 2025 shared task on the same data scored only 0.44 text-only; fine-grained (14 subclasses) collapses to 0.42 with several classes at F1 0.00.
11. **Human ceiling is low (v4):** Krippendorff's alpha between trained annotators on debate fallacies is 0.46-0.60 per type (moderate) (Goffredo 2022); propaganda-technique spans start at gamma 0.30-0.34 before adjudication (Da San Martino 2019); multilingual persuasion techniques alpha 0.34 (SemEval-2023); on MAFALDA humans score F1 0.19 at fine granularity and agree with each other even less. Any "fallacy score" reported to the public would be measuring annotation noise as much as rhetoric.
12. **Which fallacies are detectable:** lexically marked ones (loaded language F1 0.83, slogans 0.68, flag-waving 0.65, ad hominem 0.79, ad populum 0.79) work; inferential ones do not (false authority 0.00, tu quoque 0.00, false cause 0.27, slippery slope 0.32, deductive fallacy 0.26). Zero-shot GPT-4 on debates: F1 ~0.42 (5 classes).
13. **Transcription (v1):** French read/clean speech WER is 3-6% for the best models (Voxtral Small 4.03, Scribe 5.07, Whisper-large-v3 5.55 on FLEURS; Canary-1B-v2 3.36 on MLS). Common Voice French is 6-11%. Broadcast debates with overlap will be worse; published French TV diarization is DER 7.8% (pyannote 3.1 on REPERE) and overlapping speech reaches 10.4% of debate time (ETAPE). Whisper hallucinates whole phrases in ~1% of segments.
14. **Consequence for verbatim quotation:** at 5% WER a 30-word quote has a ~78% chance of containing at least one error. Automatic transcripts are fine for search (v1) but every quoted or rated span must be human-verified against the audio.
15. **Design bottom line:** treat AI as a pre-annotator feeding a human review queue; publish inter-rater agreement and model error rates; show technique explanations rather than counts or scores per candidate; expect belief effects, not vote effects; do not promise real-time verdicts.

---

## A. Effects of fact-checking on citizens' beliefs

| Study | Year | Venue | Design & sample | Key result | Replication status | Implication |
|---|---|---|---|---|---|---|
| Walter, Cohen, Holbert & Morag, "Fact-checking: a meta-analysis of what works and for whom" | 2020 | Political Communication 37(3) | Meta-analysis, k = 30, N = 20,963 | Overall *d* = 0.29 on political beliefs; weaker with truth scales, partial refutations, campaign-related statements; attenuated by prior beliefs, ideology, knowledge | Synthesis of the field; consistent with later cross-national RCTs | Expect small-to-moderate belief effects; avoid scale-only verdicts |
| Chan, Jones, Hall Jamieson & Albarracin, "Debunking" | 2017 | Psychological Science 28(11) | Meta-analysis, k = 52, N = 6,878 | Debunking *d* = 1.14-1.33; persistence of misinformation after debunking *d* = 0.75-1.06; detailed debunking helps; audience counter-arguing hurts | Effect sizes are unusually large versus later work (Walter 2020); interpret magnitudes cautiously | Give detailed, explanatory corrections, not bare labels |
| Nyhan & Reifler, "When corrections fail" | 2010 | Political Behavior 32 | Lab experiments on undergraduates (mock news articles; Iraq WMD etc.) | Corrections often failed among targeted ideological groups; a "backfire" among conservatives on WMD | Failed to replicate at scale (below) | Do not design around backfire |
| Wood & Porter, "The elusive backfire effect" | 2019 | Political Behavior 41 | 5 experiments, >10,100 subjects, 52 issues | No correction produced backfire; citizens "heed factual information" even against ideology | Largest replication attempt; corroborated by Swire-Thompson 2020 and Nyhan 2021 | Corrections can target any group |
| Swire-Thompson, DeGutis & Lazer, "Searching for the backfire effect" | 2020 | J. Applied Research in Memory & Cognition 9 | Review + measurement analysis | Backfire "not a robust empirical phenomenon"; prior findings partly measurement artefacts | Review | Use reliable multi-item belief measures if you evaluate impact |
| Nyhan, "Why the backfire effect does not explain the durability of political misperceptions" | 2021 | PNAS 118(15) | Review | Corrections "typically at least somewhat effective"; gains "often do not last or accumulate", overwhelmed by elite cues | Review | Plan repeated exposure; expect decay |
| Porter & Wood, "The global effectiveness of fact-checking" | 2021 | PNAS 118(37) | Simultaneous RCTs in Argentina, Nigeria, South Africa, UK; 22 fact-checks | Reduced false beliefs in all 4 countries; most effects detectable >2 weeks later; little cross-country variation | Preregistered, multi-site | Effects generalise across political cultures |
| Carey, Guess, Loewen, Merkley, Nyhan, Phillips & Reifler, "The ephemeral effects of fact-checks on COVID-19 misperceptions" | 2022 | Nature Human Behaviour 6 | Preregistered panel survey experiments, US / GB / Canada | Fact-checks reduce targeted misperceptions, most among the most vulnerable; reductions "do not persist over time" even with repeated exposure | Preregistered, 3 countries | One-off corrections fade; the platform is a reference, not a vaccine |
| Nyhan, Porter, Reifler & Wood, "Taking fact-checks literally but not seriously?" | 2020 | Political Behavior 42 | 2 experiments during 2016 campaign (Trump convention speech and debate claims) | Fact-checks improved factual beliefs "even among Trump supporters" but had "no measurable effect on attitudes toward Trump" | Consistent with Barrera 2020 and BJPS 2020-election conceptual replication (**UNVERIFIED** details) | Beliefs move, votes do not |
| Barrera, Guriev, Henry & Zhuravskaya, "Facts, alternative facts, and fact checking in times of post-truth politics" | 2020 | Journal of Public Economics 182 | Randomised online experiment, 2,480 French voters, 2017 presidential campaign, Marine Le Pen refugee statements | (i) alternative facts highly persuasive; (ii) fact-checking improves factual knowledge; (iii) no effect on policy conclusions or candidate support; (iv) facts alone do not reduce support; channel = increased salience of immigration | Single study, but French and directly relevant | A French fact-check can raise the salience of the checked candidate's issue |
| Amazeen, Thorson, Muddiman & Graves, "Rating scale versus contextual correction formats" | 2018 | Journalism & Mass Communication Quarterly 95 | Online experiment, political and consumer misperceptions | Truth scales "more effective in some conditions" and did not increase partisan backlash against correction or source | Contrasts with Walter 2020 meta-analytic moderator | Scales are not harmful, but not clearly superior; the explanation carries the effect |
| Wintersieck, "Debating the truth" | 2017 | American Politics Research 45(2) | Experiment with fact-checks embedded in a debate | Confirming ("true") fact-checks improved evaluation and vote likelihood; "half-true" ratings had no effect | Single study | Ambiguous verdicts do nothing; consider not publishing middle-scale ratings |
| Lim, "Checking how fact-checkers check" | 2018 | Research & Politics 5(3) | Comparison of PolitiFact and Washington Post Fact Checker ratings | Only 1 in 10 statements checked by both; agreement good on clear truths/falsehoods, "much lower" for Half True / Mostly False | Observational | Your own rating scale will have low reliability in the middle; publish reviewer agreement |

Narrative.
The strongest, most replicated finding in this literature is that corrections improve belief accuracy modestly (d about 0.3) and do not backfire; the second strongest is that the improvement decays within weeks and does not translate into changed candidate preference.
The French experiment by Barrera et al. is the closest analogue to the planned platform and warns that fact-checking a populist candidate's numbers can make her issue more salient without reducing her support.
Format evidence is mixed: the meta-analysis finds truth scales dilute effects, while Amazeen et al. find no partisan backlash from them; the safest reading is that the explanation, not the icon, does the work, and that middle-of-scale verdicts ("cherry-picked", "misstated") are both the least reliable among professional fact-checkers (Lim 2018) and the least effective on audiences (Wintersieck 2017).

## B. Effects on politicians

| Study | Year | Venue | Design & sample | Key result | Replication status | Implication |
|---|---|---|---|---|---|---|
| Nyhan & Reifler, "The effect of fact-checking on elites: a field experiment on U.S. state legislators" | 2015 | AJPS 59(3) | Field RCT, 1,169 legislators in 9 states with PolitiFact affiliates, fall 2012; treatment letters on reputational/electoral risk vs placebo ("we are monitoring") vs control | Negative PolitiFact rating: 1.8% (placebo/control) vs 1.0% (treatment); accuracy questioned in Nexis: 1.0% vs 0.3%; combined 2.8% vs 1.3% (one-sided Fisher p < .07; regression p < .05 one-sided); reduction = 44-75% of possible; only 21% of treated returned postcards vs 34% placebo | One conceptual replication with weaker results (next row); base rates very low (0.8-1.6%) | Salient threat of being checked can reduce inaccurate statements, but the evidence is one study with marginal p-values |
| Ma, Bergan, Ahn, Carnahan, Gimby, McGraw & Virtue, "Fact-checking as a deterrent? A conceptual replication" | 2023 | Human Communication Research 49(3) | Field design using a local-media / fact-checker partnership as treatment; accuracy of state legislators' tweets during Trump's first impeachment | "Limited evidence of the effects of our treatment on the accuracy of legislators' posts, even among legislators within media markets directly affected" | Replication of Nyhan & Reifler; null-ish | Deterrence is fragile; do not promise it |
| Mattozzi, Nocito & Sobbrio, "Fact-checking politicians" | 2022 (WP; VoxEU column) | SSRN 4258130; AEA registry 6432 | RCT with Pagella Politica (Italy): 55 MPs (registry: ~50 control, 10 treated, one per week), 16 weeks from March 2021 (3 pre / 10 treatment / 3 post); fact-checks disseminated via social media and geo-targeted ads | Fact-checking "discourages politicians from making factually incorrect statements", effects last several weeks; it "neither increases nor displaces correct statements"; treated politicians substitute incorrect statements with "no statements or unverifiable ones" (**numbers UNVERIFIED**: paper PDF not accessible) | Working paper, not yet peer-reviewed | Expect evasiveness, not just accuracy; track "unverifiable" share as an outcome |
| Ceron & Carrara, "Fact-checking, reputation, and political falsehoods in Italy and the United States" | 2023 | New Media & Society | Observational analysis of fact-checked statements | Falsehoods rise as elections approach (checks arrive too late), are rarer in detailed and scripted statements, and commoner on issues the politician "owns" | Observational | Speed of checking near election day is what creates cost; scripted debate segments will contain fewer checkable falsehoods |
| Lim | 2018 | Research & Politics | see A | Fact-checker disagreement in middle categories | | Politicians can and will contest ambiguous ratings |

Narrative.
The evidence that fact-checking changes politicians' behaviour rests on one 2015 field experiment with small absolute effects and p-values at the .05-.07 boundary, one replication that found little, and one unpublished Italian RCT that found deterrence accompanied by strategic vagueness.
Nothing was found on PolitiFact or Full Fact publishing causal evidence of elite behaviour change; Full Fact's public material describes live fact-checking of PMQs and Question Time but not evaluations of politicians' responses (**UNVERIFIED** absence).
The realistic hope (b) in the brief is therefore that a reference platform raises the perceived probability of being checked quickly; the documented risk is that politicians respond by saying less that is checkable.

## C. Inoculation / prebunking against manipulation techniques

| Study | Year | Venue | Design & sample | Key result | Replication status | Implication |
|---|---|---|---|---|---|---|
| Roozenbeek & van der Linden, "Fake news game confers psychological resistance" (Bad News) | 2019 | Palgrave Communications 5 | Pre-post, N ~ 15,000 self-selected players, no control group; 6 techniques (impersonation, emotion, polarisation, conspiracy, discrediting, trolling) | Fake tweets rated less reliable after play, across age, education, ideology | Followed by controlled studies (Basol 2020, Maertens 2021) and critical reanalyses (below) | Original evidence is weak by design (no control) |
| Basol, Roozenbeek, Berriche, Uenal, McClanahan & van der Linden, "Towards psychological herd immunity" (Go Viral!) | 2021 | Big Data & Society | Two preregistered studies, n = 1,771 and 1,777; English, French, German | Higher perceived manipulativeness of COVID misinformation, higher confidence, lower sharing intention; first two effects held one week | Includes a French sample | The only technique-inoculation evidence with French participants |
| Maertens, Roozenbeek, Basol & van der Linden, "Long-term effectiveness of inoculation against misinformation" | 2021 | J. Experimental Psychology: Applied 27(1) | 3 longitudinal experiments, N = 151 / 194 / 170; Bad News vs Tetris | Effect stable for 3 months with regular testing (Exp 1); "significant decay over a 2-month period" so long-term effect no longer significant without regular testing (Exp 2) | Two preregistered | Educational content needs boosters; a one-time explainer will fade |
| Roozenbeek, van der Linden, Goldberg, Rathje & Lewandowsky, "Psychological inoculation improves resilience against misinformation on social media" | 2022 | Science Advances 8(34) | 6 preregistered RCTs (n = 6,464) + YouTube ad field study (n = 22,632); 5 videos: emotional language, incoherence, false dichotomies, scapegoating, ad hominem | Technique recognition *d* = 0.49 (emotion), 0.62 (incoherence), 0.68 (false dichotomy), 0.28 (scapegoating), 0.45 (ad hominem), 0.67 (emotion replication); trust discernment *d* = 0.10-0.32; sharing discernment 0.10-0.22; YouTube: *h* = 0.09 across items, ~5% recognition gain ~18 h after viewing, US$0.05 per view | Preregistered; field study; effects robust across ideology | Short technique explainers (the v4 idea) measurably raise recognition of the taught technique, with small real-world effect sizes |
| Roozenbeek, Traberg & van der Linden, "Technique-based inoculation against real-world misinformation" | 2022 | Royal Society Open Science 9(5) | Two experiments, n = 2,188 (Bad News players), real viral misinformation posts | Perceived reliability of real misinformation fell, M 2.59 to 2.21, *d* = -0.32 | Convenience sample, pre-post | Some transfer from taught technique to real content; still not political speech |
| Modirrousta-Galian & Higham, "Gamified inoculation interventions do not improve discrimination between true and fake news" | 2023 | J. Experimental Psychology: General 152 | ROC reanalysis of Bad News / Go Viral! data | Games produced "conservative response bias shifts rather than improved discernment" (more "false" responses to everything) | Reanalysis of published data | Teaching techniques may make citizens cynical about all statements, including true ones |
| Graham, Skov, Gilson, Heise, Fallow, Mah & Lindsay, "Mixed news about the Bad News Game" | 2023 | Journal of Cognition | 4 parallel replications, 353 students, Bad News vs Tetris | False-tweet credibility fell (*d* 0.56-1.23) but true-tweet credibility also fell (*d* 0.36-0.58); no discrimination gain, only bias shift | Independent replication | Same warning |
| Seabrooke, Modirrousta-Galian & Higham, "Re-examining the Bad News game" (India) | 2025 | Psychonomic Bulletin & Review | Preregistered, N = 150 Indian participants, ROC analysis | No discrimination improvement (AUC *d*z = 0.04, p = .63); contradicts Iyengar et al. 2023 (*d* = 0.45) | Independent replication | Cross-cultural transfer unproven |
| "A signal detection theory meta-analysis of psychological inoculation" (authors **UNVERIFIED**, van der Linden group likely) | 2025 | Current Opinion in Psychology | Bayesian SDT reanalysis of 33 experiments, N = 37,025 | Gamified and video interventions "consistently improve discrimination ... without increasing response bias" | Directly contradicts the Higham-group reanalyses; dispute unresolved | The field is split on whether inoculation teaches discernment or scepticism |
| Lu, Hu, Li, Bi & Ju, "Psychological inoculation ... systematic review and meta-analysis" | 2023 | JMIR 25 | 42 studies, N = 42,530 | Misinformation credibility *d* = -0.36 [-0.50, -0.23]; discernment *d* = 0.20 [0.13, 0.28]; mostly immediate measurement, mostly US | Methodological concerns published (PMC12428163) | Average effects are small; discernment gain about a fifth of a SD |
| Wang, Phillips, Carley, Lin & Pennycook, "Limited effectiveness of psychological inoculation against misinformation in a social media feed" | 2025 | PNAS Nexus 4(6) | 5 preregistered studies, N = 3,881, simulated feed (Yourfeed), emotional-language video | Minimal/null effects on dwell, likes, shares for real tweets; only in the most artificial synthetic condition did sharing fall (*d* = 0.16) | Independent, preregistered | Recognition in a quiz does not equal changed behaviour in a feed |
| "Deception detection in politics: can voters tell when politicians are lying?" (authors not retrieved) | 2021 | Political Behavior | Experiment: participants watch politicians' speech videos | Success explained by verbal detail and demeanour cues; strong truth bias; female politicians judged more honest | Single study | Unaided citizens are poor lie detectors; there is headroom for training, but no evidence yet that fallacy training closes it |

Narrative.
Technique-based inoculation is the best-evidenced educational approach for goal (a) in the brief, and its core finding (people recognise a taught technique better afterwards) is preregistered and replicated across seven experiments and a million-view YouTube campaign.
Three things are not established: (1) whether the effect is discernment or generalised scepticism (two research groups reach opposite conclusions from overlapping data); (2) durability beyond about two months without boosters; (3) transfer to real political speech in situ.
No study was found that tests whether teaching fallacies improves citizens' judgement of actual debate excerpts, and the one realistic-feed test (Wang et al. 2025) found near-null behavioural effects.
The v4 layer should therefore be framed and evaluated as media-literacy content, with the platform itself as the natural test bed (pre/post technique-recognition quizzes on real French debate clips, with true-statement controls to detect the bias shift).

## D. Real-time / live fact-checking of debates

| Study | Year | Venue | Design & sample | Key result | Replication status | Implication |
|---|---|---|---|---|---|---|
| Garrett & Weeks, "The promise and peril of real-time corrections to political misperceptions" | 2013 | CSCW 2013 | Between-subjects online experiment, N = 574 (570 analysed); misinformation about electronic health records; control vs delayed correction (n = 191) vs immediate in-line correction (n = 182) | Accuracy vs control: delayed +3.3 points, immediate +5.2 (both p < .001); immediate > delayed (F(1,567) = 5.31, p < .05); but immediate correction interacts with prior attitude: more effective for supporters, less for opponents, whereas delayed correction works equally | Single study, non-political-candidate topic | Live corrections help those already inclined to accept them; they can widen the gap for the sceptical |
| Fridkin, Kenney & Wintersieck, "Liar, liar, pants on fire" | 2015 | Political Communication 32(1) | Internet survey experiment; negative ads with no / accurate / inaccurate fact-check article | Fact-checks change perceived accuracy, usefulness, tone of ads; sophisticated and negativity-averse citizens most responsive | About ads, not live debates | Audience heterogeneity: the engaged benefit most |
| Wintersieck, "Debating the truth: the impact of fact-checking during electoral debates" | 2017 | American Politics Research 45(2) | Experiment: debate exposure with fact-check ratings | "True" ratings raised candidate evaluation and vote likelihood; "half-true" no effect | Single study | Only decisive verdicts move debate viewers |
| Nyhan, Porter, Reifler & Wood | 2020 | Political Behavior | Post-debate fact-check exposure (2016) | Beliefs improved; candidate attitudes unchanged | see A | Same for debate context |
| Duke Reporters' Lab, Squash (automated live fact-checking) reports | 2019-2020 | Reporters' Lab blog / Nieman Lab | Deployment during State of the Union and 2020 conventions; ASR + match to ClaimReview archive + human "Gardener" editor | SOTU 2020: 20 pop-ups, 6 "in the ballpark"; frequent ASR errors; long idle periods because too few claims had prior checks; humans needed to select matches | Engineering reports, not experiments | A live layer today = retrieval of prior checks plus a human editor; it will be silent most of the time |
| Duke "FactPopUp" Chrome extension | 2016 | Reporters' Lab / Poynter | Pop-up Truth-O-Meter ratings over debate livestream (human-pushed) | Feasibility only; no audience evaluation published (**UNVERIFIED** absence) | | |
| Venktesh & Setty, "LiveFC: a system for live fact-checking of audio streams" | 2024 | arXiv 2408.07448 (under review) | System: live ASR, speaker attribution, claim detection, retrieval, verification | No audience or accuracy evaluation in abstract (**UNVERIFIED**) | | Architecture reference only |
| CBS News QR-code live blog, 2024 VP debate | 2024 | Seattle Times / news | On-screen QR code to a live blog by 20 journalists | No evaluation | | Second-screen delivery is the operational model broadcasters use |

Narrative.
The honest summary is that live, on-screen correction has essentially no causal evidence base beyond one 2013 lab experiment, and that experiment found the feature most likely to matter (reaching people predisposed to believe the claim) is exactly where real-time correction underperforms delayed correction.
Operationally, Duke's multi-year attempt concluded that automation cannot yet parse the "nuance and context" of political speech and reverted to human selection.
Nothing was found on whether viewers trust live corrections more or less than post-hoc ones (**UNVERIFIED** gap).
For 2027 the defensible plan is a second-screen live feed curated by humans (as Full Fact does for Question Time), with automated claim matching as an internal aid, and a published post-debate check as the product of record.

## E. Automatic claim detection (check-worthiness)

| Study / campaign | Year | Venue | Design & sample | Key result | Replication status | Implication |
|---|---|---|---|---|---|---|
| Hassan, Arslan, Li & Tremayne, ClaimBuster | 2017 | KDD 2017 | US presidential debates 1960-2016; 20,788 candidate-spoken sentences; 374 crowd participants, 86 "top-quality" after screening against 1,032 expert-labelled sentences; labels NFS / UFS / CFS | SVM: CFS precision 0.72, recall 0.67; P@100 = 0.96 for ranking | Dataset reused by CheckThat! 2018-2024 | Ranking the top claims is easy; classifying all sentences is not |
| Konstantinovskiy, Price, Babakar & Zubiaga (Full Fact), "Towards automated factchecking: developing an annotation schema and benchmark" | 2021 (arXiv 2018) | Digital Threats: Research and Practice (arXiv 1809.08193) | Sentences from UK political TV shows, 7-category schema, universal sentence encoder classifier | F1 = 0.83, ~5% relative over ClaimBuster / ClaimRank; agreement figures not in abstract (**UNVERIFIED**) | Single organisation | Closest analogue to French broadcast transcripts; F1 ~0.8 is the realistic ceiling on new domains |
| CheckThat! 2018 Task 1 | 2018 | CLEF (arXiv 1808.05542) | English + Arabic debate/speech sentences, ranking by MAP | Best MAP 0.1332 (Prise de Fer) | | Early ranking metrics look poor because check-worthy sentences are rare |
| CheckThat! 2019 Task 1 | 2019 | CLEF | Debates and speeches | Best MAP 0.166 (0.250 on speeches, 0.054 on debates) | | Debates are harder than speeches |
| CheckThat! 2020 Task 1 | 2020 | CLEF (arXiv 2007.07997) | English COVID tweets | Best MAP 0.806 (Accenture) | | Tweets are easier than debate speech |
| CheckThat! 2022 Subtask 1A | 2022 | CLEF (CEUR 3180) | Tweets, 6 languages, F1 positive class | English 0.698 (AI Rational), Arabic 0.628 (NUS-IDS), Spanish 0.571 (NUS-IDS, expert-journalist annotated), Turkish 0.801 (RUB-DFL), Bulgarian 0.617 (NUS-IDS); Dutch **UNVERIFIED** | | Spanish, the only expert-annotated set, was hardest |
| CheckThat! 2023 Task 1 | 2023 | CLEF (CEUR 3497) | 1B multigenre: English US debate sentences, Arabic/Spanish tweets; 1A multimodal | 1B English debates F1 0.898 (OpenFact), Arabic 0.809, Spanish 0.641; Cohen's kappa 0.49 (moderate) between annotators on the 736-item English 1A test set | | Human agreement on "check-worthy" is moderate; F1 0.9 on well-known US debates |
| CheckThat! 2024 Task 1 | 2024 | CLEF (CEUR 3740) | Arabic / Dutch / English; English test = US presidential debate sentences; 37 teams | English F1 0.802 (FactFinders, fine-tuned Llama-2-7B; baseline 0.307), Dutch 0.732 (TurQUaz), Arabic 0.569 (IAI Group); LLM prompting/fine-tuning won English and Dutch | Annual | 2024-era LLMs: F1 ~0.8 on debate sentences |
| CheckThat! 2025 | 2025 | CLEF (CEUR 4038) | No check-worthiness task (subjectivity, numerical claims, claim normalisation, retrieval) | 9-language subjectivity: Greek and Ukrainian best F1 below 0.65 / 0.51 | | The lab moved on; check-worthiness is considered "solved enough" for English tweets/debates but has no French benchmark |

Narrative.
Check-worthiness detection is the most mature component: on the canonical US debate corpus, systems reach F1 0.80-0.90 for the positive class, and since 2024 the winners are fine-tuned or prompted LLMs.
Two caveats bound this.
First, the label itself is soft: expert-versus-novice agreement on the 2023 test set was kappa 0.49, and the Spanish set annotated by professional fact-checkers was consistently the hardest, so a French set annotated by journalists should be expected to score nearer 0.6-0.7 than 0.9.
Second, no French or multilingual check-worthiness benchmark with French exists (the CheckThat! multilingual editions covered Arabic, Bulgarian, Dutch, Spanish, Turkish, German, Italian, Greek, Ukrainian, Romanian, Polish); SemEval-2025 Task 7 on fact-checked claim retrieval is multilingual but its French coverage was not verified (**UNVERIFIED**).
For v3, a French fine-tuned model with a journalist-annotated test set (at least 1,000 sentences, two annotators, published kappa) is the minimum credible setup.

## F. Automatic fact verification

| Study / campaign | Year | Venue | Design & sample | Key result | Replication status | Implication |
|---|---|---|---|---|---|---|
| Thorne, Vlachos et al., FEVER shared task | 2018 | EMNLP FEVER workshop (arXiv 1811.10971) | 185k Wikipedia-derived claims, Supported / Refuted / NEI; 23 teams | Best FEVER score 64.21% | Benchmark still used; later systems ~75% (**UNVERIFIED**) | Synthetic Wikipedia claims are far easier than political claims |
| Schlichtkrull, Chen, Vlachos et al., AVeriTeC shared task | 2024 | FEVER 2024 (ACL Anthology 2024.fever-1.1) | 4,568 real-world fact-checked claims with web evidence; labels Supported / Refuted / Conflicting-or-cherry-picking / NEI; 21 teams | Winner TUDA_MAI AVeriTeC score 0.63 (baseline 0.11); score = verdict accuracy only when evidence Q+A Hungarian-METEOR >= 0.25 | Annual | A "cherry-picking" label exists in the benchmark and is the hardest class |
| AVeriTeC 2025 (2nd shared task) | 2025 | FEVER 2025 (2025.fever-1.15) | Open-weights only, single 23 GB GPU, <= 1 min per claim; stricter Ev2R LLM-based evidence recall; test set 38.8% numerical claims; 7 submissions | Winner CTU AIC 33.17% | Annual | Under realistic constraints and honest evidence scoring, two thirds of claims are not verified correctly |
| Quelle & Bovet, "The perils and promises of fact-checking with large language models" | 2024 | Frontiers in AI 7 | 3,000 PolitiFact claims (500 per 6-level verdict) + multilingual Data Commons set (14 languages, <= 500 each); GPT-3.5 / GPT-4, with and without Google retrieval | Retrieval-augmented GPT-4 best; models better at flagging false than true claims; exact 6-level verdict accuracy "extremely low"; non-English claims markedly worse, translation to English helps | Single study, widely cited | Binary true/false with retrieval is feasible for triage; graded verdicts are not; French input should be handled with care |
| Wei et al. (Google DeepMind), "Long-form factuality in LLMs" (SAFE) | 2024 | NeurIPS 2024 (arXiv 2403.18802) | LLM agent splits text into atomic facts and checks each with Google Search; compared with crowd annotators on 16k facts | Agrees with 72% of human annotations; wins 76% of 100 sampled disagreements; 20x cheaper | Open code | Atomic-fact decomposition + search is the strongest pattern for v3, but "beats crowdworkers" is not "beats fact-checkers" |
| Min et al., FActScore | 2023 | EMNLP 2023 | Atomic-fact precision of biographies | Establishes the decomposition metric (numbers not retrieved, **UNVERIFIED**) | | Same |
| Venktesh, Anand et al., QuanTemp | 2024 | SIGIR 2024 (arXiv 2403.17169) | 15k+ numerical claims (comparative, statistical, interval, temporal) from 45 fact-checkers; 423k evidence snippets; labels True 18.8% / False 57.9% / Conflicting | Best baseline macro-F1 58.32; claim decomposition +8.8 macro-F1; numerical-aware models help | Used as CheckThat! 2025 Task 3 basis | Numbers are the hard case, and political debates are full of them |
| CheckThat! 2025 Task 3, numerical claims | 2025 | CLEF (CEUR 4038 paper 53) | English / Spanish / Arabic; 13 teams, 258 runs; mostly LLM decomposition + BM25 + cross-encoder rerank | English best macro-F1 59.54 (LIS), the only team above the 58.32 benchmark baseline (not significant); Spanish 50.34; Arabic 96.15 but binary (no Conflicting class) | Continues as CheckThat! 2026 Task 2 | State of the art on numerical political claims is ~0.6 macro-F1; "conflicting / half-true" is the failure point |
| Walters & Wilder, "Fabrication and errors in the bibliographic citations generated by ChatGPT" | 2023 | Scientific Reports 13 | 636 citations in 84 LLM-written reviews | 55% of GPT-3.5 and 18% of GPT-4 citations fabricated; of real ones, 43% / 24% contain substantive errors | Replicated in many domains | Never let a model cite from memory; every source must be retrieved and stored |
| Lim | 2018 | Research & Politics | see A | Human fact-checkers disagree in the middle of the scale | | The v3 labels "cherry-picked" and "misstated" are exactly where humans disagree; an automatic system has no ground truth to learn |

Narrative.
Verification of real political claims is not a solved problem.
The best published open-domain system under honest evidence scoring correctly verifies about a third of AVeriTeC claims (2025) and about two thirds under the more lenient 2024 metric; numerical claims, the bread and butter of French debates (unemployment, deficits, immigration figures), sit at macro-F1 ~0.6 with "conflicting" verdicts the main failure.
Known failure modes are consistent across studies: fabricated or misattributed sources when retrieval is absent, weaker performance on true claims than on false ones, worse performance in non-English input, and inability to produce graded verdicts.
What does work is decomposition into atomic facts, retrieval from a curated corpus (INSEE, Cour des comptes, Eurostat, legislative texts), and a supported / refuted / insufficient-evidence triage handed to a human.
The four-way public scale in the brief (verified / cherry-picked / misstated / false) should be assigned by humans, with the AI output shown as evidence and a proposed label.

## G. Automatic fallacy and propaganda-technique detection

### G.1 Datasets, human agreement, and model results

| Study | Year | Venue | Design & sample | Key result | Replication status | Implication |
|---|---|---|---|---|---|---|
| Da San Martino, Yu, Barron-Cedeno, Petrov & Nakov, "Fine-grained analysis of propaganda in news articles" (PTC corpus) | 2019 | EMNLP 2019 | English news, 18 techniques, span-level; 2 annotator teams + consolidators, 395 person-hours | Pre-consolidation gamma agreement 0.30-0.34 on spans (0.31 with labels; pilot 0.34/0.31); after discussion with consolidator gamma 0.74-0.76; sentence-level detection F1 up to 60.98 | Reused for SemEval-2020 | Even trained annotators agree poorly on technique spans until they negotiate |
| SemEval-2020 Task 11 (Da San Martino et al.) | 2020 | SemEval 2020 (arXiv 2009.02696) | PTC; span identification (SI) and technique classification (TC, 14 techniques) | SI best F1 51.55 (Hitachi); TC best F1 62.07 (ApplicaAI); reported average gamma 0.6 | Annual benchmark | Finding the span is harder than naming the technique once given the span |
| SemEval-2023 Task 3 (Piskorski, Stefanovitch, Da San Martino, Nakov) | 2023 | SemEval 2023 | 23 persuasion techniques, paragraph-level, 9 languages incl. **French**; ~40 annotators; 2,049 documents | Krippendorff's alpha 0.342 before consolidation (0.415 top half, 0.250 bottom half of annotators); French best micro-F1 0.469 / macro-F1 0.322 (team NAP); English best micro-F1 0.376; Italian 0.550; winner KInITVeraAI (XLM-RoBERTa-large, joint multilingual) | Annual | The only French technique benchmark: micro-F1 below 0.5 and macro-F1 ~0.3 |
| Goffredo, Haddadan, Vorakitphan, Cabrio & Villata, "Fallacious argument classification in political debates" (ElecDeb60to16) | 2022 | IJCAI 2022 | 31 US presidential debates 1960-2016, 3 computational-linguistics annotators; 1,628 fallacies in 6 categories: Appeal to Emotion 1,016 (loaded language 676, flag waving 151, pity 102, fear 87), Appeal to Authority 234, Ad Hominem 188, False Cause 69, Slogans 64, Slippery Slope 57; 14 sub-categories | IAA (3 annotators, 9 sections of 5 debates), Krippendorff's alpha: Ad Hominem 0.53, Appeal to Authority 0.58, Appeal to Emotion 0.46, Slogans 0.60 ("moderate"); 6-class macro-F1: BERT 0.55, RoBERTa 0.53, Longformer + joint loss + gold argument component/relation features 0.84; ablation without argument features 0.61; 14-subclass macro-F1 0.42: Loaded Language 0.83, Slogan 0.68, Flag Waving 0.65, Without Evidence 0.57, Ad Hominem 0.52, Pity 0.51, Popular Opinion 0.50, Fear 0.43, Slippery Slope 0.32, Circumstantial Ad Hominem 0.28, Name-Calling 0.27, False Cause 0.27, False Authority 0.00, Tu Quoque 0.00 | Extended 2023; base of 2025 shared task | Human agreement is moderate; the 0.84 relies on gold argument annotations that will not exist for live French debates |
| Goffredo, Chaves Espinoza, Cabrio & Villata, "Argument-based detection and classification of fallacies in political debates" (ElecDeb60to20) | 2023 | EMNLP 2023 | Adds 2020 Trump-Biden debates (232 new fallacies; total fallacy instances ~1,860) | IAA on 50 sentences: observed agreement 0.857, Krippendorff's alpha 0.757 ("substantial"); token-level fallacy detection (BIO merged) macro-F1 0.7394 (MultiFusion BERT with component, relation, PoS features), 0.72 for plain BERT-large token classifier | | Detection (is there a fallacy here?) reaches ~0.74; classification is the weak link |
| MM-ArgFallacy2025 shared task (Mancini et al.; system paper Pittiglio) | 2025 | ArgMining 2025 | MM-USED-fallacy: same 6 classes, text + audio of US debates | Fallacy classification macro-F1 0.4444 text-only, 0.3559 audio-only, 0.4403 multimodal (this system; task-best **UNVERIFIED**) | | Without gold argument structure, 6-class debate fallacy classification is ~0.44 |
| Dore, Damo, Cabrio & Villata, "Retrieving relations, detecting fallacies: a RAG approach to political debate analysis" | 2026 | arXiv 2608.27471 | ElecDeb60to20; retrieval over 15 GB political corpus guided by support/attack relations; 42 configurations, 14 models | Detection macro-F1 up to 0.864 (ModernBERT, +0.100 over no retrieval); classification up to 0.725 (+0.148); some LLMs lose 0.14-0.33 macro-F1 when given retrieved context | Preprint, not yet peer-reviewed | Current best on the standard debate benchmark; classification still ~0.73 |
| Jin, Lalwani, Vaidhya, Shen, Ding, Lyu, Sachan, Mihalcea & Scholkopf, "Logical fallacy detection" (LOGIC) | 2022 | Findings of EMNLP 2022 | LOGIC: 2,449 quiz-site examples, 13 classes; LOGICCLIMATE: 1,079 from Climate Feedback | Zero-shot RoBERTa-MNLI / GPT-2: 12-14% micro-F1 (near random); fine-tuned Electra 53.31; structure-aware Electra 58.77; per class: ad populum 79.45, ad hominem 78.65, faulty generalisation 60.24, deductive fallacy 25.81; transfer to real climate texts: 22.7-29.4 F1 | Widely reused | Textbook fallacies are learnable; real-world texts drop to F1 ~0.3 |
| Alhindi, Chakrabarty, Musi & Muresan, "Multitask instruction-based prompting for fallacy recognition" | 2022 | EMNLP 2022 | 5 datasets unified, 28 fallacy types; T5-large / T5-3B | T5-3B multitask acc/macro-F1: Argotario 64/64, Propaganda 73/56, LOGIC 70/66, COVID-19 29/28, Climate 25/20 (column mapping inferred from Table 2 order); GPT-3 few-shot competitive only on the 5-class Argotario | | Fact-checked real-world fallacies (COVID, climate) sit at F1 0.2-0.3 |
| Helwe, Calamai, Paris, Clavel & Suchanek, MAFALDA | 2024 | NAACL 2024 | 200 manually annotated texts (incl. 17 political-debate texts), 260 fallacy instances, 23 fine classes in 3 levels; 4 extra human annotators on 20 items | Zero-shot F1 (L0 binary / L1 category / L2 fine): GPT-3.5 0.627 / 0.201 / 0.138; Zephyr-7B 0.524 / 0.192 / 0.098; Mistral-Instruct-7B 0.536 / 0.144 / 0.069; random 0.435 / 0.061 / 0.010; humans on sample 0.749 / 0.352 / 0.186; treating any single annotator as gold, the others reach at most F1 0.144 at L2 | Benchmark reused by Pan 2024 | The human ceiling at fine granularity is F1 ~0.2; "GPT does not perform better than humans" |
| Ruiz-Dolz & Lawrence, "Detecting argumentative fallacies in the wild" | 2023 | ArgMining 2023 | Natural-language argumentation-scheme corpus; 4 fallacy classes + no fallacy | Macro-F1, 5-class: RoBERTa fine-tuned 66.5 vs GPT-4 51.7 vs GPT-3.5 45.5; 2-class detection: RoBERTa 79.6 vs GPT-4 51.1; 4-class: RoBERTa 76.2 vs GPT-4 58.3; adding context lowered LLM scores | | Zero-shot LLMs trail small fine-tuned models on fallacies |
| Pan, Wu, Li & Luu, "Are LLMs good zero-shot fallacy classifiers?" | 2024 | EMNLP 2024 | GPT-4, GPT-3.5, Qwen2.5-14B/7B, Llama-3-8B, Mistral-7B, Llama-2-13B on Argotario, LOGIC, Reddit, ElecDeb, Propaganda (in-domain for T5) and MAFALDA, COVID (OOD) | GPT-4 zero-shot macro-F1 (single-round): Argotario 78.9, LOGIC 50.4, Reddit 79.1, **ElecDeb 42.3**, Propaganda 34.8, MAFALDA 48.7, COVID 20.5 (column order inferred from table layout); best full-shot T5-3B: ElecDeb 56.4, Propaganda 43.3, MAFALDA 35.6, COVID 14.6; multi-round prompting adds 1-4 points | | On political debates GPT-4 zero-shot is ~0.42 macro-F1, below a fine-tuned T5 |
| Ramponi, Daffara & Tonelli, "Fine-grained fallacy detection with human label variation" (Faina) | 2025 | NAACL 2025 | Italian social-media posts on migration, climate, health; 11k+ span annotations, 20 types, 2 experts, label variation preserved | Multi-task transformer baselines "strong"; numbers not retrieved (**UNVERIFIED**) | | Nearest Romance-language resource; explicitly treats disagreement as signal |
| Habernal et al., ad hominem in Reddit CMV | 2018 | (cited in Goffredo 2022) | Single fallacy | Cohen's kappa 0.79 | | Agreement is high only for the one fallacy with clear lexical markers |
| Sourati et al., case-based reasoning for fallacy classification | 2023 | IJCAI 2023 / Knowledge-Based Systems | | Numbers not retrieved (**UNVERIFIED**) | | |

### G.2 Answers to the specific questions

Is human agreement on fallacy labels in political debate high or low? Moderate at best.
Per-type Krippendorff's alpha among three trained linguists on US debates was 0.46 (emotion) to 0.60 (slogans), below the 0.667 conventionally required for reliable coding; the 2023 extension reports 0.757 but on only 50 sentences.
Propaganda-technique spans in news start at gamma ~0.3 and reach 0.75 only after negotiated consolidation; the 23-technique multilingual corpus (including French) has alpha 0.34.
MAFALDA's user study shows that four humans given the same texts reach F1 0.19 against a curated gold standard and 0.14 against each other at fine granularity.
Any automatic system evaluated against a single gold label is therefore being scored against a partially arbitrary reference, and macro-F1 above ~0.75 should be read as fitting one team's annotation conventions, not as recovering an objective property of the speech.

Which fallacy classes are detectable and which are not? Detectable (F1 0.65-0.85 in-domain): loaded language, name-calling / ad hominem when insulting words are present, slogans, flag-waving, ad populum with explicit majority markers.
Weak (F1 0.4-0.55): appeal to fear / pity, "without evidence" appeals to authority, slippery slope.
Not detectable with current methods (F1 0.0-0.3): false authority, tu quoque, false cause, circumstantial ad hominem, deductive / formal fallacies, and every class once texts move from quizzes to real fact-checked content (LOGICCLIMATE, COVID, Climate: F1 0.2-0.3).
The pattern is consistent across papers: models detect lexical surface cues, not invalid inference.

French: no French political-debate fallacy dataset exists.
SemEval-2023 French persuasion techniques (news paragraphs) is the only French benchmark, with micro-F1 0.47 and macro-F1 0.32 at the top.
Everything above would have to be re-annotated for French debates, and the IAA numbers above are the realistic expectation for that annotation.

## H. Speech-to-text and diarization for French debate audio

| Source | Year | Type | Setup | Key numbers (French unless noted) | Status | Implication |
|---|---|---|---|---|---|---|
| Mistral, Voxtral technical report | 2025 | arXiv 2507.13264 | FLEURS and Common Voice 15.1, per-language WER | FLEURS fr: Voxtral Small 4.03, GPT-4o-mini-transcribe 4.51, Voxtral Mini 4.87, ElevenLabs Scribe 5.07, Whisper-large-v3 5.55, Gemini 2.5 Flash 6.17. Common Voice 15.1 fr: Scribe 5.44, Voxtral Small 6.18, Voxtral Mini 8.92, GPT-4o-mini 10.75, Whisper-large-v3 11.33, Gemini 11.86 | Vendor report, but includes competitors with stated method | Best French clean-speech WER is 4-6%; Whisper-large-v3 is 1-2 points behind the newest models |
| NVIDIA, Canary-1B-v2 & Parakeet-TDT-0.6B-v3 report | 2025 | arXiv 2509.14128 | FLEURS (25 langs), MLS, CoVoST2 | FLEURS fr: Canary-1B-v2 5.02. MLS fr: Canary-1B-v2 3.36, Parakeet-TDT-0.6B-v3 4.97, Voxtral-Mini 5.75, Whisper-large-v3 7.15 | Vendor report | Open NVIDIA models match or beat Whisper on French read speech; Parakeet v3 supports French |
| ElevenLabs Scribe launch blog | 2025 | Vendor blog | FLEURS | Claims 3.1% fr WER; Mistral's independent measurement gives 5.07 | Vendor claim, contradicted by third-party measurement | Treat vendor WER claims as upper bounds on quality |
| Deepgram Nova-3, Gladia Solaria-3, AssemblyAI Universal-2 | 2025-2026 | Vendor pages | French supported; Deepgram reports 5.26% median batch WER on its own suite (all languages); Gladia reports internal-dataset gains only | No public French benchmark WER found (**UNVERIFIED**) | | Benchmark them yourself on 1-2 hours of French debate audio before choosing |
| Bain, Huh, Han & Zisserman, WhisperX | 2023 | Interspeech 2023 | Word-level timestamps via forced alignment + VAD; diarization via pyannote | AMI word-timestamp precision 84.1% / recall 60.3% (200 ms tolerance); alignment models are per-language, English primary | Widely used | Word timestamps for clip linking are good enough; verify the French alignment model |
| Koenecke, Choi, Mei, Schellmann & Sloane, "Careless Whisper" | 2024 | ACM FAccT 2024 | Whisper hallucinations on real speech | ~1% of transcriptions contain hallucinated phrases absent from audio; 38% of those are harmful (invented violence, false attribution) | Peer-reviewed | A 1% hallucination rate is unacceptable for attributed quotations without human check |
| pyannote speaker-diarization-3.1 model card | 2023-2024 | Hugging Face | DER with no collar, overlap scored | **REPERE phase 2 (French TV): DER 7.8%** (FA 1.8, miss 2.6, confusion 3.5); VoxConverse 11.3; AISHELL-4 12.2; AMI headset 18.8; DIHARD-3 full 21.7; AliMeeting 24.4 | Open, reproducible | French broadcast diarization is at ~8% DER in the least forgiving setup |
| Charlet et al. / Orange-LIMSI, overlap in ETAPE | 2013 | ICASSP 2013 | French broadcast news and debates | Overlapping speech = 6.7% of speech in ETAPE TV, 1.2% in news, **10.4% in debates**; overlap detection F1 up to 59.2%; overlap handling improves DER up to 26% relative | Campaign-era | One word in ten of a French TV debate is spoken over someone else; those words are the ones most likely to be mistranscribed and misattributed |
| REPERE campaign results (as cited by Bredin et al.) | 2013 | | 3 h of French TV | Best systems DER ~11% single-show, ~14% cross-show | Historical | Modern systems roughly halved this |
| Ryant et al., DIHARD III | 2021 | Interspeech 2021 (arXiv 2012.01477) | 11 domains, hardest public diarization benchmark | Track 2 (from scratch) best systems DER ~17% full / ~20% core (Hitachi-JHU 16.94 / 20.01, 2nd place); baseline 19.37 core | Campaign | Multi-domain "wild" audio is 2x harder than clean TV |

Narrative.
For v1 search and navigation, current French ASR is adequate: 4-6% WER on clean speech, likely 8-15% on lively debate segments with overlap (**estimate, UNVERIFIED**; no published Whisper-v3-era WER on ESTER / ETAPE / REPERE debate audio was found).
For verbatim quotation, the arithmetic is unforgiving: at 5% WER the probability that a 30-word quotation contains at least one error is 1 - 0.95^30 = 78%; at 2% it is 45%.
Diarization confusion of 3.5% on REPERE plus 10% overlapped speech in debates means a non-trivial share of sentences will be attributed to the wrong candidate exactly in the heated exchanges that matter most.
Whisper-family hallucinations (~1% of segments, sometimes inventing violent or attributive content) are a reputational hazard for a site that publishes what candidates "said". The workable design is: automatic transcript with word timestamps for search and clip linking; every span that is quoted, rated (v3) or tagged (v4) is played back and corrected by a human before publication; the corrected transcript is diffed against the ASR output to publish a running WER, which also doubles as the platform's own French debate benchmark.

## Design recommendations grounded in evidence

1. **AI as pre-annotator, humans as authors.** Every layer where the literature shows F1 below ~0.8 or human agreement below alpha 0.67 (claim verification, graded verdicts, all fallacy classes, overlapped speech) must route through a human review queue. Publish the queue statistics (proposed vs accepted labels) so the AI's real precision is visible.
2. **Publish inter-rater agreement, per label.** Double-annotate a fixed 10% sample of claims and technique tags; report Krippendorff's alpha per label on the site. The field's numbers (0.46-0.60 for debate fallacies, 0.34 for persuasion techniques, kappa 0.49 for check-worthiness) are the benchmark; if yours are similar, say so, and drop labels that stay below 0.5.
3. **Prefer explanation to verdict.** The meta-analytic moderators (Walter 2020; Chan 2017) favour detailed corrections; scale-only ratings dilute effects and are where professionals disagree (Lim 2018) and audiences ignore (Wintersieck 2017). Show the evidence and the reasoning first, the label second; consider collapsing "cherry-picked" and "misstated" into "misleading (see why)".
4. **Do not score people.** No study supports a per-candidate "fallacy count" or "honesty index"; annotation noise (alpha ~0.5) would dominate any ranking, and selection of which statements get checked is itself a known bias (Lim 2018; Ceron & Carrara 2023). Present techniques per statement, with the timestamped clip, and let users see the full transcript around it.
5. **Show the technique with its definition, a neutral example, and a "why this is not just persuasion" note.** This mirrors the inoculation videos that produced *d* 0.3-0.7 recognition gains, and counters the documented risk that technique training raises blanket scepticism: always include clearly valid arguments as counter-examples and, if you run a quiz, include true statements to measure discrimination (d') rather than bias.
6. **Plan for decay.** Belief corrections and inoculation effects fade in 2-8 weeks. A reference site is re-consulted; that is its mechanism. Build for return visits (per-debate digests, per-claim permalinks, notifications when a repeated claim is checked again), not for one-time exposure.
7. **Expect no effect on vote intention, and say so.** The French and US evidence agrees: knowledge changes, support does not. Frame the platform's success metric as accuracy of citizens' beliefs and quality of public argument, not electoral outcomes; the alternative sets the project up to be judged a failure by its own PR.
8. **Anticipate salience side-effects.** Barrera et al. found that checking Le Pen's refugee figures increased the salience of immigration. Balance coverage across candidates and themes (v2 theme classification can be used to audit this) and publish the distribution of checked statements by candidate and theme.
9. **Deterrence: measure evasiveness.** If the platform aims at politician behaviour, track the share of unverifiable statements per candidate over time (the Italian RCT's substitution effect), not only the share of false ones.
10. **Live layer: human-curated second screen, automated matching internal.** Given Squash's 6-of-20 hit rate and the lack of audience evidence, run live as a moderated feed that mostly surfaces previously checked claims (repeat claims are the tractable case), publish the full check afterwards, and instrument it (A/B on delayed vs immediate delivery with belief measures) so 2027 produces the missing evidence.
11. **Verification pipeline.** Atomic-claim decomposition, retrieval only from a curated French corpus (INSEE, DREES, Cour des comptes, Eurostat, Legifrance, parliamentary reports) with stored snapshots, NLI-style supported / refuted / insufficient triage, explicit numeric handling (unit, period, base of comparison), and a hard rule that no source can be cited unless it was retrieved.
12. **Transcript integrity.** Word-level timestamps; human correction of every published span; running published WER and DER estimated from the corrected sample; explicit "overlapping speech" markers; never show a candidate's name next to text that has not been attribution-checked.
13. **French benchmark contribution.** Because no French check-worthiness or debate-fallacy dataset exists, the platform's corrected transcripts and double-annotated labels are themselves a research asset; releasing them (with IAA) would give the project scientific credibility and let others measure what the site's models actually do.

## Layer-by-layer evidence map

| Platform layer | What the evidence supports | Best published numbers | Main documented risk | Human role required |
|---|---|---|---|---|
| v1 Transcripts (search, navigation) | Fully feasible for search; usable word timestamps | French clean-speech WER 4-6% (FLEURS: Voxtral Small 4.03, Whisper-large-v3 5.55); French TV diarization DER 7.8% (pyannote 3.1, REPERE) | 10.4% overlapped speech in debates; ~1% hallucinated segments (Whisper); misattribution in heated exchanges | Correct every span that is quoted, rated, or tagged; mark overlap |
| v2 Theme classification | Not researched here; standard topic classification, no political-science evidence needed | n/a | Silent coverage imbalance across candidates/themes (salience effect, Barrera 2020) | Use it to audit balance and publish the distribution |
| v3a Claim extraction (check-worthiness) | Mature on English debates; moderate human agreement | F1 0.80-0.90 positive class (CheckThat! 2023-2024); kappa 0.49 | No French benchmark; journalist-annotated sets score lower (Spanish 0.57-0.64) | Annotate a French test set; review the top-ranked claims, not all sentences |
| v3b Claim verification and rating | Feasible only as retrieval-assisted triage | AVeriTeC 0.63 (2024, lenient) / 0.33 (2025, strict); numerical claims macro-F1 ~0.6; GPT-4 6-level verdicts "extremely low" | Fabricated sources without retrieval (18-55%); "conflicting/cherry-picked" is the weakest class for humans and machines | Humans assign the public label; AI supplies decomposed sub-claims, retrieved evidence, and a proposal |
| v3c Effect on citizens | Proven: beliefs improve (*d* ~0.3), no backfire; decay in weeks; no vote effect | Walter 2020 *d* = 0.29; Porter & Wood 2021 >2 weeks; Barrera 2020 French null on support | Salience spillover; middle-scale ratings ineffective and unreliable | Write detailed explanations; avoid scale-only verdicts |
| v3d Effect on politicians | Plausible, thin: one field RCT, one weak replication, one unpublished RCT | Negative ratings 2.8% to 1.3% (Nyhan & Reifler 2015) | Substitution toward unverifiable statements (Mattozzi et al.) | Track unverifiable-statement share as an outcome |
| v4 Fallacy / technique tagging | Detection ~0.74-0.86 macro-F1 on US debates; coarse classification 0.44-0.73 without gold structure; fine classes collapse | Goffredo 2022/2023; Dore 2026; MM-ArgFallacy 2025 text 0.44; MAFALDA humans 0.19 at fine level | Human agreement alpha 0.46-0.60; inferential fallacies at F1 0-0.3; zero French debate data | Humans confirm every tag; publish per-label agreement; restrict public labels to detectable classes |
| v4 Educational effect (inoculation) | Technique recognition rises after short explainers; contested whether discernment or scepticism | *d* 0.28-0.68 (RCTs), *h* 0.09 (YouTube); decay ~2 months | Blanket scepticism (response bias); near-null behaviour change in feeds; no transfer test on political speech | Include true/valid examples; run pre/post quizzes with d' |
| Live layer | No causal audience evidence; automation not ready | Squash 6/20 pop-ups in the ballpark; Garrett & Weeks: immediate +5.2 vs delayed +3.3 points but worse for the predisposed | Silence most of the time; ASR errors on stage; widening of partisan gap | Human-curated second screen; automated matching of previously checked claims only |

## Metric glossary (so the numbers above are comparable)

- **Cohen's *d***: standardised mean difference; 0.2 small, 0.5 medium, 0.8 large. Fact-check belief effects are ~0.3; inoculation recognition effects 0.3-0.7 in the lab.
- **Cohen's *h***: effect size for a difference between two proportions; the YouTube inoculation field study reports *h* = 0.09, i.e. a few percentage points.
- **F1 (positive class)**: harmonic mean of precision and recall for the "check-worthy" class; used by CheckThat!. **Macro-F1**: unweighted mean of per-class F1, penalises ignoring rare classes; used by fallacy and numerical-claim tasks. **Micro-F1**: instance-weighted, dominated by frequent classes; used by SemEval-2023 persuasion techniques, which is why French micro 0.47 coexists with macro 0.32.
- **MAP**: mean average precision of a ranked list; early CheckThat! editions (0.13-0.17) look poor because only a handful of sentences per debate are positive.
- **AVeriTeC score**: verdict accuracy counted only when the retrieved evidence is judged sufficient (2024: Hungarian METEOR >= 0.25 against gold question-answer pairs; 2025: Ev2R LLM-judged recall). The 2024 and 2025 winners (0.63 vs 0.33) are not comparable because the evidence threshold changed.
- **Cohen's kappa / Krippendorff's alpha / Mathet's gamma**: chance-corrected agreement. Conventional thresholds: kappa 0.41-0.60 "moderate", 0.61-0.80 "substantial"; alpha >= 0.667 minimum for tentative conclusions, >= 0.80 for reliable coding; gamma is a span-aware unitising-plus-labelling measure and is generally pessimistic.
- **WER**: (substitutions + deletions + insertions) / reference words. **DER**: (false alarm + missed speech + speaker confusion) / reference speech time; pyannote reports it with no forgiveness collar and overlapped speech included, the strictest convention, so its numbers are not directly comparable with older campaign results that removed overlap.

## Register of UNVERIFIED items and evidence gaps

Items marked UNVERIFIED in the tables, with what would resolve them:

1. Nyhan et al. 2020 exact belief effect sizes (publisher page blocked; SSRN abstract read). Resolve: read the Political Behavior PDF.
2. Mattozzi, Nocito & Sobbrio numeric effects (SSRN and VoxEU blocked; design confirmed from the AEA registry and the VoxEU summary). Resolve: obtain the working paper PDF.
3. Authors of the 2025 SDT meta-analysis in Current Opinion in Psychology (abstract read via Semantic Scholar; author list not retrieved).
4. BJPS conceptual replication of four 2020-election findings (title and venue confirmed; abstract not retrieved).
5. Full Fact: no published evaluation of live tools or of politician behaviour change was found; absence is not proof of absence.
6. FActScore and Sourati et al. 2023 numbers not retrieved; Ramponi et al. 2025 model scores not retrieved.
7. CheckThat! 2022 Dutch best F1; CheckThat! 2021 best scores; MM-ArgFallacy2025 overall winner (only one system paper read).
8. Pan et al. 2024 and Alhindi et al. 2022 per-dataset numbers rely on column order inferred from the extracted table layout; the values quoted for ElecDeb (GPT-4 42.3, T5-3B 56.4) should be re-checked against the typeset PDF.
9. FLEURS French WER for Whisper-large-v3 in the NVIDIA report was not extractable; the Mistral report's 5.55 was used instead. Different reports normalise text differently, so cross-report comparisons carry about 1 point of uncertainty.
10. No published WER for any 2024-2026 model on French debate audio (ESTER / ETAPE / REPERE); the 8-15% figure in section H is an estimate.
11. FactPopUp / CBS QR-code audience effects: none published, as far as found.
12. Whether SemEval-2025 Task 7 (multilingual fact-checked claim retrieval) includes French.

Substantive gaps in the literature (not retrieval failures):

- No randomised evaluation of on-screen live corrections in a real televised debate with trust or belief outcomes.
- No experiment testing whether fallacy or technique training transfers to judgements of real political speech.
- No French political-debate fallacy corpus; no French check-worthiness corpus.
- No causal evidence on elite behaviour outside the US (2015) and Italy (working paper).
- Human agreement on fallacy labels has been measured on small samples (9 debate sections; 50 sentences; 20 MAFALDA texts); a larger reliability study would itself be a contribution.

## A pre-registered evaluation plan the platform could run

The platform will be the largest French-language deployment of these ideas, and several of the gaps above can be closed with modest instrumentation. Each proposed measure follows a design already used in the literature cited.

1. **Reliability audit (v3, v4).** Double-annotate 10% of claims and 100% of technique tags for the first three debates; report Krippendorff's alpha per label, as Goffredo et al. (2022) and Piskorski et al. (2023) do. Decision rule: labels with alpha < 0.5 after guideline revision are not shown to the public.
2. **Transcript accuracy (v1).** Compute WER and DER on the human-corrected spans against the raw ASR output, per debate and per speaker, and publish them. This also produces the first French debate benchmark for the models in section H.
3. **Belief effect (v3c).** A survey experiment in the Wood & Porter / Porter & Wood design: French panel, 10-20 checked claims, control vs fact-check exposure, belief accuracy measured immediately and at 2 weeks, plus candidate favourability and issue salience (the Barrera channel). Expected effect *d* ~0.3 on beliefs; power for *d* = 0.2 requires roughly 800 per arm.
4. **Format test (v3c).** Within the same experiment, randomise presentation: detailed correction only vs correction plus four-way label vs label only. This directly adjudicates the Walter-versus-Amazeen disagreement for a French audience.
5. **Technique recognition and discrimination (v4).** Pre/post quiz on real French debate clips containing (a) tagged techniques and (b) valid arguments; score with d' and criterion c as in Modirrousta-Galian & Higham (2023), not with mean ratings alone. A follow-up at 4-8 weeks tests decay (Maertens et al. 2021).
6. **Live delivery (live layer).** During one debate, randomise registered users to immediate second-screen corrections vs a post-debate digest, and measure belief accuracy and trust in the platform the next day (Garrett & Weeks design). This would be the first such field test.
7. **Elite response (v3d).** Code, for each candidate, the share of statements that are checkable, checked, rated false, and rated unverifiable across the campaign; this replicates the Italian outcome set observationally and lets the platform report whether ambiguity rises as checks accumulate.
8. **Coverage balance (v2).** Publish weekly the distribution of checked claims by candidate and theme relative to airtime; treat imbalance as a defect to correct, given the salience findings.

## Notes on reading the evidence

- The strongest evidence in this memo is meta-analytic and multi-site: fact-checks correct beliefs modestly and do not backfire. Treat this as settled.
- The weakest evidence is anything about live delivery and anything about politicians. One field experiment each, with marginal statistics, plus one unpublished replication; treat as hypotheses.
- Inoculation is in the middle: replicated for recognition, disputed for discrimination, untested for political speech. Treat as promising media-literacy content whose claims should be stated carefully.
- The NLP results follow a consistent gradient: surface cues are learnable (check-worthiness, loaded language, slogans), inference is not (numerical verification, false cause, formal fallacies), and every method loses 20-40 F1 points when moved from curated benchmarks to fact-checked real-world text or to a new language. French sits on the wrong side of that gradient today; the platform's own annotated data would move it.
- Numbers reported by vendors (ASR WER, LLM fact-checking accuracy) were consistently better than independent measurements of the same systems (ElevenLabs 3.1 vs 5.07; SAFE "better than humans" meaning crowdworkers). Independent measurement on the platform's own audio and claims is the only number that will hold up in public.

## How this memo was produced

- Primary sources were read directly: 24 PDFs (IJCAI, EMNLP, NAACL, ArgMining, KDD, CLEF/CEUR overviews, FEVER/AVeriTeC overviews, arXiv reports, the Nyhan & Reifler 2015 author PDF, Garrett & Weeks 2013) were downloaded and text-extracted locally; numbers in the tables are copied from their results tables.
- Publisher pages that block automated access (Springer, SAGE, ScienceDirect, SSRN, CEPR) were covered through the Semantic Scholar API abstract, PubMed/PMC mirrors, the AEA trial registry, or author-hosted copies; where only an abstract was available the row says so or carries UNVERIFIED.
- Vendor claims (ElevenLabs, Deepgram, Gladia, AssemblyAI) are labelled as such and, where an independent measurement exists (Mistral's Voxtral report), the independent number is given first.
- Nothing was taken from secondary summaries alone except three items explicitly flagged (Mattozzi et al. effects from the VoxEU summary; REPERE 2013 campaign DER as cited by later work; Whisper 11.0% French from the Whale paper).
- Search date 2026-09-05; the most recent items are the CheckThat! 2025 overviews (CEUR Vol-4038), the AVeriTeC 2025 overview, the 2025 PNAS Nexus and Current Opinion in Psychology inoculation papers, and the August 2026 arXiv preprint by Dore et al.

## Sources

Section A
- Walter et al. 2020, Political Communication: https://doi.org/10.1080/10584609.2019.1668894
- Chan et al. 2017, Psychological Science: https://doi.org/10.1177/0956797617714579 ; PDF https://socialactionlab.org/wp-content/uploads/2024/01/Chan_Debunking-A-Meta-Analysis-of-the-Psychological-Efficacy-of-Messages-Countering-Misinformation_2017.pdf
- Nyhan & Reifler 2010, Political Behavior: https://doi.org/10.1007/s11109-010-9112-2 ; PDF https://fbaum.unc.edu/teaching/articles/PolBehavior-2010-Nyhan.pdf
- Wood & Porter 2019, Political Behavior: https://doi.org/10.1007/s11109-018-9443-y
- Swire-Thompson, DeGutis & Lazer 2020, JARMAC: https://doi.org/10.1016/j.jarmac.2020.06.006
- Nyhan 2021, PNAS: https://doi.org/10.1073/pnas.1912440117
- Porter & Wood 2021, PNAS: https://doi.org/10.1073/pnas.2104235118
- Carey et al. 2022, Nature Human Behaviour: https://doi.org/10.1038/s41562-021-01278-3
- Nyhan, Porter, Reifler & Wood 2020, Political Behavior: https://doi.org/10.1007/s11109-019-09528-x ; SSRN https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2995128
- Barrera, Guriev, Henry & Zhuravskaya 2020, Journal of Public Economics: https://doi.org/10.1016/j.jpubeco.2019.104123 ; PSE page https://www.parisschoolofeconomics.eu/en/publications-hal/facts-alternative-facts-and-fact-checking-in-times-of-post-truth-politics/
- Amazeen, Thorson, Muddiman & Graves 2018, JMCQ: https://doi.org/10.1177/1077699016678186
- Wintersieck 2017, American Politics Research: https://doi.org/10.1177/1532673X16686555 ; LSE summary https://blogs.lse.ac.uk/usappblog/2017/03/23/real-time-fact-checking-can-change-peoples-opinion-about-a-candidate-but-only-if-the-ratings-are-decisive/
- Lim 2018, Research & Politics: https://doi.org/10.1177/2053168018786848
- BJPS conceptual replication (2020 US election) (UNVERIFIED details): https://www.cambridge.org/core/journals/british-journal-of-political-science/article/abs/conceptual-replication-of-four-key-findings-about-factual-corrections-and-misinformation-during-the-2020-us-election-evidence-from-panelsurvey-experiments/21D45B9466EA012D406BCDD67F5CDC8A

Section B
- Nyhan & Reifler 2015, AJPS: https://doi.org/10.1111/ajps.12162 ; author PDF https://bpb-us-e1.wpmucdn.com/sites.dartmouth.edu/dist/5/2293/files/2021/03/fact-checking-elites.pdf ; replication data https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/26867
- Ma et al. 2023, Human Communication Research: https://academic.oup.com/hcr/article-abstract/49/3/321/6909031
- Mattozzi, Nocito & Sobbrio, "Fact-Checking Politicians": SSRN https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4258130 ; AEA registry https://www.socialscienceregistry.org/trials/6432 ; VoxEU column https://cepr.org/voxeu/columns/politicians-response-fact-checking-evidence-randomised-experiment-leading-fact
- Ceron & Carrara 2023, New Media & Society: https://doi.org/10.1177/14614448211012377
- Full Fact live fact-checking practice: https://fullfact.org/blog/2017/nov/how-we-live-factcheck-prime-ministers-questions/ ; https://fullfact.org/live/2024/may/fact-checking-question-time/

Section C
- Roozenbeek & van der Linden 2019, Palgrave Communications: https://doi.org/10.1057/s41599-019-0279-9
- Basol et al. 2021, Big Data & Society: https://doi.org/10.1177/20539517211013868
- Maertens et al. 2021, JEP: Applied: https://doi.org/10.1037/xap0000315 ; PubMed https://pubmed.ncbi.nlm.nih.gov/33017160/
- Roozenbeek et al. 2022, Science Advances: https://doi.org/10.1126/sciadv.abo6254 ; PMC https://pmc.ncbi.nlm.nih.gov/articles/PMC9401631/ ; Cambridge summary https://www.cam.ac.uk/stories/inoculateexperiment
- Roozenbeek, Traberg & van der Linden 2022, RSOS: https://royalsocietypublishing.org/rsos/article/9/5/211719/96738/Technique-based-inoculation-against-real-world ; correction https://royalsocietypublishing.org/doi/10.1098/rsos.231235
- Modirrousta-Galian & Higham 2023, JEP: General: https://pubmed.ncbi.nlm.nih.gov/36996156/
- Graham et al. 2023, Journal of Cognition: https://journalofcognition.org/articles/10.5334/joc.324
- Seabrooke, Modirrousta-Galian & Higham 2025, Psychonomic Bulletin & Review: https://link.springer.com/article/10.3758/s13423-025-02827-x ; PMC https://pmc.ncbi.nlm.nih.gov/articles/PMC12705795/
- SDT meta-analysis 2025, Current Opinion in Psychology: https://www.sciencedirect.com/science/article/pii/S2352250X25002076 (DOI 10.1016/j.copsyc.2025.102194)
- Lu et al. 2023, JMIR: https://www.jmir.org/2023/1/e49255 ; methodological concerns https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12428163/
- Wang et al. 2025, PNAS Nexus: https://academic.oup.com/pnasnexus/article/4/6/pgaf172/8151956
- Deception detection in politics 2021, Political Behavior: https://doi.org/10.1007/s11109-021-09747-1
- Traberg, Roozenbeek & van der Linden 2022 review: https://journals.sagepub.com/doi/full/10.1177/00027162221087936

Section D
- Garrett & Weeks 2013, CSCW: https://doi.org/10.1145/2441776.2441895 ; PDF https://rkellygarrett.com/wp-content/uploads/2014/05/Garrett-and-Weeks-Promise-and-peril-of-real-time-corrections.pdf
- Fridkin, Kenney & Wintersieck 2015, Political Communication: https://doi.org/10.1080/10584609.2014.914613
- Duke Reporters' Lab, Squash: https://reporterslab.org/2020/02/23/squash-report-card-improvements-during-state-of-the-union-and-how-humans-will-make-our-ai-smarter/ ; https://reporterslab.org/the-lessons-of-squash-our-groundbreaking-automated-fact-checking-platform/ ; https://www.niemanlab.org/2020/07/a-lesson-in-automated-journalism-bring-back-the-humans/ ; https://www.poynter.org/fact-checking/2020/how-the-duke-reporters-lab-used-the-political-conventions-to-perfect-its-automated-fact-checking-program/
- FactPopUp 2016: https://reporterslab.org/2016/10/17/reporters-lab-experiment-pop-fact-checking-debate/
- LiveFC 2024: https://arxiv.org/abs/2408.07448
- CBS 2024 VP debate QR code: https://www.seattletimes.com/business/want-to-check-that-fact-for-vp-debate-viewers-just-scan-the-code/

Section E
- Hassan et al. 2017, KDD (ClaimBuster): https://doi.org/10.1145/3097983.3098131 ; PDF https://ranger.uta.edu/~cli/pubs/2017/claimbuster-kdd17-hassan.pdf
- Konstantinovskiy et al. (Full Fact): https://arxiv.org/abs/1809.08193
- CheckThat! 2018 Task 1: https://arxiv.org/pdf/1808.05542
- CheckThat! 2019 Task 1: https://www.semanticscholar.org/paper/1d4cc805b65809ebbdee0bd9431de507a778797f
- CheckThat! 2020: https://arxiv.org/pdf/2007.07997
- CheckThat! 2021 Task 1: https://arxiv.org/pdf/2109.12987
- CheckThat! 2022 Task 1: https://ceur-ws.org/Vol-3180/paper-28.pdf
- CheckThat! 2023 Task 1: https://ceur-ws.org/Vol-3497/paper-019.pdf
- CheckThat! 2024 Task 1: https://ceur-ws.org/Vol-3740/paper-24.pdf
- CheckThat! 2025 lab overview and Task 1: https://ceur-ws.org/Vol-4038/paper_51.pdf ; https://arxiv.org/html/2503.14828v1
- CheckThat! 2026 Task 2 (numerical claims): https://checkthat.gitlab.io/clef2026/task2/ ; https://arxiv.org/pdf/2602.09516

Section F
- Thorne et al. 2018, FEVER shared task: https://arxiv.org/abs/1811.10971 ; https://aclanthology.org/W18-5501/
- AVeriTeC 2024 shared task: https://aclanthology.org/2024.fever-1.1/
- AVeriTeC 2025 shared task: https://aclanthology.org/2025.fever-1.15/ ; winner HerO2 https://aclanthology.org/2025.fever-1.16.pdf ; CTU AIC https://arxiv.org/html/2508.04390
- Ev2R: https://arxiv.org/abs/2411.05375
- Quelle & Bovet 2024, Frontiers in AI: https://doi.org/10.3389/frai.2024.1341697 ; arXiv https://arxiv.org/abs/2310.13549
- Wei et al. 2024, SAFE / LongFact: https://arxiv.org/abs/2403.18802 ; code https://github.com/google-deepmind/long-form-factuality
- QuanTemp 2024: https://arxiv.org/abs/2403.17169
- CheckThat! 2025 Task 3 (numerical claims): https://ceur-ws.org/Vol-4038/paper_53.pdf ; ClaimIQ https://arxiv.org/abs/2509.11492
- Walters & Wilder 2023, Scientific Reports: https://www.nature.com/articles/s41598-023-41032-5

Section G
- Da San Martino et al. 2019, EMNLP: https://aclanthology.org/D19-1565/
- SemEval-2020 Task 11: https://arxiv.org/abs/2009.02696 ; https://aclanthology.org/2020.semeval-1.186/
- SemEval-2023 Task 3: https://aclanthology.org/2023.semeval-1.317/ ; KInITVeraAI https://arxiv.org/abs/2304.11924
- Goffredo et al. 2022, IJCAI: https://www.ijcai.org/proceedings/2022/0575.pdf
- Goffredo et al. 2023, EMNLP: https://aclanthology.org/2023.emnlp-main.684.pdf ; code https://github.com/pierpaologoffredo/FallacyDetection
- MM-ArgFallacy2025 shared task and system paper: https://nlp-unibo.github.io/mm-argfallacy/2025/ ; https://arxiv.org/abs/2507.15641
- Dore, Damo, Cabrio & Villata 2026: https://arxiv.org/abs/2608.27471
- Jin et al. 2022, Findings of EMNLP: https://aclanthology.org/2022.findings-emnlp.532/
- Alhindi et al. 2022, EMNLP: https://aclanthology.org/2022.emnlp-main.560/
- Helwe et al. 2024, MAFALDA, NAACL: https://aclanthology.org/2024.naacl-long.270/ ; https://arxiv.org/abs/2311.09761
- Ruiz-Dolz & Lawrence 2023, ArgMining: https://aclanthology.org/2023.argmining-1.1/
- Pan et al. 2024, EMNLP: https://aclanthology.org/2024.emnlp-main.794.pdf ; https://arxiv.org/abs/2410.15050
- Ramponi, Daffara & Tonelli 2025, NAACL (Faina): https://arxiv.org/abs/2502.13853
- Sourati et al. 2023 (not retrieved): https://dl.acm.org/doi/10.24963/ijcai.2023/576

Section H
- Voxtral technical report: https://arxiv.org/abs/2507.13264
- Canary-1B-v2 / Parakeet-TDT-0.6B-v3 report: https://arxiv.org/abs/2509.14128
- ElevenLabs Scribe launch (vendor): https://elevenlabs.io/blog/meet-scribe
- Deepgram Nova-3 French (vendor): https://deepgram.com/learn/deepgram-expands-nova-3-with-spanish-french-and-portuguese-support
- Gladia Solaria-3 (vendor): https://www.gladia.io/blog/solaria-3-speech-to-text-model-for-european-languages
- AssemblyAI Universal-2 (vendor): https://www.assemblyai.com/research/universal-2
- WhisperX, Interspeech 2023: https://www.isca-archive.org/interspeech_2023/bain23_interspeech.pdf ; https://arxiv.org/abs/2303.00747
- Koenecke et al. 2024, FAccT: https://dl.acm.org/doi/10.1145/3630106.3658996 ; https://arxiv.org/abs/2402.08021
- pyannote speaker-diarization-3.1 model card: https://huggingface.co/pyannote/speaker-diarization-3.1
- Overlap in ETAPE (Orange / LIMSI): https://www.researchgate.net/publication/260933297_Impact_of_overlapping_speech_detection_on_speaker_diarization_for_broadcast_news_and_debates
- DIHARD III overview: https://arxiv.org/abs/2012.01477 ; Hitachi-JHU system https://arxiv.org/abs/2102.01363
- Whale multilingual ASR (Whisper fr 11.0% cited): https://arxiv.org/pdf/2506.01439
