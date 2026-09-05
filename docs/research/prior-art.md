# Prior art: transcript, position, claim and fallacy layers for French political speech

Research date: 2026-09-05. Scope: what already exists, in France and abroad, that overlaps with the four planned layers of the 2027 site — v1 searchable timestamped transcripts ("who said what, when"), v2 theme classification and candidate positioning, v3 checkable-claim extraction and rating, v4 timestamped rhetorical-technique / fallacy tagging — plus a live layer during debates and community correction of transcripts.

Every entry was checked against the project's own site, repo or docs where reachable. Entries where only press or search-engine snippets could be reached are marked UNVERIFIED. Pages that could not be fetched at all (paywalls, bot blocks: lemonde.fr, liberation.fr, factuel.afp.com, snopes.com, idir.claimbuster.org) are flagged in the notes.

## Executive summary

1. **Nobody in France publishes searchable, timestamped, speaker-attributed transcripts of 2027 candidates' TV/radio appearances.** The closest thing is larroumec.fr, a one-off post-hoc scan of the 27 August 2026 MEDEF/LCI debate (80 claims checked, "transcription intégrale attribuée par empreinte vocale", timestamps linked to the LCI replay) — but no data, no code, no licence, no rhetoric layer. Layer v1 is genuinely open ground.
2. **Layer v2 (positions by theme) is crowded but shallow.** At least eight 2027 comparators are live (MonVote2027, Observatoire 2027, ÉlyséeScope, compare2027, lespresidentielles.ai, iFRAP, chiffrex, scoly-oss). They summarise programmes; only Observatoire 2027 (3,796 sourced "relevés" across 16 candidates as of 3 Sept 2026) and MonVote2027 (100 questions, "données ouvertes") link positions to dated public statements, and none links to a verbatim timestamp. A transcript-anchored position layer would be new.
3. **Layer v3 (claims) is covered editorially, not structurally.** Décodeurs, CheckNews, AFP Factuel, Vrai ou Fake, Les Surligneurs, 20 Minutes Fake Off, France 24 Observateurs and Science Feedback are all active in 2026, but none exposes an open claim database or API; ClaimReview coverage in France is via Google's tool only, and the ClaimReview ecosystem itself is weakening (Correctiv left it in April 2026; FactStream is dead). The v3 gap is a *structured, open, per-utterance* claim registry — not more fact-checks.
4. **Layer v4 (fallacies) has no public French product anywhere.** Research assets exist (SemEval-2023 Task 3 includes French persuasion-technique spans; MAFALDA from Télécom Paris; DISPUTool 3.0 from Inria Sophia with a public demo on US debates; MM-ArgFallacy2025) but every deployed "fallacy detector" is an English browser extension or app. This layer would be first-of-its-kind in French.
5. **The live layer has been tried and documented as hard.** Duke's Squash (2017–2021) and Full Fact's Live/AI tools show the pipeline (ASR → claim detection → match against prior fact-checks → human gate); Squash's post-mortem lists ASR errors, an empty match database and idle-time UX as the killers. Full Fact AI and Factiverse Live are paid, closed products; Full Fact supports only three languages.
6. **Reusable French raw material:** DILA's Vie-publique "Collection des discours publics" (≈150k speeches since 1974, metadata under Licence Ouverte 2.0, full text on the site), Assemblée nationale and Sénat comptes rendus (Licence Ouverte, XML/Akoma Ntoso, full text with speakers), ParlaMint-FR (TEI, CLARIN), FREDSum (CC BY-SA 4.0 French debate transcripts from Linagora), "Parole de présidents" (CC BY 4.0, 9,202 texts).
7. **Reusable code:** WhisperX (BSD-2, French alignment + pyannote diarization), Hyperaudio Lite (MIT, word-level interactive transcripts), BBC react-transcript-editor / digital-paper-edit (correction UI, community-forked), Label Studio (Apache-2.0, timestamped audio/text spans), ELAN (GPLv3, tiered video annotation), Meedan Check (MIT, claim workflow + Alegre similarity), Open Parliament TV (open licences, Aeneas forced alignment of proceedings to video), QuotaClimat/Data For Good OME (MIT, Mediatree ASR ingest of French TV/radio).
8. **Partnership candidates in France:** Les Surligneurs + QuotaClimat's *Droit à l'Info* (launched 28 May 2026; monitors 18 TV/radio channels with automated narrative detection and human review; partners Science Feedback, Data For Good, Wikimédia France) — the only 2027-specific automated broadcast-monitoring effort found; De Facto (EDMO French hub, aggregates partner fact-checks, active Aug 2026); MieuxVoter (MIT-licensed 2027 polls repo with contribution workflow); INA (research-only corpora, restrictive GCU).
9. **Community-correction precedents:** Correctiv's Faktenforum (2,500+ registered citizens co-checking with staff; repos partly AGPL-3.0/MIT), CheckNews' reader-question model, MonVote2027's error-report loop, Wikipedia/Wikidata (Q111594692). No project lets the public correct *transcripts* of political speech; Open Parliament TV and larroumec do not either.
10. **Net verdict:** the combination (verbatim timestamped corpus → sourced positions → per-utterance claims → per-utterance rhetoric, all open-licensed and community-correctable) does not exist in France or, as one integrated public site, abroad. Individual pieces to reuse are listed per layer below; the two biggest external dependencies are broadcast access (INA/Mediatree/Arcom vs. YouTube replays) and a claim-matching database that is open enough to bootstrap live matching.

---

## Area 1 — France: fact-checking outlets, databases, institutional and civic data, 2027 initiatives

| Name | URL | What it does | Layers | Data access & licence | Active 2026? | Community / AI approach | Notes |
|---|---|---|---|---|---|---|---|
| Les Décodeurs (Le Monde) | https://www.lemonde.fr/les-decodeurs/ | Fact-checking desk (est. 10 March 2014, ~10 people). Décodex (Feb 2017) rates site reliability; browser extension reference dropped from lemonde.fr by Aug 2022. | v3 (editorial) | Articles paywalled; no API; Décodex search on site only. Copyright. | Yes (UNVERIFIED for 2026 – lemonde.fr blocked fetch; status from FR Wikipedia + search) | Journalist-only; no public AI/ASR tooling published | Décodex criticised for bias/coverage; database "not continuously updated" per third-party guides. |
| CheckNews (Libération) | https://www.liberation.fr/checknews/ | Reader-question "journalisme à la demande" since Sept 2017 (successor of Désintox); ~5,500 answered questions. | v3 (editorial) | No API/open data; paywalled. | Yes (UNVERIFIED – liberation.fr blocked fetch) | Community *asks*, journalists answer; De Facto partner. | Model worth copying for "ask us to check this utterance". |
| AFP Factuel | https://factuel.afp.com/ | AFP's French-language fact-check unit; IFCN verified signatory; Meta 3PFC partner; EuroClimateCheck member. | v3 (editorial) | ClaimReview markup on articles (via Google tools, UNVERIFIED for 2026); no public API. | Yes (site blocked fetch; IFCN profile confirms) | Journalists; AFP-Medialab maintains the open-source InVID-WeVerify verification plugin (MIT, commits to Apr 2026). | Largest FR fact-check producer. |
| Vrai ou Fake / Le vrai du faux (franceinfo) | https://www.franceinfo.fr/vrai-ou-fake/ ; https://www.franceinfo.fr/replay-radio/le-vrai-du-faux/ | Daily radio segment + web vertical checking politicians' statements and viral claims. | v3 (editorial) | No API; free web + radio replays. | Yes | Journalists only. | Public-service; likely live-debate coverage in 2027 but no structured output. |
| Les Surligneurs | https://lessurligneurs.eu/ ; https://lessurligneurs.eu/legal-checking/ | "Legal checking": lawyers/academics check the legal feasibility of politicians' proposals. IFCN signatory. Partnership with Public Sénat through the 2027 second round. | v3 (legal variant), v2 partially | Articles CC? (UNVERIFIED); no API. | Yes | Academic volunteers + editorial; runs *Droit à l'Info* (below). | Natural partner for a "legal feasibility" rating on proposals. |
| Droit à l'Info (Les Surligneurs × QuotaClimat) | https://droitalinfo.org/ | Early-warning detection of emerging disinformation narratives; monitors X/Instagram/Facebook/video/forums **and 18 TV/radio channels**; automated detection then "analyse humaine approfondie"; alerts on site + WhatsApp. Launched 28 May 2026 (climate-first 3-month validation, other topics from July 2026). "665 cas de désinformation climatique détectés dans l'audiovisuel en 2025." | v3, live-ish (monitoring, not real-time display) | No open data/API stated; no licence stated. | Yes (2027-specific) | Automated narrative extraction (tool unnamed); 4-expert scientific committee; partners Science Feedback, Data For Good, En Plateau, La Concorde fund, Wikimédia France. | Only 2027-specific automated broadcast monitor found. Partner candidate. |
| Fact & Furious | https://factandfurious.com/ | French independent fact-check blog (science/politics/media). | v3 | None. | Dormant — latest content seen 2021–2022 (UNVERIFIED) | Individual blogger. | Not a reuse candidate. |
| Politiscope | https://politiscope.fr/ | AI-generated political news summaries + a "comparateur de programmes présidentiels"; run by one author ("Emmanuel"). | v2 (weak) | None; no methodology. | Yes (posts dated 2–5 Sept 2026) | Explicitly LLM-generated content. | Low-trust; note the name collision with CNRS *Politoscope*. |
| Factare | https://factare.fr/ | AI fact-checking of YouTube videos, articles, text: splits into claims, 6-level verdict, "MFS" score 0–100, detects manipulation techniques; web app, Chrome extension, iOS. | v3, v4 (light: manipulation techniques on articles) | Public API documented at /docs/api, €0.12–0.30 per analysis; free tier 3/day. Closed source, © 2026. | Yes | Fully automated LLM pipeline ("API IA" + web search; OpenAI mentioned as fallback); methodology public (SIFT/CRAAP/lateral reading). | Closest French product to automated v3+v4, but proprietary and not political-speech specific. |
| Vera (LaReponse.tech) | https://www.askvera.org/en | Phone/WhatsApp fact-check assistant answering from 150+ IFCN/EFCSN fact-checkers and 350+ media; GPT-4 grounded on curated sources; France first. | v3 (retrieval over existing fact-checks) | No API stated. | Yes | Volunteer NGO; LLM RAG. Partners Science Feedback, Snopes, AFP Factuel, Conspiracy Watch. | Shows a French claim-matching corpus exists behind closed doors. |
| De Facto (EDMO French hub) | https://defacto-observatoire.fr/ | Aggregates fact-checks from AFP Factuel, Les Surligneurs, CheckNews, 20 Minutes etc.; EDMO monthly maps; "Désinfopédia" media-literacy resources. Runs on XWiki. | v3 (aggregation) | Searchable site; no API or ClaimReview feed stated; licence unstated. | Yes (content to Aug 2026) | Consortium (Sciences Po médialab/AFP/CLEMI/XWiki — UNVERIFIED on the page itself). | Best French aggregation point for a claim-matching seed. |
| Vie-publique.fr — Collection des discours publics (DILA) | https://www.vie-publique.fr/discours ; https://www.data.gouv.fr/datasets/discours-publics-metadonnees-de-vie-publique-fr | ≈150,000 speeches/interviews of President, PM, ministers, party and union leaders since 1974; full text on site; **data.gouv.fr dataset is metadata + URL only** (JSON, updated daily). | v1 (text-only, no audio timestamps) | Licence Ouverte / Open Licence 2.0 (metadata). Full-text reuse terms not stated in dataset; site content DILA. | Yes | Institutional; no community. | Primary text source for "what candidates said" when they held office; candidates who are not ministers (e.g. Mélenchon) are covered via interviews. Verify full-text reuse terms before scraping. |
| Assemblée nationale open data | https://data.assemblee-nationale.fr/ ; https://www.data.gouv.fr/datasets/comptes-rendus-des-debats-de-l-assemblee-nationale | Séance and commission comptes rendus, amendments, votes; XML/JSON; "au fil de l'eau" URLs + daily CSV lists (latency 1 min–1 day). DILA mirror on data.gouv.fr in XML, "all interventions with speaker attribution". | v1 (parliament) | Licence Ouverte (Etalab). | Yes (DILA mirror last updated 2 Aug 2026; "fréquence non respectée" flag) | Institutional. | Useful for MPs-turned-candidates (Attal, Retailleau, Le Pen…). |
| Sénat open data | https://data.senat.fr/ | Comptes rendus of public sessions since Jan 2003 (Akoma Ntoso XML), Ameli amendments, Dosleg, questions; PostgreSQL dumps + CSV. | v1 (parliament) | Sénat open licence (page-level). | Yes | Institutional. | Same use as AN. |
| NosDéputés.fr / NosSénateurs.fr (Regards Citoyens) | https://www.nosdeputes.fr/ ; https://www.regardscitoyens.org/nosdeputes-fr/ | Deputy activity: 870k interventions, presences, amendments; citizen comments on debates; API (JSON/XML/CSV). | v1 (parliament), community | CC BY-SA 2.0 FR. | **Partly** — last blog post July 2022 ("dernier ? tour"); covers 16th legislature; no evidence of 17th (2024–) coverage; nosdeputes.fr returned 503 during research (UNVERIFIED). | Volunteer civic-tech; open-source scrapers on GitHub. | Code (scrapers, parsers) reusable; org appears dormant. |
| La Fabrique de la Loi (Regards Citoyens × Sciences Po LIEPP) | https://www.regardscitoyens.org/la-fabrique-de-la-loi/ | Legislative process visualiser, 800+ laws; Python scrapers on GitHub. | – (law, not speech) | CC BY-SA 2.0 FR; code open. | Last major update 2018; status 2026 UNVERIFIED | Civic-tech. | Not directly relevant. |
| Politoscope (CNRS ISC-PIF, D. Chavalarias) | https://politoscope.org/ ; https://iscpif.fr/politoscope/ | Twitter/X political-community mapping for 2017 and 2022 campaigns (Gargantext theme classification, community detection); 2016–2023 study of far-right drift. | v2 (themes of tweets, not candidate positions) | No dataset/code licence stated; mobile app in 2017. | No 2027 activity found (pages stop at 2022); Twitter API access changed. UNVERIFIED for 2027. | Research lab. | Not a reuse candidate for speech; possible academic partner. |
| Le Grand Continent — Observatoire des élections; La Loupe Politique | https://legrandcontinent.eu/fr/elections/ ; https://www.loupepolitique.fr/ | Election data observatories (2.3M data points, 750+ charts). La Loupe Politique: 2027 polls aggregation + social audiences (X, Instagram, TikTok, YouTube) + Wikimedia pageviews. | – (polls/attention; no speech) | No API yet ("V4 – Diffuser" planned 2027). Licence unstated. | Yes | Editorial/data team; no AI stated. | Not overlapping; possible embed partner. |
| Observatoire 2027 | https://observatoire2027.fr/ | 3,796 dated, sourced position "relevés" across 16 candidates on 33 subjects (updated 3 Sept 2026); left-right "estimations analytiques". | v2 (strongest French instance) | No open data/API; licence unstated; portraits from Wikimedia Commons. | Yes | Unnamed operator; manual sourcing. | Closest existing v2; positions are not tied to verbatim timestamps. |
| MonVote2027 | https://monvote2027.fr/ ; https://monvote2027.fr/donnees | 100 questions × candidates on a 5-point scale, "sources vérifiables" per candidate page; "l'ensemble des positions en données ouvertes". Donation-funded, no ads. | v2 | "Données ouvertes" page; format/licence not stated (UNVERIFIED). | Yes | Error-report form → manual review. | Candidate for data exchange. |
| ÉlyséeScope 2027 | https://www.elyseescope.com/ | Candidate profiles, poll aggregation, programme comparison, RSS news every 20 min; newsletter "L'Éclaireur". | v2 | "Projet open source (AGPL-3.0)" stated on site; repo link not found (UNVERIFIED). | Yes | Aggregation from official sources; no AI stated. | Licence claim unverifiable without repo. |
| Compare 2027 (yp-edu) | https://www.compare2027.fr/ ; https://github.com/yp-edu/compare-2027 | Natural-language question → structured comparison; Next.js + Payload CMS + Vercel Postgres; sources are URLs to programmes, interviews, speeches, X posts, vote records. | v2 (LLM-assisted) | MIT; 15 commits. | Yes | Solo dev; MCP support; LLM unspecified. | Small; schema ideas reusable. |
| Les Présidentielles AI (DSIA Conseil) | https://www.lespresidentielles.ai/ | RAG chatbot over official programmes, Mistral + mistral-embed, hosted on French VPS. | v2 | Closed. | Yes | Commercial consultancy; LLM. | Programmes only, no speech. |
| iFRAP comparator | https://www.ifrap.org/comparateurs/presidentielles-2027 | Think-tank comparator, 9 themes / 34 domains; paraphrased positions, no dated citations. | v2 | Closed, © iFRAP. | Yes | Think-tank staff. | Partisan-leaning source; not reusable. |
| Chiffrex Élections 2027 | https://elections.chiffrex.fr/ | Candidate cards, IFOP polls, public statistics from data.gouv.fr, quiz. | v2 (weak) | © 2026, all rights reserved. | Yes | – | – |
| scoly-oss / presidentielles-2027 | https://scoly-oss.github.io/presidentielles-2027/ | Scores 8 candidates' programmes on 8 dimensions + "budget realism index". | v2 | GitHub Pages; repo returned 404 (UNVERIFIED). | UNVERIFIED | – | – |
| MieuxVoter / presidentielle2027 | https://github.com/MieuxVoter/presidentielle2027 | CSV/JSON compilation of 2027 polls with GitHub-Actions validation and contribution guide; 259 commits. | – (polls) | MIT. | Yes | Community PRs. | Good template for a community-maintained open dataset of French election data. |
| larroumec.fr — "Le débat Medef au scanner" | https://www.larroumec.fr/ | Post-hoc analysis of the 27 Aug 2026 MEDEF/LCI debate (7 candidates, 3h07): full transcript "attribuée par empreinte vocale", **timestamps linked to the LCI YouTube replay**, 80 claims checked against INSEE/COR/Eurostat/Sénat/Cour des comptes, weighted verdict scale (true 1 … false 0), speaking-time stats, "grille Larroumec" (8 economic axes, 0–3 each), targeting matrix, evasion scoring. | v1 (single event), v3, v2-lite | No data/code; "droit de courte citation"; no open licence. | One-off (Aug 2026) | Anonymous author; ASR + voiceprint attribution implied; manual checking. | Proof that the pipeline is feasible in 48 h; no rhetoric layer. |
| INA — dataset.ina.fr / INAthèque / "Les débats présidentiels" playlist | https://www.ina.fr/institut-national-audiovisuel/research/dataset-project ; https://inatheque.ina.fr/ ; https://www.youtube.com/playlist?list=PLSyeHqcFPtDA-SJVWIhmgg6UaDj8yRhRi | Research corpora (10 sub-corpora incl. spINAch 330 h, InaGVAD) for registered research entities only, 2-year access, no redistribution, no cloud; no political-debate transcript corpus. INAthèque consultation on site. Public YouTube playlist of historic presidential debates. | v1 (audio source, restricted) | Research-only GCU; not open. | Yes | Institutional; VoxSigma ASR used internally. | Not usable for a public site; useful for academic partnership. |
| FREDSum (Linagora) | https://github.com/linagora-labs/FREDSum ; hdl.handle.net/11403/fredsum | Transcripts + extractive/abstractive summaries of French political debates (EMNLP Findings 2023); standardized speaker tags; HF + Ortolang. | v1 (historic corpus) | CC BY-SA 4.0. | Yes (maintained) | Research; manual transcripts. | Reusable for evaluation/bootstrap of the transcript layer. |
| Parole de présidents 1958–2022 (Labbé & Savoy) | https://arxiv.org/abs/2411.18468 | 9,202 presidential texts, 20M labelled words. | v1 (text) | CC BY 4.0. | Published Nov 2024 | Academic. | Stylometry baseline. |
| ParlaMint-FR (CLARIN) | https://www.clarin.si/repository/xmlui/handle/11356/2004 ; https://github.com/clarin-eric/ParlaMint | TEI-encoded Assemblée nationale debates in ParlaMint 5.0 (July 2025), with plain-text and TSV metadata, MT to English. | v1 (parliament) | CLARIN open licences (CC BY, UNVERIFIED per-corpus). | Yes | Research consortium. | Schema (Parla-CLARIN TEI) is a candidate transcript format. |
| CLAPI / ORTOLANG / CEFC-ORFEO | http://clapi.ish-lyon.cnrs.fr/ ; https://www.ortolang.fr/ | Spoken-French interaction corpora; ORTOLANG hosts FREDSum. | v1 (linguistic) | CC licences. | Yes | Academic. | Not political per se. |
| QuotaClimat × Data For Good — Observatoire des Médias sur l'Écologie | https://github.com/dataforgoodfr/quotaclimat | Ingests **Mediatree** speech-to-text of French TV/radio via API, web-press sitemaps, DE/BE SRTs; keyword/theme detection with stop-word filtering; Label Studio annotations for climate fact-checking; Python/Postgres/dbt/Metabase; 2,471 commits. Partners ADEME, Arcom. | live monitoring infrastructure (v1-adjacent) | MIT. | Yes | Volunteer data scientists + NGO; ASR is commercial (Mediatree). | Most directly reusable French broadcast-monitoring codebase; Mediatree access is the constraint. |
| Wikipédia / Wikidata | https://fr.wikipedia.org/wiki/Élection_présidentielle_française_de_2027 ; https://www.wikidata.org/wiki/Q111594692 | Election and candidacies articles; Wikidata item Q111594692; polls list. | v2-lite (candidate metadata) | CC BY-SA 4.0 / CC0 (Wikidata). | Yes | Community wiki. | Use Wikidata QIDs as candidate identifiers; Wikimédia France is a Droit à l'Info partner. |
| IFCN French signatories | https://ifcncodeofprinciples.poynter.org/ | Verified: AFP Factuel/AFP Fact Check, 20 Minutes Fake Off, France 24 Les Observateurs, Les Surligneurs, Science Feedback. | v3 | – | Yes | – | Signatories page itself did not render; profiles verified individually. |
| HoaxBuster, Conspiracy Watch | – | Older FR hoax archive; conspiracism observatory (Vera partner). | v3 | – | UNVERIFIED | – | Peripheral. |

**Not found:** any French site with per-utterance claim IDs, any French fallacy tagger, any live overlay during the MEDEF debate (franceinfo ran a live blog; larroumec published after the fact).

---

## Area 2 — International fact-checking, claim detection and infrastructure

| Name | URL | What it does | Layers | Data access & licence | Active 2026? | Community / AI approach | Notes |
|---|---|---|---|---|---|---|---|
| Full Fact (UK) — Full Fact AI | https://fullfact.org/ai/ ; https://github.com/FullFact | Claim detection (BERT sentence classifier, "hundreds of thousands → tens of thousands"), claim matching (ML + generative), ingest from news sites, **live TV speech**, podcasts, social, Hansard; historical "Live" and "Trends" tools (Omidyar/OSF-funded 2017). 40+ orgs, 12 elections in 2024. | v3, live | **Paid licence**, closed; 3 languages, 30 countries (French not listed). GitHub: ClaimReview WordPress plugin, pastel/genai-utils (Apache-2.0, Aug 2026), no claim-detection code. | Yes | Human-in-the-loop; explicit "human experts aren't going anywhere". | Reference architecture; not reusable as code. |
| Duke Reporters' Lab — ClaimBuster, Squash, FactStream, Tech & Check | https://reporterslab.org/tech-and-check/ ; https://reporterslab.org/the-lessons-of-squash-our-groundbreaking-automated-fact-checking-platform/ | ClaimBuster (UTA) scores check-worthiness; Tech & Check Alerts email daily claims from transcripts; Squash (2017–2021): Google Cloud ASR → ClaimBuster → ClaimReview DB match → "Gardener" human filter → on-screen pop-up. FactStream app **stopped 31 Dec 2024**. | v3, live | ClaimBuster API existed at idir.uta.edu (site returned 503; English-only, key-based — UNVERIFIED for 2026). Squash code not published. | Squash ended 2021; Tech & Check Alerts status UNVERIFIED; 2026 census (437 projects) still published. | Academic + student; human gate essential. | Post-mortem lists: ASR errors, too few prior fact-checks to match, bad matches without topic tagging, idle-time UX. |
| Google Fact Check Tools / ClaimReview / Data Commons | https://developers.google.com/fact-check/tools/api ; https://schema.org/ClaimReview ; https://datacommons.org/factcheck/ | Claim Search API (API key) over Fact Check Explorer; ClaimReview Read/Write API (Search Console auth); Data Commons ClaimReview DataFeed download "updated on a frequent and regular basis". Schema: claimReviewed, itemReviewed(Claim + appearance), reviewRating, author, datePublished; MediaReview sibling. | v3 (schema + corpus) | Google API ToS; feed licence unstated. French fact-checks present (UNVERIFIED count). | Yes, but Google "scaled back central functions" per Correctiv (Apr 2026). | – | Still the only cross-publisher claim corpus; risk of further deprecation. |
| Correctiv (DE) — Faktencheck & Faktenforum | https://correctiv.org/faktencheck/ ; https://www.faktenforum.org/ ; https://github.com/faktenforum | **Left ClaimReview on 2 Apr 2026** to build "eigene, resiliente Infrastruktur". Faktenforum (Nov 2024): community fact-checking platform, 2,500+ registered citizens research with staff; structured claim DB used for ML; Checkbot / Wolf-Schneider-KI assistants (human-in-the-loop). | v3, community | GitHub org: correctiv-app (AGPL-3.0, updated 5 Sept 2026), search "RAG service for fact-checking" (MIT), LibreChat fork, MCP servers. Platform itself partly open (UNVERIFIED which parts). | Yes | Strongest community-contribution model in Europe. | Direct model for community claim work; codebase worth reading. |
| Meedan Check | https://github.com/meedan/check | Collaborative media annotation/fact-check workflow: check-api (Rails), check-web, Alegre (similarity/claim matching), Pender, tipline bots. | v3 workflow, community | MIT; self-hostable (dev compose only; "do not use in production" for that repo). | Yes (580 commits develop) | Tiplines + newsroom workflow; Alegre ML similarity. | Heavy stack; Alegre's matching is reusable. |
| Factiverse (NO) | https://www.factiverse.ai/ | Gather (monitor video/audio for political claims), **Factiverse Live**, API, AI Editor, FactiSearch DB; "110+ languages"; users NRK, SVT. | v3, live | Commercial, patented; no open data. | Yes | Proprietary AI; EU/TU Delft/Stavanger research. | Benchmark for live product UX. |
| Newtral (ES) — ClaimHunter / ClaimCheck | https://www.newtral.es/claimcheck-herramienta-mentiras-repetidas/20221221/ ; https://ceur-ws.org/Vol-2877/paper3.pdf | ClaimHunter: XLM-R/BERT claim detection on politicians' tweets and **audio transcripts** (F1 ≈0.8, 10× reviewed claims); ClaimCheck (with ABC Australia/LSE JournalismAI): multilingual repeated-claim matching alerts. | v3 | Internal tools; no public API found (UNVERIFIED). | Yes (org active) | Journalist feedback loop retrains model. | Spanish/Catalan/Galician; multilingual design applicable to French. |
| Maldita.es (ES) | https://github.com/MalditaEs ; https://fundacionmaldita.es/en/ | WhatsApp chatbot crowdsourcing; Disinformation Management System DB; AI search over articles; DEWARD early warning. | v3, community | GitHub: EuroClimateCheck ClaimReview WordPress plugins (2024–25), wikidata-extractor (MIT); core platform closed. | Yes | Community tips + staff; JournalismAI grants. | Plugins show ClaimReview export patterns. |
| Faktisk.no / Faktisk Verifiserbar (NO) | https://en.wikipedia.org/wiki/Faktisk.no | Co-owned by NRK/Schibsted/Dagbladet; Verifiserbar (12 media houses) trains OSINT, "all AI tools open-source on GitHub" (per GIJN). | v3 | Specific repos not located (UNVERIFIED). | Yes | Cross-newsroom consortium — model for a French media coalition. | – |
| Snopes (US) | https://www.snopes.com/ | Oldest general fact-checker; ratings; Vera partner. | v3 | No API (site blocked fetch; UNVERIFIED). | Yes | Reader tips. | Not political-speech focused. |
| PolitiFact (Poynter, US) | https://www.politifact.com/ | Truth-O-Meter ratings of politicians' statements, per-person scorecards; RSS; api.politifact.com is a legacy article host, **no public API**. | v3, v2-lite (scorecards) | Copyright; ClaimReview markup. | Yes | Staff; state partners. | Scorecard UX (per-candidate truth distribution) is worth copying. |
| FactCheck.org (Annenberg) | https://www.factcheck.org/ | ~250 stories/yr; live debate process: flag 12–15 claims in real time, publish 8–10 false ones after. | v3, live-ish | Copyright; no API. | Yes (Sept 2026) | Staff. | – |
| IFCN / EFCSN / EDMO | https://ifcncodeofprinciples.poynter.org/ ; https://efcsn.com/ ; https://efcsn.com/factcricis | Standards bodies. EFCSN (Paris, 60+ members) ran EuroClimateCheck / FactCRICIS: 1,100+ climate fact-checks, 80k data points, 25 orgs/15 countries (AFP, Science Feedback for France); researcher/journalist access by application, "API for custom analysis" (project ended late 2025). | v3 (governance, shared DB) | Application-based; licence unstated. | Yes | – | Template for a shared French claim DB; potential data partner. |
| CLEF CheckThat! lab | https://arxiv.org/abs/2602.09516 (2026) ; https://arxiv.org/abs/2503.14828 (2025) | Shared tasks: check-worthiness/subjectivity, claim normalisation, numerical & temporal claim verification, previously-fact-checked-claim retrieval (SemEval-2025 T7), 20+ languages. | v3 (models/data) | Task datasets, research licences. | Yes (2026 edition) | Academic. | Source of multilingual check-worthiness models applicable to French. |
| vera.ai / InVID-WeVerify plugin (AFP-Medialab) | https://www.veraai.eu/ ; github.com/AFP-Medialab/verification-plugin | EU Horizon project (GA 101070093); browser plugin for image/video verification, MIT, v0.87 July 2025, commits to Apr 2026; Truly Media/EDMO integration. | media verification (not speech) | MIT. | Yes | French agency lead (AFP). | Peripheral but shows AFP's open-source appetite. |
| Logically (UK) | https://en.wikipedia.org/wiki/Logically_(company) | AI disinformation analytics + Logically Facts; lost IFCN cert, Meta/TikTok contracts; **pre-pack administration July 2025**, assets to Kreatur Ltd. | v3 | Closed. | Effectively no (as fact-checker) | – | Cautionary tale on platform-dependent funding. |
| Bot Sentinel (US) | https://botsentinel.com/ | Inauthentic-account detection on X; v3.0 Nov 2025, relaunch May 2026. | – | Closed. | Yes (UNVERIFIED depth) | – | Not speech-related. |
| Open-source fact-verification pipelines (Loki/OpenFactVerification, OpenFactCheck, live-fact-checker) | https://github.com/Libr-AI/OpenFactVerification ; https://github.com/yuxiaw/OpenFactCheck ; https://github.com/alandaitch/live-fact-checker | LLM pipelines: claim decomposition → check-worthiness → retrieval → verdict; live-fact-checker does YouTube/stream transcription + Gemini grounding. | v3, live (prototype) | Open source (licences vary; UNVERIFIED individually). | Yes | – | Prototyping shortcuts; not production-grade. |

---

## Area 3 — Political speech transcript databases

| Name | URL | What it does | Layers | Data access & licence | Active 2026? | Community / AI approach | Notes |
|---|---|---|---|---|---|---|---|
| The American Presidency Project (UCSB) | https://www.presidency.ucsb.edu/ | Presidential documents, speeches, **debate transcripts** since 1960; run by Woolley & Peters since 1999. | v1 (text, no timestamps) | Web only; no API/bulk; ToS. | Yes | Academic curation. | Gold-standard canonical archive, but text-only. |
| Factba.se (Roll Call / FiscalNote) | https://rollcall.com/factbase/trump/transcripts | Searchable transcripts of every Trump/Biden speech, interview, briefing (2026 items present); founded 2017 by FactSquared; acquired by FiscalNote 2021. | v1 (search, speaker, often video-synced) | Free search; paid analytics; proprietary. | Yes | ASR + human; proprietary. | Closest commercial analogue to v1; note it is single-politician. |
| Rev.com transcript library / CPD debates.org / jamesmartherus/debates | https://www.rev.com/category/politics ; https://www.debates.org/voter-education/debate-transcripts/ ; https://github.com/jamesmartherus/debates | Free machine/human transcripts of US debates with timestamps and speakers (marketing for Rev's ASR); CPD official transcripts; tidy CSV compilation on GitHub. | v1 | Rev: free to read, copyright; GitHub: open (licence UNVERIFIED). | Yes | Vendor + volunteers. | Timestamped-speaker-turn format worth copying. |
| TheyWorkForYou / ParlParse (mySociety, UK) | https://www.theyworkforyou.com/api/ ; https://github.com/mysociety/parlparse | Hansard → XML scrapers (4,274 commits), API (debates, members, constituencies) from £20/month, free/reduced for non-profits. | v1 (parliament) | Open-source scrapers; data from Parliament (Open Parliament Licence). | Yes | Charity; citizen email alerts. | Reference for parliamentary transcript UX; French equivalent (NosDéputés) is dormant. |
| Open Parliament TV (DE) | https://openparliament.tv/ ; https://github.com/OpenParliamentTV | Bundestag video search: official proceedings **force-aligned to video with Aeneas** (synthetic TTS vs waveform, language-agnostic), Wikidata entities, DIP API; hosted by Center for the Cultivation of Technology; live Oct 2021. | v1 (video + timestamped text) | All components "openly licensed"; proceedings public domain. | Yes | Non-profit; no citizen correction found. | **Most reusable architecture for v1**: align official/verified text to video rather than trusting ASR. |
| ParlaMint (CLARIN) | https://github.com/clarin-eric/ParlaMint | 29 corpora incl. FR, TEI/Parla-CLARIN, v5.0 July 2025. | v1 | Open CLARIN licences. | Yes | Research. | Schema reuse. |
| Internet Archive TV News Archive / GDELT Television API | https://archive.org/details/tv ; https://blog.gdeltproject.org/gdelt-2-0-television-api-debuts/ | Closed-caption search of 163 stations since 2009 in 15-second windows; AI Television Explorer; mostly US + selected international (BBC, DW, Al Jazeera) — **no French channels confirmed**. | v1, live-adjacent | Free API; captions are station-owned. | Yes | Institutional. | Shows the "15-second window" search pattern; France lacks an equivalent public caption archive (INA is closed). |
| PolInterviews (DE) | https://arxiv.org/html/2501.04484 | Dataset of German politicians' public-broadcast interviews (Harvard Dataverse). | v1 | Open (Dataverse). | 2025 | Academic. | Template for an interview corpus. |
| French corpora (Vie-publique, AN/Sénat, FREDSum, Parole de présidents, ParlaMint-FR, INA) | see Area 1 | – | v1 | – | – | – | Listed in Area 1 to avoid duplication. |

---

## Area 4 — Fallacy / propaganda-technique detection available to the public

| Name | URL | What it does | Layers | Data access & licence | Active 2026? | Community / AI approach | Notes |
|---|---|---|---|---|---|---|---|
| SemEval-2020 Task 11 / SemEval-2021 Task 6 (QCRI "Tanbih"/Prta) | https://tanbih.qcri.org/ ; https://tanbih.qcri.org/demos/ | Span-level propaganda-technique detection in news (14/18 techniques), memes (2021). Tanbih article-analysis demo "examines your news article for bias, propagandistic language, and possibly incorrect claims"; API hub apihub.tanbih.org. Prta demo not found on current site (UNVERIFIED whether still online). | v4 (text, news) | Datasets research-licensed; English (+Arabic). | Partly | Academic. | Taxonomy origin for most later work. |
| SemEval-2023 Task 3 (Piskorski et al.) | https://propaganda.math.unipd.it/semeval2023task3/ ; https://aclanthology.org/2023.semeval-1.317/ ; https://github.com/kinit-sk/semeval2023-task3-persuasion-techniques | Genre, framing and **23 persuasion techniques with spans in 9 languages incl. French** (26,663 train/dev paragraphs in 6 languages). KInIT fine-tuned XLM-R models on GitHub. | v4 (text, French available) | Research use; models open. | Data/models static | Academic. | **Best starting point for French v4 models.** |
| MAFALDA (Télécom Paris, Helwe et al., NAACL 2024) | https://github.com/ChadiHelwe/MAFALDA | Unified fallacy taxonomy + benchmark with manual explanations; subjectivity-aware evaluation; zero-shot LLM baselines. | v4 (taxonomy/eval) | GitHub (licence UNVERIFIED); English. | Yes (static) | French academic team. | Adopt taxonomy; authors are Paris-based potential partners. |
| ElecDeb60to20 / MM-USED-fallacy / MM-ArgFallacy2025 (Univ. Bologna, Inria) | https://github.com/pierpaologoffredo/ElecDeb60to20 ; https://nlp-unibo.github.io/mm-argfallacy/2025/ | US presidential debates 1960–2020 annotated for 6 fallacies (Ad Hominem, Appeal to Authority, Appeal to Emotion, False Cause, Slippery Slope, Slogan); 18,910 utterances, 1,457 fallacious; **text+audio** shared task at ACL 2025 ArgMining; data via MAMKit (audio rebuilt dynamically for copyright). | v4 (debate, multimodal) | Open research data; audio not redistributed. | Yes (2025 task) | Academic. | Exactly the v4 task on debates — in English. |
| DISPUTool 3.0 (Inria/Univ. Côte d'Azur, ACL 2025 demo) | https://aclanthology.org/2025.acl-demo.45/ ; https://3ia-demos.inria.fr/disputool/ | Web app: argument mining + **fallacy detection and automatic "repair"** on US debates; public demo. | v4 (public demo) | Code availability UNVERIFIED; English. | Yes | French lab (Cabrio, Villata). | Nearest public v4 demo; French partner. |
| Argotario (UKP Darmstadt) | https://github.com/UKPLab/argotario | Multilingual serious game on fallacies (2017); site domain expired; English data CC0. | v4 (education) | CC0 data; code archived. | No | Crowd game. | Gamified annotation idea for community fallacy tagging. |
| Logical-fallacy browser extensions / apps (FallacyCheck, Fallacy Detector (Claude-based, YouTube support), FallacyFilter, Skeptik (ASU), Skeptic Reader, logicalfallacies.org, Google Play "Logical Fallacy Detector") | https://dl.acm.org/doi/10.1145/3771882.3774253 ; https://chromewebstore.google.com/detail/fallacy-detector/hldpaimaggankhhbgkndneaacgkojfkd ; https://www.logicalfallacies.org/fallacy-detector/ | LLM prompts over page text; 9–16 fallacy types; some process YouTube transcripts. | v4 (consumer, text) | Closed, English-centric. | Yes | Pure LLM; 2025 study: "most LLMs exhibit limited performance in fallacy detection". | No French, no timestamps, no political focus. |
| CoCoLoFa, FALCON, LOGIC, MISSCI | https://arxiv.org/pdf/2410.03457 ; https://dl.acm.org/doi/pdf/10.1145/3672608.3707913 | Additional fallacy datasets (news comments, multi-label graphs, science misrepresentation). | v4 (data) | Research. | – | – | Secondary. |
| Factare (see Area 1) | https://factare.fr/ | Detects "techniques de manipulation" in articles/videos in French. | v4-lite | API paid. | Yes | LLM. | Only French commercial v4-ish. |

**Not found:** any public tool tagging rhetorical techniques on *timestamped political audio/video in French*. Bot Sentinel and Logically are not fallacy tools.

---

## Area 5 — Reusable civic-tech / open-source building blocks

| Name | URL | What it does | Layers | Data access & licence | Active 2026? | Community / AI approach | Notes |
|---|---|---|---|---|---|---|---|
| WhisperX (+ pyannote) | https://github.com/m-bain/whisperX | Whisper batched ASR (70× realtime), wav2vec2 word-level alignment incl. **French**, pyannote speaker diarization; faster-whisper backend. | v1 (ASR) | BSD-2-Clause; pyannote models gated. | Yes (558 commits) | – | Default ASR stack; expect proper-noun errors (cf. Squash). |
| Aeneas forced alignment (via Open Parliament TV) | https://github.com/OpenParliamentTV/OpenParliamentTV-Tools | Align verified text to audio via synthetic TTS + DTW; language-agnostic. | v1 (alignment) | Open. | Yes | – | Use when an official/corrected transcript exists. |
| Hyperaudio Lite / Hyperaudio Lite Editor | https://github.com/hyperaudio/hyperaudio-lite | 10 KB dependency-free interactive transcript (click-to-seek, search, share timestamped selections); editor creates timed transcripts; converters from SRT/Speechmatics/Gentle/Google STT JSON. | v1 (UI) | MIT. | Yes (480 commits, open PRs) | – | Front-end for v1 and for anchoring v3/v4 tags to words. |
| BBC digital-paper-edit / react-transcript-editor | https://github.com/bbc/digital-paper-edit-client | React transcript correction + paper-edit; BBC no longer maintains (moved to Firebase version); community fork continues. | v1 (correction UI) | BBC licence (see LICENCE.md; UNVERIFIED terms). | Archived | – | Correction UI patterns for community edits. |
| oTranscribe (MuckRock) | https://github.com/oTranscribe/oTranscribe | Browser transcription editor, .otr format, YouTube support. | v1 (manual) | MIT. | Yes (maintained by MuckRock) | – | Lightweight fallback. |
| Audapolis | https://github.com/bugbakery/audapolis | Word-processor-like transcript-based media editor with local ASR. | v1 | AGPL-3.0. | Activity UNVERIFIED | – | Desktop only. |
| Amara (PCF) | https://amara.org/ | Collaborative subtitling; **closed source since Jan 2020** (last AGPL code on GitLab). | v1 (crowd subtitling) | Proprietary now. | Yes | Community subtitling model. | Workflow model, not code. |
| ELAN (MPI Psycholinguistics) | https://archive.mpi.nl/tla/elan | Tiered audio/video annotation, EAF XML; v7.0 (2025). | v4 (expert annotation) | GPLv3. | Yes | – | For building gold fallacy annotations; EAF → JSON export. |
| Label Studio | https://github.com/HumanSignal/label-studio | Audio/video timestamp regions + text spans, templates, self-host. | v3/v4 (annotation) | Apache-2.0. | Yes | Multi-annotator. | Already used by QuotaClimat for fact-check labels. |
| Doccano | https://github.com/doccano/doccano | Text classification / sequence labelling, collaborative. | v2/v3/v4 (text annotation) | MIT. | Yes | – | Simpler than Label Studio; no audio. |
| Hypothesis (h) | https://github.com/hypothesis/h | Web annotation server + client; self-host via Docker. | community annotation | BSD-2-Clause. | Yes (18.9k commits) | – | Could host public comments on transcript passages. |
| Meedan Check / Alegre | see Area 2 | Claim workflow + similarity. | v3 | MIT. | Yes | – | – |
| Full Fact / Maldita ClaimReview WordPress plugins | https://github.com/FullFact/claim-review-schema-wordpress-plugin ; https://github.com/MalditaEs | ClaimReview JSON-LD emitters. | v3 (schema) | Open (licences vary). | Static | – | Copy the JSON-LD shape even if not on WordPress. |
| QuotaClimat OME | see Area 1 | French broadcast ingest + keyword detection. | live | MIT. | Yes | – | – |
| Wikimedia approaches | https://www.wikidata.org/wiki/Q111594692 | Wikidata QIDs for candidates/events; wiki edit-history model for community correction; Wikimédia France collaborates with Droit à l'Info. | community | CC0 / CC BY-SA. | Yes | Open editing with history and talk pages. | Adopt "every edit is attributed and revertible" for transcript corrections. |

---

## Gaps and reuse map (by layer)

- **v1 transcripts:** nothing public in France. Build on WhisperX + pyannote (or Aeneas when a verified text exists), store in a ParlaMint/TEI-compatible schema with word timings, front with Hyperaudio Lite, correction UI inspired by react-transcript-editor, edit history à la Wikipedia. Source video via broadcaster YouTube replays (as larroumec did); INA and Mediatree are closed/commercial.
- **v2 positions:** many comparators; partner with Observatoire 2027 / MonVote2027 for exchange, but anchor each position to a transcript timestamp — none does this today. Use Wikidata QIDs.
- **v3 claims:** editorial fact-checkers are the raters; the missing piece is an open per-utterance claim registry emitting ClaimReview JSON-LD *and* an independent feed (Correctiv's lesson). Seed matching from Data Commons feed + De Facto + EFCSN data; check-worthiness models from CheckThat!/Full Fact-style BERT; keep a human gate (Squash "Gardener").
- **v4 rhetoric:** train/fine-tune from SemEval-2023 T3 (French spans) with MAFALDA/ElecDeb taxonomies; expert gold set in ELAN/Label Studio; consider a partnership with Inria (DISPUTool) or Télécom Paris (MAFALDA). No competitor.
- **Live:** feasible as "match against already-published checks + flag check-worthy" (Full Fact/Squash pattern); real-time verdicts are not credible. Budget for ASR latency and proper-noun errors.
- **Community:** CheckNews (ask), Faktenforum (co-research), MonVote2027 (report), Wikipedia (edit) — combine ask + edit with attribution.

---

## Sources

French outlets, institutions, 2027 initiatives
- https://fr.wikipedia.org/wiki/Les_D%C3%A9codeurs
- https://www.lemonde.fr/les-decodeurs/ (fetch blocked)
- https://www.liberation.fr/checknews/ (fetch blocked)
- https://factuel.afp.com/ (fetch blocked)
- https://ifcncodeofprinciples.poynter.org/application/public/afp-fact-checking/661a8b0eba7689d4814295f9
- https://ifcncodeofprinciples.poynter.org/application/public/les-surligneurs/58CCEC03-DAB8-F468-A61E-21F6937F27CC
- https://ifcncodeofprinciples.poynter.org/application/public/france-24-les-observateurs/661a8b02ba7689d481416604
- https://ifcncodeofprinciples.poynter.org/profile/science-feedback
- https://www.franceinfo.fr/vrai-ou-fake/
- https://www.franceinfo.fr/replay-radio/le-vrai-du-faux/
- https://lessurligneurs.eu/legal-checking/
- https://lessurligneurs.eu/presidentielle-2027-les-surligneurs-lancent-avec-quotaclimat-un-dispositif-de-detection-precoce-de-la-desinformation/
- https://droitalinfo.org/
- https://www.publicsenat.fr/partenariat-avec-le-collectir-les-surligneurs-autour-du-legal-checking
- https://factandfurious.com/
- https://politiscope.fr/
- https://factare.fr/
- https://factare.fr/blog/outils-verification-information
- https://www.askvera.org/en
- https://defacto-observatoire.fr/
- https://www.vie-publique.fr/discours
- https://www.data.gouv.fr/datasets/discours-publics-metadonnees-de-vie-publique-fr
- https://data.assemblee-nationale.fr/foire-aux-questions
- https://www.data.gouv.fr/datasets/comptes-rendus-des-debats-de-l-assemblee-nationale
- https://data.senat.fr/
- https://www.regardscitoyens.org/
- https://www.regardscitoyens.org/nosdeputes-fr/
- https://www.regardscitoyens.org/la-fabrique-de-la-loi-reprend-du-service/
- https://politoscope.org/le-politoscope/
- https://iscpif.fr/politoscope/
- https://legrandcontinent.eu/fr/elections/
- https://www.loupepolitique.fr/
- https://observatoire2027.fr/
- https://monvote2027.fr/comparer
- https://monvote2027.fr/donnees
- https://www.elyseescope.com/
- https://www.elyseescope.com/sources
- https://www.compare2027.fr/
- https://github.com/yp-edu/compare-2027
- https://www.lespresidentielles.ai/
- https://www.ifrap.org/comparateurs/presidentielles-2027
- https://elections.chiffrex.fr/
- https://scoly-oss.github.io/presidentielles-2027/
- https://github.com/MieuxVoter/presidentielle2027
- https://www.larroumec.fr/
- https://lcp.fr/actualites/presidentielle-2027-ce-qu-il-faut-retenir-du-premier-debat-entre-les-candidats-440670
- https://www.franceinfo.fr/elections/presidentielle/direct-attal-le-pen-melenchon-philippe-suivez-le-premier-debat-de-la-presidentielle-organise-par-le-medef-entre-sept-candidats-declares_8162033.html
- https://www.ina.fr/institut-national-audiovisuel/research/dataset-project
- https://inatheque.ina.fr/appel-a-chercheures-20262027
- https://www.youtube.com/playlist?list=PLSyeHqcFPtDA-SJVWIhmgg6UaDj8yRhRi
- https://github.com/linagora-labs/FREDSum
- https://aclanthology.org/2023.findings-emnlp.280/
- https://arxiv.org/abs/2411.18468
- https://www.clarin.si/repository/xmlui/handle/11356/2004
- https://github.com/clarin-eric/ParlaMint
- http://clapi.ish-lyon.cnrs.fr/
- https://github.com/dataforgoodfr/quotaclimat
- https://www.wikidata.org/wiki/Q111594692
- https://fr.wikipedia.org/wiki/%C3%89lection_pr%C3%A9sidentielle_fran%C3%A7aise_de_2027

International fact-checking and infrastructure
- https://fullfact.org/ai/
- https://fullfact.org/blog/2025/feb/how-ai-can-help-fact-checkers/
- https://github.com/FullFact
- https://reporterslab.org/tech-and-check/
- https://reporterslab.org/the-lessons-of-squash-our-groundbreaking-automated-fact-checking-platform/
- https://www.poynter.org/fact-checking/2026/fact-checking-projects-survive-funding-cuts-duke-census/
- https://developers.google.com/fact-check/tools/api
- https://schema.org/ClaimReview
- https://datacommons.org/factcheck/
- https://correctiv.org/in-eigener-sache/2026/04/02/correctiv-steigt-aus-der-internationalen-faktencheck-infrastruktur-claimreview-aus-was-jetzt-folgt/
- https://correctiv.org/projekte/faktenforum/
- https://www.faktenforum.org/ueber-uns
- https://github.com/faktenforum
- https://github.com/meedan/check
- https://www.factiverse.ai/
- https://www.newtral.es/claimcheck-herramienta-mentiras-repetidas/20221221/
- https://ceur-ws.org/Vol-2877/paper3.pdf
- https://github.com/MalditaEs
- https://fundacionmaldita.es/en/
- https://en.wikipedia.org/wiki/Faktisk.no
- https://gijn.org/stories/how-generative-ai-helps-fact-checkers/
- https://www.politifact.com/
- https://api.politifact.com/article/
- https://www.factcheck.org/
- https://penntoday.upenn.edu/news/after-political-debates-factcheckorg-tells-true-story
- https://efcsn.com/factcricis
- https://efcsn.com/news/2025-05-23_euroclimatecheck-opens-researcher-access-to-climate-fact-check-database/
- https://arxiv.org/abs/2602.09516
- https://arxiv.org/abs/2503.14828
- https://www.veraai.eu/posts/verification-plugin
- https://www.uktech.news/ai/ai-fact-checker-logically-sold-off-in-administration-deal-20250707
- https://en.wikipedia.org/wiki/Logically_(company)
- https://botsentinel.com/
- https://github.com/Libr-AI/OpenFactVerification
- https://github.com/yuxiaw/OpenFactCheck
- https://github.com/alandaitch/live-fact-checker

Transcript databases
- https://www.presidency.ucsb.edu/about
- https://rollcall.com/factbase/trump/transcripts
- https://en.wikipedia.org/wiki/Factba.se
- https://www.rev.com/category/politics
- https://www.debates.org/voter-education/debate-transcripts/
- https://github.com/jamesmartherus/debates
- https://www.theyworkforyou.com/api/
- https://github.com/mysociety/parlparse
- https://openparliament.tv/faq?a=faq&lang=en
- https://github.com/OpenParliamentTV/OpenParliamentTV-Tools
- https://aclanthology.org/2024.parlaclarin-1.12.pdf
- https://archive.org/details/tv
- https://blog.gdeltproject.org/gdelt-2-0-television-api-debuts/
- https://arxiv.org/html/2501.04484

Fallacy / propaganda detection
- https://tanbih.qcri.org/
- https://tanbih.qcri.org/demos/
- https://aclanthology.org/2023.semeval-1.317/
- https://github.com/kinit-sk/semeval2023-task3-persuasion-techniques
- https://github.com/ChadiHelwe/MAFALDA
- https://aclanthology.org/2024.naacl-long.270/
- https://github.com/pierpaologoffredo/ElecDeb60to20
- https://nlp-unibo.github.io/mm-argfallacy/2025/
- https://aclanthology.org/2025.argmining-1.35.pdf
- https://aclanthology.org/2025.acl-demo.45/
- https://3ia-demos.inria.fr/disputool/
- https://github.com/UKPLab/argotario
- https://dl.acm.org/doi/10.1145/3771882.3774253
- https://chromewebstore.google.com/detail/fallacy-detector/hldpaimaggankhhbgkndneaacgkojfkd
- https://www.logicalfallacies.org/fallacy-detector/
- https://arxiv.org/pdf/2410.15050

Building blocks
- https://github.com/m-bain/whisperX
- https://github.com/hyperaudio/hyperaudio-lite
- https://github.com/bbc/digital-paper-edit-client
- https://github.com/oTranscribe/oTranscribe
- https://github.com/bugbakery/audapolis
- https://amara.org/about
- https://news.slashdot.org/story/20/01/18/1753246/another-project-goes-private-amara-stops-being-developed-as-open-source
- https://archive.mpi.nl/tla/elan
- https://en.wikipedia.org/wiki/ELAN_software
- https://github.com/HumanSignal/label-studio
- https://github.com/doccano/doccano
- https://github.com/hypothesis/h
- https://github.com/FullFact/claim-review-schema-wordpress-plugin
