# Vie-publique.fr and the Collection des discours publics: history, legal posture, data, what the site can reuse

**Status:** research notes, 2026-09-05. **Not legal advice.** Compiled by an AI research agent from primary sources only: vie-publique.fr and dila.gouv.fr pages, the DILA open-data specification and presentation PDFs, the data.gouv.fr dataset record, the full DILA metadata dump (`vp_discours.json`, 230 MB, file dated 2026-09-05, 153,541 records, parsed by streaming), DILA activity reports, the Cour des comptes report on the SIG, the SIG's own pages on info.gouv.fr, a Sénat report, an Assemblée nationale written question, and the 2002 site of the Documentation française. Every claim carries its source. Items that no primary source settles are tagged **UNVERIFIED**.

**Method caveat.** vie-publique.fr serves a JavaScript bot-mitigation challenge (`bot_mitigation_cookie`, "This website requires JS enabled and cookies") to every non-browser client, including the Internet Archive's own crawler since mid-2023 for some pages. Every vie-publique.fr page quoted here was read from a dated Wayback Machine capture that predates or slipped past the challenge; the capture timestamp is given each time (`web.archive.org/web/<timestamp>/<url>`). Légifrance sits behind a Cloudflare challenge and info.gouv.fr returns 403 to non-browsers; the decrees are therefore cited as already verified in `legal-france.md` section 9, and the SIG pages from Wayback captures. Where this file repeats a fact already in `legal-france.md` §9 or `prior-art.md`, it does so only to anchor a new one.

Already known and not repeated here (see `docs/research/legal-france.md` §9): what DILA publishes as verified on 2026-09-05, the reconstruction of its legal basis from décrets 2000-1027 and 2010-31, the fact that the open data is metadata only, and the 2002 Jean-Marie Le Pen and 2004 Marine Le Pen pages.

---

## Executive summary

1. **The collection predates both DILA and the SIG's current mandate.** It is the Documentation française's documentary database, described on its own 2002 site as gathering "toutes les déclarations officielles des personnalités politiques, transmises par les services de presse ou récupérées sur les sites publics par la Documentation française, sélectionnées et analysées par ses soins et sous sa responsabilité" (§1.1). It has always been a *documentation* activity (select, index, republish texts that already exist), not a transcription service.
2. **The "Source" line is a provenance stamp, not a method statement.** Across eras it names the SIG (2002, 2025-2026), a ministry website (2021), or a candidate's campaign website (2007 second-round debate: `desirsdavenir.org`; 2012: `francoishollande.fr`, `lafranceforte.fr`). For non-office-holders the DF/DILA republished what the campaigns themselves had put online; SIG verbatims cover members of the Government (§1.4, §2.3). Whether the SIG's verbatims are typed by humans or produced by ASR is stated nowhere (**UNVERIFIED**).
3. **Candidate coverage collapsed after 2007.** Items whose `type_emetteur` is "Partis": 1,116 in 2002, 767 in 2007, 321 in 2009, **0 in 2010**, 168 in 2012, 3 in 2017, 1 in 2022. In the January-to-second-round window, all 16 candidates of 2002 and all 12 of 2007 have entries (Chirac 125, Jospin 119, Bayrou 86 in 2002; Royal 124, Sarkozy 112, Bayrou 103 in 2007), including radio and TV interviews; in 2012 the ten candidates are present but thinly (Sarkozy 128 mostly as President, Joly 40, Hollande 33, Le Pen 4, Mélenchon 1); in **2017 and 2022 no candidate other than the sitting President appears except in the second-round debate** (§2.2).
4. **The five second-round debates since 1995 are in the collection as full transcripts** (1995, 2007, 2012, 2017, 2022), plus the 2007 Royal–Bayrou debate on BFM TV; the 2007 text was sourced from Ségolène Royal's website (§2.3).
5. **DILA's published legal posture is explicit and narrow.** Its "Utiliser nos contenus" page (dated 1 March 2023) states: « Discours - texte du discours. Droits non gérés par la DILA. » and « La DILA n'étant pas propriétaire des contenus listés ci-dessous, elle ne peut en autoriser la reproduction, hormis celle de courtes citations » ; requests must go « à l'organisme dont dépend l'auteur du contenu ou directement à son auteur ». The footer's « Sauf mention contraire, tous les textes de ce site sont sous licence etalab-2.0 » is therefore overridden for the discours texts. Metadata are Licence Ouverte 2.0 with a three-line attribution (§3).
6. **No CADA opinion, court decision, Cour des comptes finding or parliamentary answer addresses the reuse of the discours texts.** The Cour des comptes (2012) mentions the SIG's « prestations de veille audiovisuelle (alertes médias, retranscriptions, enregistrements et montages) » as outsourced services being pooled. The Government's answer to written question 11845 (JO 3 March 2026) cites décret 2010-31 as DILA's basis for free access to its contents (§3.6).
7. **The page format is stable and copyable:** title = `<Type> de <M./Mme Prénom Nom>, <fonction>, à <média> le <date>, sur <sujets>`; block "Intervenant(s)" with the journalist listed and labelled « Journaliste »; « Média : »; « Texte intégral »; speaker labels in capitals on their own line; journalist's questions and third-party voices included; no timestamps; closing « Source : … » line; « MOTS CLÉS »; internal 9-digit id (§4).
8. **Data:** 18-field JSON schema, closed lists for `domaine` (4), `type_emetteur` (12), `type_document` (16), `type_media` (5); 597 distinct `thematiques` (474 in use since 2023), 4,961 distinct `descripteurs` (including person names); daily full-file refresh, no API, RSS feed; `mise_a_jour` is a re-indexing date, not a correction log (99% of records carry a 2025-09 bulk date); `id` is DILA's internal identifier, the URL node id is different (§5).
9. **Reusable now:** the metadata as a seed catalogue of Appearances (LO 2.0), the `thematiques` vocabulary as a candidate Theme list for v2 (LO 2.0), deep links to each page, the page conventions; **not reusable without the speaker's consent:** the full text of any discours (§6). What only DILA or the SIG can answer is listed as letter questions in §7.

---

## 1. History and production

### 1.1 The Documentation française collection (1974 →)

The earliest primary description found is the Documentation française's own site `discours-publics.ladocumentationfrancaise.fr`, captured by the Internet Archive on 2 October 2002 (presentation page `logos/presentation/presentation.htm`). Verbatim:

> « La collection des discours publics est une base de données documentaire sur la vie publique française depuis 30 ans qui rassemble toutes les déclarations officielles des personnalités politiques, transmises par les services de presse ou récupérées sur les sites publics par la Documentation française, sélectionnées et analysées par ses soins et sous sa responsabilité.
> C'est donc une collection de plus de 150 000 documents rendue accessible aux citoyens :
> 6 000 déclarations présidentielles (en texte intégral depuis 1974);
> 13 000 communiqués officiels dont tous ceux des conseils des ministres (en texte intégral depuis 1974);
> 60 000 déclarations politiques (depuis 1979) dont 34 000 déclarations gouvernementales (…), 20 000 déclarations de responsables politiques, 6 000 déclarations syndicales et patronales.
> Ces déclarations sont en texte intégral depuis 1999 ; pour les déclarations antérieures, des résumés sont proposés en ligne, le texte intégral étant disponible sur demande;
> 73 000 dépêches de chronologie, rédigées depuis 1974 par la Documentation française (…). »

and, on the selection of party sources:

> « Concernant les partis politiques, un ensemble de critères déterminent leur présence dans cette collection : représentation au Parlement, importance du parti comme acteur du débat politique, notamment par le biais des médias, positionnement dans un contexte électoral. Des règles constantes concernant le choix des auteurs sont respectées pour chacune des composantes politiques ou syndicales. »

and on indexing: « Chaque document fait l'objet d'une analyse documentaire thématique, à partir d'un vocabulaire contrôlé ». This is the origin of today's `thematiques` / `descripteurs`.

Two things follow. First, the *full text* of political declarations is systematic only from 1999; the metadata dump confirms the shape (449 records dated 1974, a jump to 1,616 in 1979 when "déclarations politiques" start, 3,000–4,800 per year from 1987 to 2009; §2.1). Second, the collection was conceived as a *documentation* of texts that already exist (press services, public websites), which is exactly what the "Source" lines still show (§1.4).

Consistent later descriptions: the Sénat's 2003 report on the Documentation française notes on vie-publique.fr « des milliers de références à des discours publics du Président de la République, du Premier ministre et des membres du gouvernement » (rapport n° 394, 2002-2003, ch. IV); DILA's 2019 activity report states that at the relaunch of vie-publique.fr on 23 October 2019 « Ont été mis en ligne dès l'ouverture du site : (…) la collection des discours publics (140 000 textes) » (p. 28); the DILA 20-years press kit (September 2022) counts « 145 000 discours publics » (p. 12); the current collection page says « près de 150 000 » and the listing page « plus de 160 000 » (Wayback 2026-01-24 and 2026-01-18). The "Qui sommes-nous ?" page (dated 2 September 2025; Wayback 2026-03-08) calls it one of « deux bases patrimoniales : la Collection des discours publics initiée en 1974 et la Bibliothèque des rapports publics lancée en 1995 ».

### 1.2 The SIG and media monitoring

The SIG's own history page (info.gouv.fr, Wayback 2024-04-03) gives the lineage and the wording of the 2000 decree, verbatim:

> « 12 juin 1974 — Création de la Délégation générale à l'information (DGI) rattachée au ministère de l'Information. (…) 06 décembre 1976 — Création du Service d'information et de diffusion (SID), rattaché au Premier ministre. Les missions du SID couvrent désormais des actions d'information de nature interministérielle, l'assistance technique aux administrations publiques et la coordination de leurs interventions, la diffusion des informations aux élus et à la presse sur l'action des administrations relevant de l'État. (…) 15 janvier 1996 — Le SID devient le SIG (…). 18 octobre 2000 — Le décret du 18 octobre fait évoluer les missions du SIG qui désormais comprennent l'analyse de l'opinion publique et le contenu des médias, la diffusion d'informations sur l'action gouvernementale auprès de divers publics (grand public, médias, élus) (…). »

The SIG's landing page (Wayback 2026-01-15) lists as first mission « analyser l'évolution de l'opinion publique et le traitement médiatique de l'action gouvernementale » and gives « 1963 Date de création », « Environ 87 collaborateurs », « 14,1 millions d'euros Budget 2023 ».

The only official document found that names transcription as an SIG activity is the Cour des comptes' *Organisation et fonctionnement du service d'information du Gouvernement* (communication au Premier ministre, art. L. 132-5-1 CJF, September 2012; hosted as rapport 124000512 on vie-publique.fr), p. 31: « le SIG a initié une démarche de mutualisation des prestations de veille audiovisuelle (alertes médias, retranscriptions, enregistrements et montages, notamment). Celle-ci est sur le point d'aboutir ». So in 2012 the transcripts were *purchased services* under media-monitoring contracts, pooled across ministries. The SIG's "marchés publics" page (Wayback 2024-04-03) confirms the model without naming lots: « Le Service d'information du Gouvernement compte ainsi 65 marchés actifs, dont 39 sont mutualisés avec les autres ministères ». Which supplier transcribes today, and whether ASR is used, is not published (**UNVERIFIED**; a BOAMP search is the next step, see §7).

The SIG's *répertoire d'informations publiques* (Wayback 2024-08-15) lists actualités, rapports, datasets on data.gouv.fr and marchés; it does **not** list verbatims or transcripts as a public-information holding. The SIG's data.gouv.fr organisation page holds 11 datasets (audiences, Grand Débat, Covid FAQ, baromètre), none about speeches.

### 1.3 DILA (2010 →) and the site

Décret n° 2010-31 du 11 janvier 2010 created DILA by merging the Journaux officiels and the Documentation française; its art. 2 mission « favoriser l'accès des citoyens à la vie publique et au débat public » is quoted in `legal-france.md` §9.2 (Légifrance could not be re-fetched today: Cloudflare challenge, **UNVERIFIED re-check**). The Government itself relies on that article: in its answer to written question n° 11845 (AN, 17e législature, JO 3 March 2026, p. 1872) it writes that DILA's mission is « de favoriser l'accès des citoyens à la vie publique et au débat public par l'édition et la diffusion de publications, la mise à disposition de documents et d'espaces de diffusion sur l'internet » (décret n° 2010-31 du 11 janvier 2010) and that « La très grande majorité des contenus édités ou produits par La Documentation française est librement accessible en ligne, notamment les rapports publics (…) diffusées sur le portail vie-publique.fr ».

vie-publique.fr itself: created in 2002 (DILA press kit and `contenus_vie-publique.fr.pdf`: « création en 2002, refonte en 2008 », « repensé en 2019 »); Wikipedia cites an « Arrêté du 5 juillet 2002 relatif à la création au secrétariat général du Gouvernement (direction de la Documentation française) d'un site internet intitulé "vie-publique.fr" » (**UNVERIFIED** on Légifrance). The relaunch of 23 October 2019 closed ladocumentationfrancaise.fr (DILA RIP page « Les données du débat public », updated 30 October 2019: « Le lancement du nouveau site "Vie-publique.fr" et la fermeture concomitante du site "ladocumentationfrançaise.fr", le 23 octobre 2019 »). Since then the collection lives at `vie-publique.fr/discours` and every record carries `mise_en_ligne: 2019-07-05` if it predates the migration (§5.4).

The editorial team: « Les rédacteurs, agents de la DILA, sont les garants de l'application de cette ligne éditoriale », with commitments of « Fiabilité », « Clarté », « Richesse », « Équilibre : les contenus excluent tout jugement de valeur ou interprétation personnelle » (Qui sommes-nous ?, 2 September 2025). Audience: 20,859,459 visits in 2025 (same page); « 21 millions de visites et 32,8 millions de pages vues » (DILA rapport d'activité 2025, p. 38).

### 1.4 How the collection is produced today

No page describes the workflow. What the pages themselves show:

| Era | Example (capture) | Closing "Source" line | Speaker labels |
|---|---|---|---|
| 1995 | Chirac–Jospin debate, 148596 (2022-05-01) | none visible | « M. DURAND. - », « M. CHIRAC.- » inline |
| 2002 | J.-M. Le Pen interviews, 129966 (see legal-france §9.1) | « (Source : Premier ministre, Service d'information du gouvernement, le 30 avril 2002) » | inline |
| 2007 | Royal–Sarkozy debate, 166574 (2020-07-30) | « Source http : //www.desirsdavenir.org, le 3 mai 2007 » | « Arlette Chabot : » inline |
| 2012 | Hollande, L'Express, 184912 (2026-02-08); Sarkozy, 184916 and 184947 (2022) | « Source : http://francoishollande.fr, le 16 avril 2012 »; « Source http://www.lafranceforte.fr, le 18 avril 2012 » | Q/A paragraphs, no labels |
| 2012 | Sarkozy–Hollande debate, 184977 (2022-05-18) | none visible; text opens « Script du débat entre François Hollande et Nicolas Sarkozy » | « David PUJADAS », « François HOLLANDE » on own line |
| 2021 | Beaune, Public Sénat, 280375 (2026-02-09) | « Source https://www.diplomatie.gouv.fr, le 11 juin 2021 » | « Q - » / « R - » |
| 2025 | Vautrin, BFM TV, 300132 (2026-02-14) | « Source : Service d'information du Gouvernement, le 11 septembre 2025 » | « APOLLINE DE MALHERBE », « CATHERINE VAUTRIN », « YANN, ARTISAN BOUCHER DANS LE GARD » on own line |
| 2026 | Farandou, BFM TV, 302053 (legal-france §9.1) | « Source : Service d'information du Gouvernement, le 12 février 2026 » | same |

Reading: the SIG is the source for members of the Government (2002 Prime minister's SIG; 2025-2026), the Quai d'Orsay publishes its own ministers' interviews which DILA copies, and **for candidates who are not in office the text came from the candidate's own website** (2007 debate from Royal's site; 2012 Hollande and Sarkozy from their campaign sites). The DF's 2002 statement « transmises par les services de presse ou récupérées sur les sites publics » therefore still describes the intake. The date on the Source line is the date DILA received or fetched the text: Vautrin was broadcast on 27 August 2025, sourced from the SIG on 11 September, `mise_en_ligne` 2025-09-11, `mise_a_jour` 2025-09-24. Across the 980 radio and TV interviews dated 2025-01-01 or later, the lag from `prononciation` to `mise_en_ligne` has a median of 1.5 days (p25 = 1, p75 = 4, p90 = 8, max 36). Human versus ASR: **UNVERIFIED**; the 2025 texts are clean verbatim with speaker names in capitals and no fillers, which is consistent with either a corrected ASR or a typing service.

---

## 2. Scope over time and candidate coverage

All counts below come from `vp_discours.json` (file dated 2026-09-05 06:01, 153,541 records, `prononciation` from 1959-01-15 (five stray records before 1974) to 2026-08-31). Method: streaming parse; "candidate items" are records whose `intervenants[].nom` matches the candidate's surname, dated from 1 January of the election year to the second round inclusive. `intervenants[].qualite` is unreliable for this purpose (it is null on most pre-2019 records: e.g. Hollande's 2012 interview has `qualite: null`, `type_media: null`, `media: null` in the dump while the page shows « Média : Emission Forum RMC L'Express - L'Express »), so the counts rely on names and titles.

### 2.1 Volume and composition by year (selected)

| Year | Records | of which `Interview` | `type_emetteur` = Partis | Syndicats Patronat |
|---|---|---|---|---|
| 1974 | 449 | 1 | – | – |
| 1979 | 1,616 | 242 | – | – |
| 1988 | 4,787 | 1,214 | – | – |
| 1995 | 3,348 | 586 | 853 | 229 |
| 2002 | 4,175 | 984 | 1,116 | 251 |
| 2007 | 3,917 | 961 | 767 | 204 |
| 2009 | 3,744 | 851 | 321 | 93 |
| 2010 | 2,674 | 414 | **0** | 0 |
| 2012 | 2,449 | 311 | 168 | 0 |
| 2017 | 2,527 | 472 | 3 | 0 |
| 2019 | 2,763 | 1,024 | 0 | 0 |
| 2022 | 2,215 | 681 | 1 | 0 |
| 2025 | 2,097 | 651 | 0 | 0 |
| 2026 (to 31 Aug) | 1,362 | 397 | 0 | 0 |

Whole collection: `type_document` = Déclaration 57,804; Interview 29,757; Article 29,147; Communiqué 26,376; Conférence de presse 7,314; Lettre 2,646; Littérature grise 156; Tribune 141; Dossier 83; Rapport 13; Chronologie 5; Ouvrage 5; Périodique 5; Sélection 3; Statistiques 1; null 85. `type_emetteur` = Gouvernement 74,434; Partis 21,777; Président de la République 10,472; Premier ministre 7,504; Syndicats Patronat 6,802; Ministère des affaires étrangères 4,981; Présidence de la République 3,552; Parlement 1,989; Conseil des ministres 1,974; Services du Premier ministre 1,544; null 11,298 plus the literal string "NULL" 7,214. Radio and television interviews in the campaign years, all speakers: 2002 = 750 (470 radio, 280 TV); 2007 = 759; 2012 = 251; 2017 = 424; 2022 = 513. The party and union strands stop in 2010, which matches DILA's creation (January 2010) and the end of the DF's "responsables politiques, syndicaux et patronaux" intake; nothing published explains the decision (**UNVERIFIED**, question for DILA in §7).

### 2.2 Candidate coverage per presidential campaign (1 January to second round)

**2002 (to 5 May; 16 candidates, all present).** Chirac 125 items (of which 13 radio/TV interviews: France 2, Europe 1, RTL, Forum RMC), Jospin 119 (11 broadcast interviews), Bayrou 86 (28 broadcast, incl. 14 TV, Europe 1, RTL, France Culture, BFM), Mamère 72, Hue 64, Madelin 57, Chevènement 55, Le Pen 43 (5 broadcast interviews + 3 broadcast declarations), Laguiller 41, Lepage 32, Mégret 27, Boutin 25, Saint-Josse 22, Taubira 19, Besancenot 15, Gluckstein 12. Recurrent media: RTL (« Emission L'Invité de RTL »), Europe 1, France 2, France Info, BFM, Forum RMC (Libération / Le Figaro), La Croix, regional press. Each candidate also has a « Déclaration … Fédération nationale des accidentés du travail et des handicapés » and a « source privée » entry, i.e. the DF collected candidates' answers to interest groups.

**2007 (to 6 May; 12 candidates, all present).** Royal 124, Sarkozy 112 (13 broadcast interviews: RTL, France 2, Europe 1, BFM, Canal+, France Info), Bayrou 103, Buffet 41, Le Pen 34, Laguiller 31, Voynet 24, de Villiers 23, Bové 15, Schivardi 13, Besancenot 7, Nihous 3. 725 records carry the theme « Élection présidentielle » that year; the journalists most present are Aphatie (27), Demorand (24), Sicard (19), Bourdin (17), Elkabbach (17).

**2012 (to 6 May; 10 candidates, all present but thin).** Sarkozy 128 (103 as President; 20 with `qualite` « Candidat à l'élection présidentielle », mostly declarations, letters and print interviews), Joly 40 (25 tagged EELV candidate; declarations, one radio interview), Hollande 33 (26 declarations, 2 France 2 interviews, print), Poutou 12, Bayrou 8, Le Pen 4 (three declarations, one « Littérature grise »), Arthaud 4, Dupont-Aignan 3 (one France 2 interview), Cheminade 3, Mélenchon 1 (his programme « L'Humain d'abord »). Candidates' programmes and professions de foi were catalogued as « Programme électoral » / « Profession de foi » declarations.

**2017 (to 7 May).** Macron 3 (the 3 May debate, the 7 May victory declaration and allocution), Le Pen 1 (the debate). Fillon, Mélenchon, Hamon, Dupont-Aignan, Lassalle, Poutou, Asselineau, Arthaud, Cheminade: **0**. The 52 records themed « Élection présidentielle » are ministers commenting on the campaign.

**2022 (to 24 April).** Macron 42 (38 as President, 4 as « Président de la République, candidat à l'élection présidentielle 2022 », including the 10 April first-round declaration), Le Pen 1 (the 20 April debate, `qualite` « Candidate du Rassemblement national à l'élection présidentielle 2022 »). Mélenchon, Zemmour, Pécresse, Jadot, Lassalle, Roussel, Dupont-Aignan, Hidalgo, Poutou, Arthaud: **0**.

Conclusion: from 2017 the collection is an archive of the executive's speech; the last campaign in which it documented all candidates with broadcast interviews is 2007. The 2002 and 2004 opposition pages cited in `legal-france.md` §9 are the tail of the DF period, not a DILA policy.

### 2.3 Debates

Titles beginning with « Débat » number 321 across the collection, mostly 1980s TV debates between a party figure and MPs (`type_document` Interview). The presidential second-round debates present as full text:

| Date | Record | Media field | Source line on page |
|---|---|---|---|
| 1995-05-02 Chirac–Jospin | 148596 (Interview) | null; « Circonstance : Débat radiotélévisé… » | none visible |
| 2007-04-28 Royal–Bayrou | 166543 (Interview) | BFM TV | not captured |
| 2007-05-02 Royal–Sarkozy | 166574 (Interview) | France 2 | « Source http : //www.desirsdavenir.org, le 3 mai 2007 » |
| 2012-05-02 Sarkozy–Hollande | 184977 (Déclaration) | France 2 | none visible; « Circonstance : Campagne officielle : débat télévisé de l'entre-deux tours » |
| 2017-05-03 Macron–Le Pen | 203174 (Déclaration) | France 2 | not captured |
| 2022-04-20 Macron–Le Pen | 285127 (Interview) | France 2 | not captured |

No first-round multi-candidate debate (2017 TF1 and BFMTV/CNews, 2022) was found in the dump.

### 2.4 Media mix today

Records dated 2025-01-01 to 2026-08-31: 3,459 (about 160–240 a month outside August–September), of which 980 radio/TV interviews (548 radio, 432 TV). Media of those interviews: France Info 147, France 2 105, BFM TV 95, RTL 92, TF1 91, France Inter 81, Sud Radio 70, CNews 62, LCP 28, LCI 26, RMC Info 24, France Info TV 22, RMC 19, Europe 1 17, BFM Business 16, Radio J 16, RFI 10, Public Sénat 8, France 5 7 (47 with `media` null). The `media` field has 1,799 distinct strings over the whole collection and is not normalised (« BFM », « BFM TV », « BFM Business »; « RMC », « RMC Info »; « Emission L'Invité de RTL » vs « RTL »).

---

## 3. Legal posture as published

### 3.1 Mentions légales (page dated 3 July 2020; Wayback 2023-02-06)

> « Le contenu de ce site internet est fourni par : Direction de l'information légale et administrative - 26, rue Desaix - 75727 Paris Cedex 15 (…) N° SIREN : 130-009-186 (…) Code APE : 5813Z/Édition de journaux. Directeur de la publication « Au sens de l'article 93-2 de la loi n° 82-652 du 29 juillet 1982. » Madame Anne Duclos-Grisier, directrice de la DILA. Prestataire d'hébergement Atos Worldline (…). Liens hypertextes : Vie-publique.fr propose de nombreux liens vers d'autres sites (…) elles n'engagent pas la responsabilité de la DILA. »

The current version names Véronique Lehideux and Outscale (legal-france §9.2). Neither version contains an intellectual-property clause. dila.gouv.fr's own mentions légales (updated 23 July 2024) add nothing on the discours.

### 3.2 Footer licence

Every captured vie-publique.fr page (2022, 2023, 2026) ends with « Sauf mention contraire, tous les textes de ce site sont sous licence etalab-2.0 », linking to `github.com/etalab/licence-ouverte/blob/master/LO.md`. This resolves the UNVERIFIED point in `legal-france.md` §9.3: the footer exists. But it is subject to « sauf mention contraire », and the "Utiliser nos contenus" page is that contrary mention.

### 3.3 « Utiliser nos contenus » (page dated 1 March 2023; Wayback 2026-01-17)

This is the operative statement. Verbatim, the parts that matter:

> « **Contenus réutilisables sous Licence Ouverte 2.0.** Les contenus listés ci-dessous peuvent être réutilisés sous réserve de mentionner : la source : Vie-publique.fr ; la date de création ou mise à jour du contenu qui figure sur Vie-publique.fr ; de ne pas modifier le contenu ; (…) Contenus textuels : Éclairages, Brèves, Lois, Fiches, Questions-réponses, Consultations. »

> « **Métadonnées réutilisables sous Licence Ouverte 2.0.** On appelle métadonnées les éléments qui permettent de décrire un contenu : titre, auteur(s), thèmes associés… Dans le cas d'une utilisation à l'unité (…), les métadonnées peuvent être librement réutilisées. Dans le cas de l'utilisation d'un grand nombre (plus de 50) ou de l'ensemble des références d'un contenu, les métadonnées des contenus listés ci-dessous peuvent être réutilisées sous réserve de mentionner : la source : Vie-publique.fr ; la date de création ou mise à jour du contenu qui figure sur Vie-publique.fr. Métadonnées réutilisables sous Licence Ouverte : Discours, Livres et revues, Rapports publics. »

> « **Contenus dont les droits ne sont pas gérés par la DILA.** La DILA n'étant pas propriétaire des contenus listés ci-dessous, elle ne peut en autoriser la reproduction, hormis celle de courtes citations* : Discours, y compris la rubrique "Discours dans l'actualité" ; Rapports. Les demandes de reproduction ou de rediffusion de rapports ou discours doivent être adressées à l'organisme dont dépend l'auteur du contenu ou directement à son auteur. »

> « * La citation doit respecter l'esprit du texte dont elle est extraite, elle doit mentionner la source (le nom de l'auteur s'il est indiqué, la source : Vie-publique.fr, la date de création ou de mise à jour indiquée sur Vie-publique.fr), elle doit être justifiée par le caractère critique, polémique, pédagogique, scientifique ou d'information de l'œuvre à laquelle elle est intégrée. La citation doit être courte. »

> « **En résumé** (…) Discours dans l'actu. Reproduction non autorisée. Discours - métadonnées : Contenus réutilisables sous Licence Ouverte. Discours - texte du discours. Droits non gérés par la DILA. »

Contact for requests: « DILA - Département de l'édition et du débat public - 26, rue Desaix - 75727 Paris CEDEX 15 » or the contact form. Logos and the marks « Vie publique » and « La Documentation française » are INPI-registered; partner use requires citing DILA.

Reading for this project: DILA states that it does **not** hold the rights in the discours texts and will not license them; it points reusers to the author (the speaker) or the author's organisation. Nothing is said about broadcasters or journalists. The "courte citation" carve-out is DILA's restatement of CPI L.122-5 3° a, not a grant.

### 3.4 Open-data conditions (data.gouv.fr dataset 692efee34bc7205826d04002, created 2 December 2025; DILA presentation sheet of 10 November 2025)

> « Les métadonnées sont réutilisables gratuitement sous licence ouverte v2.0. Les réutilisateurs s'obligent à mentionner : la paternité des données (DILA) ; l'url d'accès longue de téléchargement ; le nom du fichier téléchargé ainsi que la date du fichier. Le réutilisateur s'oblige à prendre en compte les demandes de mise à jour de données publiées ponctuellement par la DILA dans le forum de discussion du jeu de données sur data.gouv.fr. » Contact: donnees-dila@dila.gouv.fr (Administration des données).

The dataset record says `license: lov2`, organisation « Premier ministre », `frequency: punctual` (inconsistent with the sheet's « Les données sont mises à jour tous les jours »), `temporal_coverage` 2025-12-02 → 2035-02-01 (a placeholder). The discussion forum could not be read (connection resets, **UNVERIFIED** whether any thread exists). A separate data.gouv.fr "réutilisation" record « Collection des discours publics » (created 21 September 2015, type news_article, pointing at `vie-publique.fr/discours/`) shows that an earlier dataset existed before the December 2025 one; it now returns 404.

### 3.5 What DILA's repertoire says

DILA's *répertoire des informations publiques* page « Les données du débat public » (updated 30 October 2019) lists only three datasets: « Norme Debatescore », « Débats et consultations publics », « Thésaurus information publique » (all XML). The discours metadata were not a listed public-information holding until December 2025.

### 3.6 Official documents on the collection and its reuse

- **DILA activity reports** 2019 (p. 28, quoted §1.1), 2024 and 2025: the 2024 and 2025 reports describe vie-publique.fr (audience, municipales 2026, Cairn partnership, RGAA 100%) and do not mention the discours collection at all; 2012 and 2013 reports: no mention found (text extraction of 2013 is garbled).
- **Cour des comptes**, SIG report September 2012, p. 31 (quoted §1.2). No Cour des comptes text on DILA's collection was found.
- **CADA**: no avis mentioning vie-publique.fr or the discours collection was found through the cada.fr search results reachable today (the CADA search itself could not be queried programmatically, **UNVERIFIED**).
- **Court decisions**: none found on the collection (searches limited to what the proxy allowed; **UNVERIFIED**).
- **Parliament**: no written question on the collection was found. Closest: AN QE 11845 (Timothée Houssin, published 23 December 2025; answer 3 March 2026) on free access to Documentation française publications; the answer cites décret 2010-31, states most contents are free online, and justifies paid publications by « contributeurs extérieurs dont les droits d'auteurs doivent être respectés (…) contrats d'édition conformes au code de la propriété intellectuelle ». Sénat rapport n° 394 (2002-2003) on the Documentation française mentions the discours references on vie-publique.fr as a quality of the site.
- **Broadcasters, journalists, speakers**: no arrangement, consent or licence is mentioned on any page or report found (**UNVERIFIED**; see §7).

---

## 4. Editorial conventions of a verbatim broadcast-interview page

Observed on record 300132 (Vautrin, BFM TV, 27 August 2025; Wayback 2026-02-14), cross-checked with 280375 (2021), 184912 (2012), 184977 (2012 debate), 148596 (1995).

**Title.** `Interview de Mme Catherine Vautrin, ministre du travail, de la santé, des solidarités et des familles, à BFM TV le 27 août 2025, sur les 30 000 dirigeants de PME (…), le vote de confiance demandé par François Bayrou, la gestation pour autrui et la hausse de la mortalité infantile.` Pattern: `<Interview|Entretien|Déclaration|Débat télévisé> de <M.|Mme> <Prénom Nom>, <fonction>, à <média> le <date>, sur <liste de sujets>.` The `<title>` element is different: `Prononcé le 27 août 2025 - Catherine Vautrin 27082025 BFM crise des PME vote de confiance GPA | vie-publique.fr`, i.e. the URL slug. `og:title` and JSON-LD `headline` are the full title truncated at 255 characters; JSON-LD `name` is complete.

**Head of page.** Thematic tags (« Économie », « Institutions », links to /economie, /institutions); « Prononcé le 27 août 2025 » (`<time datetime="2025-08-27T12:00:00Z">`); « Intervenant(s) : Catherine Vautrin - Ministre du travail, de la santé, des solidarités et des familles ; Apolline de Malherbe - Journaliste », each linked to an author page `/auteur/17772-catherine-vautrin`, `/auteur/12261-apolline-de-malherbe`; « Média : BFM TV ». The 2012 debate page adds « Circonstance : Campagne officielle : débat télévisé de l'entre-deux tours ».

**Body.** Heading « Texte intégral », then one `<p>` per turn: speaker label in capitals, `<br>`, the turn. The journalist's questions are included in full; a listener's recorded message is transcribed and labelled « YANN, ARTISAN BOUCHER DANS LE GARD ». Names inside the text are also capitalised (« Bonjour Catherine VAUTRIN »). Numbers use non-breaking spaces. **No timestamps, no links to the replay, no video embed** (the site's own "Discours dans l'actualité" page for the 14 July interviews notes « format vidéo uniquement, pas de retranscription » for 2014 and 2022, showing that video-only entries exist without text). Older conventions: 2021 MFA interviews use « Q - » / « R - »; 2007 uses « Arlette Chabot : » inline; 1995 uses « M. DURAND. - ».

**Footer of the text.** « Source : Service d'information du Gouvernement, le 11 septembre 2025 » as the last line of the text field; then « MOTS CLÉS » (descripteurs, e.g. Finances publiques, Budget de l'État, Article 49, Budget 2026, Mortalité infantile, Travailleur étranger); then the internal id « 253001560 » (equals `id` in the dump).

**Corrections and updates.** No « Dernière modification » or correction notice appears on discours pages (the news pages carry « Dernière modification : 19 juillet 2022 »). The metadata `mise_a_jour` exists but is not a correction log (§5.4). How DILA handles a correction request is not published (**UNVERIFIED**).

**Sharing.** Buttons « Imprimer », « Télécharger au format pdf », « Envoyer par Email », « Copier dans le presse-papier », social networks (the PDF link is generated per page; not fetched).

**URL scheme and permalinks.** `https://www.vie-publique.fr/discours/<node>-<slug>`, canonical set in `<link rel="canonical">`; `<node>` is a 6-digit Drupal node id (129966 for 2002 items, 300132 for 2025, 304466 for August 2026), `<slug>` derived from the title (« catherine-vautrin-27082025-bfm-crise-des-pme-vote-de-confiance-gpa ») or, for pre-2019 items, from the old title (« interview-de-m-francois-hollande-depute-ps-et-candidat-lelection-p »). The `url` field in the dump appends `?egn-publisher=dila_vp&egn-name=informer_opendata_discours` (tracking parameters to strip). Whether `/discours/<node>` without slug redirects: **UNVERIFIED** (site blocks non-browsers). Author pages: `/auteur/<id>-<slug>`.

**Sitemaps and feeds.** `/sitemap.xml` is a Drupal `simple_sitemap` index pointing to `/discours/sitemap.xml`, itself an index of `/sitemaps/discours/sitemap.xml?page=1 … N` (`lastmod` 2026-01-12 in the 2026-01-17 capture); `robots.txt` declares both sitemaps and disallows only Drupal system paths. RSS: `https://www.vie-publique.fr/discours-feeds.xml` (« titre, résumé et URL » of the latest discours; page « Flux RSS », 15 June 2020). Both are behind the bot challenge for non-browser clients today.

---

## 5. Data: the open-data metadata

### 5.1 Files

`https://echanges.dila.gouv.fr/OPENDATA/DISCOURS_PUBLICS/` (plain Apache index, no bot challenge): `vp_discours.json` (230 MB, UTF-8, pretty-printed JSON array, regenerated daily around 04:00–06:00 UTC: file timestamp 2026-09-05 06:01, data.gouv `last_update` 2026-09-04T04:00:19Z), `Specifications-datagouv-referentiel-discours_V1_20251126.pdf` (spec V1.0 dated 10 November 2025, validated after a V0.9 of 10 July 2025), `DILA_Discours publics_Presentation_20251126.pdf`. « Cette ressource permet d'accéder à la dernière version totale (non incrémentale) en vigueur du fichier mis à jour » (spec §2). No API; no incremental feed; sort key is `prononciation` (spec §1.4), newest first.

### 5.2 Schema (spec §1.4, verified against the file)

| Field | Required | Multi | Type | Spec description | Observed |
|---|---|---|---|---|---|
| `id` | yes | | numeric string | ID du discours | 9 digits, DILA internal (shown at page bottom); not the URL node id |
| `titre` | yes | | text | | may end with `\r\n` |
| `url` | yes | | text | Adresse du discours complet sur Vie-publique.fr | with tracking query string |
| `domaine` | yes | | closed list (4) | domaine d'intervention | Déclaration 115,886; Conseil des ministres 16,752; Président de la République 11,810; Communiqué 8,878; null 215 |
| `prononciation` | yes | | date | Date de prononciation (clé de tri) | ISO date |
| `intervenants[].nom` | yes | yes | text | Auteur | null for communiqués; 37,214 records have 2+ named intervenants (journalists count) |
| `intervenants[].qualite` | | yes | text | Description courte de l'auteur | 3,464 distinct strings, null on most pre-2019 records |
| `intervenants[].qualite_long` | | yes | text | Description longue | present on 139,135 entries (long biographical function) |
| `auteur_moral` | | yes | text | | Secrétariat général du Gouvernement 8,105; Présidence de la République 2,862; Premier ministre 1,156; ministries |
| `circonstance` | | | text | Circonstances | 71,877 records |
| `type_emetteur` | yes | | closed list | | 12 values (§2.1) |
| `type_document` | yes | | closed list | | 16 values (§2.1) |
| `type_media` | | | closed list | | Radio 12,730; Télévision 6,602; Presse régionale 1,428; Presse étrangère 828; « Agence de presse » (trailing space) 124; null 131,829 |
| `media` | | | text | Nom du média | 1,799 distinct, not normalised |
| `resume` | | | text | Présentation courte | 14,536 records |
| `thematiques` | | yes | text | Thématique générale | 597 distinct |
| `descripteurs` | | yes | text | Descripteurs | 4,961 distinct |
| `mise_en_ligne` | yes | | date | | |
| `mise_a_jour` | yes | | date | | |

Sample record (spec §1.3, verbatim): `{"id": "257001777", "titre": "Déclaration de M. Emmanuel Macron, président de la République, sur l'importance des forêts primaires (…), à Belém le 6 novembre 2025.\r\n", "url": "https://www.vie-publique.fr/discours/300832-emmanuel-macron-06112025-lutte-contre-le-dereglement-climatique", "domaine": "Président de la République", "prononciation": "2025-11-06", "intervenants": [{"nom": "Emmanuel Macron", "qualite": "Président de la République", "qualite_long": null}], "auteur_moral": [], "circonstance": "Lancement du Tropical Forests Forever Fund", "type_emetteur": "Président de la République", "type_document": "Déclaration", "type_media": null, "media": null, "resume": null, "thematiques": ["Climat"], "descripteurs": ["Forêt", "Biodiversité", "Décarbonation", "Financement"], "mise_en_ligne": "2025-11-07", "mise_a_jour": "2025-11-07"}`.

### 5.3 Taxonomies

**`thematiques`** (597 distinct values, full list with counts in Appendix A). It is a flat controlled vocabulary mixing policy areas (« Politique économique » 3,064, « Santé publique » 1,623, « Logement » 1,433, « Retraite » 980, « Immigration » 966, « Climat » 895), countries and regions (« Ukraine » 496, « Israël », « Chine »), institutions (« Parlement », « Gouvernement »), populations (« Femme », « Jeune », « Handicapé »), and events (« Jeux Olympiques et Paralympiques »). 474 of the 597 values were used on at least one record dated 2023 or later; the most used since 2023: Politique étrangère 357, Politique économique 322, Ukraine 237, Budget de l'État 233, Israël 209, Construction européenne 195, Politique agricole 187, Fonction publique 175, Ordre public 134, Santé publique 131, Retraite 131, Outre-mer 130, Politique de la défense 111, Politique des transports 109, Proche-Orient 108, Politique gouvernementale 94, Climat 93, Femme 93, Logement 92, Guerre 87, Politique de l'environnement 87, Politique industrielle 83, Politique de l'énergie 82, Politique culturelle 76, Politique judiciaire 76, Sécurité sociale 75, Politique de l'enseignement 72, Antisémitisme 66, Enfant 62, Intelligence artificielle 39. « Élection présidentielle » (1,300 overall) is itself a thematique.

**`descripteurs`** (4,961 distinct; 2,327 used since 2023). Finer, includes person names in « Nom Prénom » form (« Mitterrand François » 5,032, « Chirac Jacques » 4,389, « Sarkozy Nicolas »), parties (« PS » 6,626, « UDF » 3,560), bilateral pairs (« Russie - Ukraine », « France - Israël », « UE - MERCOSUR »), instruments (« Projet de loi » 12,260, « Réforme » 11,825, « Loi de finances »), and year-bound items (« Budget 2026 », « Election presidentielle 2012 » on the 2012 debate page). The full list is not reproduced here; it is regenerated by the one-pass script described in §2 (count `descripteurs` values over the file). The page's « MOTS CLÉS » block displays the descripteurs, so page and dump agree.

No hierarchy, no identifiers, no definitions are published for either list; the DF's 2002 « vocabulaire contrôlé » is not published as a thesaurus (DILA's separate « Thésaurus information publique » dataset, listed in the RIP, covers the "information administrative" domain, not the discours; **UNVERIFIED** whether they overlap).

### 5.4 What `mise_a_jour` means

Of 153,541 records, only 1,324 have `mise_a_jour == mise_en_ligne`; 146,193 have a `mise_a_jour` more than two years after `mise_en_ligne`. Every pre-2019 record has `mise_en_ligne = 2019-07-05` (the migration to the new site) and the vast majority carry `mise_a_jour` in late September 2025 (a bulk re-index preceding the open-data release: e.g. Beaune 2021 → 2025-09-25, Hollande 2012 → 2025-09-25). The field therefore records the last save of the record, editorial or technical, and cannot be read as "text corrected on". A change-detection strategy for the seed catalogue must diff the whole file (title, intervenants, descripteurs) rather than trust the date.

### 5.5 Deep-linking to a discours

Use the `url` field with its query string removed. The stable part is the node id; the slug is derived from the title and may differ between the 2019 migration form and the current form. Keep `id` as the DILA identifier for matching future dumps (the URL is required but `id` is the primary key in DILA's own file). Timestamped links are impossible: the pages have no anchors below « Texte intégral » and no time codes.

---

## 6. What we can reuse

| Asset | Licence and condition | Exact reference | Use in this project |
|---|---|---|---|
| **Metadata of every discours** (title, date, intervenants with function, media, type, themes, descripteurs, URL, DILA id) | Licence Ouverte 2.0. Mandatory mention: « la paternité des données (DILA) ; l'url d'accès longue de téléchargement ; le nom du fichier téléchargé ainsi que la date du fichier », plus taking into account update requests posted on the data.gouv.fr forum. The site page adds, for more than 50 references: source « Vie-publique.fr » and the creation/update date shown on the site. | data.gouv.fr dataset 692efee34bc7205826d04002 « Métadonnées des Discours publics de Vie-publique.fr »; `echanges.dila.gouv.fr/OPENDATA/DISCOURS_PUBLICS/vp_discours.json`; DILA presentation sheet 10 Nov 2025; « Utiliser nos contenus » (1 Mar 2023) | Seed catalogue of Appearances for any Candidate who is or was in the executive (title, date, medium, journalist, themes); cross-reference of our own Appearances to DILA's record (`id`, node id); the `intervenants[].nom` list as a Speaker gazetteer (journalists included). For non-executive candidates it yields nothing after 2012. Attribution line to keep verbatim: « Source : DILA, Métadonnées des Discours publics de Vie-publique.fr, https://echanges.dila.gouv.fr/OPENDATA/DISCOURS_PUBLICS/vp_discours.json, fichier vp_discours.json du <date> ». |
| **`thematiques` vocabulary** (597 labels; 474 live) | Same LO 2.0 as the metadata (it is a field of the dump). Labels only; no definitions, no hierarchy. | Appendix A; dump field `thematiques` | Candidate list for the v2 Theme taxonomy: pick the 15–25 policy-area labels (Politique économique, Santé publique, Logement, Retraite, Immigration, Climat, Politique de l'énergie, Politique de l'enseignement, Justice, Ordre public, Politique de la défense, Politique étrangère, Construction européenne, Fonction publique, Budget de l'État, Politique agricole, Outre-mer, Femme, Jeune, Handicapé, Économie numérique…) and keep DILA's exact spelling so a Segment tagged with our Theme can be joined to DILA's records. Countries, persons and events stay out of Theme (they are Topics or entities). |
| **`descripteurs` vocabulary** (4,961 labels) | Same LO 2.0. | Dump field `descripteurs`; page « MOTS CLÉS » | Source of Topic labels under a Theme (« Retraite » → « Âge de la retraite »?) and of the person-name convention (« Nom Prénom »). Too large and uneven to adopt whole. |
| **Deep links** to each discours page and each author page | Linking needs no licence; DILA's own mentions légales treat links as normal. Strip `?egn-publisher…`. | `url` field; `/auteur/<id>-<slug>` | On each Appearance that DILA also holds, a « Transcription officielle sur vie-publique.fr » link; on each Speaker profile, the vie-publique author page. |
| **Formatting conventions** (title grammar, Intervenant(s) block with the journalist labelled « Journaliste », « Média : », « Texte intégral », speaker label on its own line in capitals, closing « Source : … » line, keyword block) | Conventions are not protected; copying DILA's editorial *text* (titles, résumés) is LO 2.0 with attribution. | §4 | Adopt as the house style for Transcript pages, adding what DILA lacks: timestamps per Segment, link to the replay, version history. |
| **Short quotations** of a discours text | CPI L.122-5 3° a as restated by DILA: « courte », « respecter l'esprit du texte », mention « le nom de l'auteur (…), la source : Vie-publique.fr, la date de création ou de mise à jour ». | « Utiliser nos contenus », footnote * | Quoting a DILA transcript to illustrate a Statement or a discrepancy with our own transcript, with that attribution. |
| **Full text of a discours** | **Not licensed.** « Droits non gérés par la DILA » ; « Les demandes de reproduction ou de rediffusion (…) doivent être adressées à l'organisme dont dépend l'auteur du contenu ou directement à son auteur. » | « Utiliser nos contenus », « En résumé » | Do not import DILA texts into the repository. For an Appearance where DILA has a transcript, link to it and, if we transcribe it ourselves, treat DILA's text as a comparison source only. Consent for full text comes from the speaker (candidate/campaign), which is what the consent-letter ticket is for; DILA's own practice for candidates (2007, 2012) was to take texts the campaigns had published. |
| **« Discours dans l'actualité » selections** | « Reproduction non autorisée. » | same page | Not reusable; may be linked. |
| **Logos and marks** | INPI-registered; partner use only with « DILA » cited; commercial use forbidden without written consent. | same page | Do not display the logo; a text link suffices. |
| **RSS feed** `discours-feeds.xml` and sitemaps | Not licensed separately; both are behind the bot challenge for scripts. | page « Flux RSS » | Not a viable ingestion channel; the daily JSON is. |

Practical import recipe: fetch `vp_discours.json` daily; filter `prononciation >= 2026-08-27` and `type_document in (Interview, Déclaration)` with `type_media in (Radio, Télévision)`; keep `id`, canonical `url`, `titre`, `prononciation`, `intervenants`, `media`, `thematiques`, `descripteurs`; record the file date in the attribution line; store nothing from the page body.

---

## 7. Open questions (what only DILA or the SIG can answer)

Phrased as a letter would ask them. Addressees: DILA, Département de l'édition et du débat public (rédaction de Vie-publique.fr), 26 rue Desaix, 75727 Paris Cedex 15; DILA Administration des données (donnees-dila@dila.gouv.fr); SIG, 20 avenue de Ségur, 75007 Paris.

To DILA (Vie-publique.fr):

1. Who produces the verbatim texts of ministers' radio and television interviews that the Collection des discours publics publishes with the line « Source : Service d'information du Gouvernement » — is the transcription made by SIG staff, by a contractor under an SIG media-monitoring contract, or by automatic speech recognition, and is it reviewed before publication?
2. Under which legal analysis does DILA publish the full text of broadcast interviews, including the journalists' questions, permanently and without a licence from the broadcaster or the journalist? Does any written arrangement exist with France Télévisions, Radio France, TF1, BFM/RMC, CNews, LCI, Europe 1, Sud Radio or their journalists' representatives?
3. Does DILA obtain consent from the speaker (or a party's or campaign's press service) before publishing an interview text, or does it rely on the text having been transmitted by the speaker's own press service or published on their site, as the 2002 Documentation française presentation described and as the « Source http://francoishollande.fr » lines of 2012 suggest?
4. Why did the intake of party leaders' and union leaders' statements (« type_emetteur » Partis, Syndicats Patronat) stop in 2010, and why were the 2017 and 2022 candidates not documented outside the second-round debate? Is there a written collection policy, and does DILA intend to document the 2027 candidates?
5. For the second-round debates of 1995, 2007, 2012, 2017 and 2022 and for the 2007 Royal–Bayrou debate, where did the transcript come from (broadcaster, campaign, SIG), and did the broadcaster consent to its permanent publication?
6. Would DILA license, under Licence Ouverte 2.0 or otherwise, the full text of the interviews and debates of the 2027 candidates to a non-commercial citizen site that links back to Vie-publique.fr, and if not, which « organisme dont dépend l'auteur » does it consider competent for a candidate who holds no office?
7. How are corrections to a published verbatim handled (who may request one, whether the page shows a correction notice), and does the `mise_a_jour` field in the open-data file ever reflect a textual correction?
8. Is the `thematiques` vocabulary maintained as a thesaurus with definitions, scope notes or a hierarchy, and can it be published as such under Licence Ouverte so that third parties can align their own theme taxonomies to it?
9. Does the daily `vp_discours.json` carry deletions (records removed after a takedown request), and is there a changelog or an incremental feed planned?
10. Has DILA ever received a notice, complaint or CADA request concerning the reproduction of a broadcast interview text in the collection, and what was the outcome?

To the SIG:

11. Under which contract (title, BOAMP reference) are the verbatims of ministers' broadcast interviews produced, what does the contract say about the ownership and reuse of the transcripts, and are they human-typed or ASR-based?
12. Does the SIG's media monitoring during a presidential campaign produce verbatims of the candidates who are not members of the Government, and if so, are they public-information documents communicable under CRPA L.311-1 and reusable under L.321-1 et seq.?
13. Does the SIG's arrangement with broadcasters for its « veille audiovisuelle » (recordings, montages, transcripts) include any clause on redistribution, and does it regard the text of a broadcast interview as covered by the broadcaster's neighbouring right?
14. Has any broadcaster or journalists' organisation objected to the publication of SIG verbatims on Vie-publique.fr?

---

## Sources

vie-publique.fr (via Internet Archive captures; timestamp = capture):
- Mentions légales, page dated 3 July 2020: https://web.archive.org/web/20230206143208/https://www.vie-publique.fr/mentions-legales
- Utiliser nos contenus, page dated 1 March 2023: https://web.archive.org/web/20260117015252/https://www.vie-publique.fr/utiliser-nos-contenus
- Qui sommes-nous ?, page dated 2 September 2025: https://web.archive.org/web/20260308061033/https://www.vie-publique.fr/qui-sommes-nous
- Collection des discours publics (home): https://web.archive.org/web/20260124204054/https://www.vie-publique.fr/collection-discours-publics
- Discours publics listing (« plus de 160 000 »): https://web.archive.org/web/20260118041139/https://www.vie-publique.fr/discours
- Discours dans l'actualité: https://web.archive.org/web/20260212165133/https://www.vie-publique.fr/discours-dans-lactualite ; 14 July interviews page (275023): https://web.archive.org/web/20220822164251/https://www.vie-publique.fr/discours-dans-lactualite/275023-les-interviews-televisees-des-presidents-de-la-republique-du-14
- Flux RSS: https://web.archive.org/web/20260112111527/https://www.vie-publique.fr/flux-rss ; Espace presse: https://web.archive.org/web/20260213004736/https://www.vie-publique.fr/espace-presse
- sitemap.xml: https://web.archive.org/web/20260201000338/https://www.vie-publique.fr/sitemap.xml ; discours/sitemap.xml: https://web.archive.org/web/20260117221726/https://www.vie-publique.fr/discours/sitemap.xml ; robots.txt: https://web.archive.org/web/20220102211606/https://www.vie-publique.fr/robots.txt
- Discours pages: 300132 Vautrin BFM TV 27 Aug 2025: https://web.archive.org/web/20260214014708/https://www.vie-publique.fr/discours/300132-catherine-vautrin-27082025-bfm-crise-des-pme-vote-de-confiance-gpa ; 280375 Beaune Public Sénat 10 June 2021: https://web.archive.org/web/20260209030735/https://www.vie-publique.fr/discours/280375-entretien-clement-beaune-10062021-politique-gouvernementale ; 184912 Hollande L'Express 10 Apr 2012: https://web.archive.org/web/20260208192430/https://www.vie-publique.fr/discours/184912-interview-de-m-francois-hollande-depute-ps-et-candidat-lelection-p ; 184916 and 184947 Sarkozy 2012: https://web.archive.org/web/20220928163952/https://www.vie-publique.fr/discours/184916-interview-de-m-nicolas-sarkozy-candidat-lelection-presidentielle-d , https://web.archive.org/web/20210119190305/https://www.vie-publique.fr/discours/184947-declaration-de-m-nicolas-sarkozy-candidat-lelection-presidentielle ; 184977 debate 2012: https://web.archive.org/web/20220518055736/https://www.vie-publique.fr/discours/184977-debat-televise-entre-mm-nicolas-sarkozy-president-de-la-republique-et ; 166574 debate 2007: https://web.archive.org/web/20200730001947/https://www.vie-publique.fr/discours/166574-debat-televise-entre-mme-segolene-royal-depute-ps-et-m-nicolas-sarkoz ; 148596 debate 1995: https://web.archive.org/web/20220501204502/https://www.vie-publique.fr/discours/148596-debat-televise-et-radiodiffuse-entre-les-candidats-au-deuxieme-tour-de-l

Documentation française (2002 site, Internet Archive):
- Présentation de la collection des discours publics: https://web.archive.org/web/20021002221149/http://discours-publics.ladocumentationfrancaise.fr/logos/presentation/presentation.htm
- Aide à la consultation: https://web.archive.org/web/20020810235942/http://discours-publics.ladocumentationfrancaise.fr/logos/aide/aide.htm

DILA:
- Open-data directory: https://echanges.dila.gouv.fr/OPENDATA/DISCOURS_PUBLICS/ (vp_discours.json 2026-09-05; Specifications-datagouv-referentiel-discours_V1_20251126.pdf; DILA_Discours publics_Presentation_20251126.pdf)
- data.gouv.fr dataset record: https://www.data.gouv.fr/api/1/datasets/discours-publics-metadonnees-de-vie-publique-fr/ (id 692efee34bc7205826d04002; page https://www.data.gouv.fr/datasets/metadonnees-des-discours-publics-de-vie-publique-fr) ; réutilisation record: https://www.data.gouv.fr/api/1/reuses/collection-des-discours-publics/
- Mentions légales dila.gouv.fr (23 July 2024): https://www.dila.gouv.fr/informations-sur-le-site/article/mentions-legales
- Répertoire des informations publiques, Les données du débat public (30 Oct 2019): https://www.dila.gouv.fr/services/repertoire-des-informations-publiques/les-donnees-du-debat-public
- Rapport d'activité 2019 (p. 28): https://www.dila.gouv.fr/IMG/pdf/ra_dila_2019.pdf ; 2024: https://www.dila.gouv.fr/IMG/pdf/rapport_dila_2024_accessible.pdf ; 2025 (p. 38-39): https://www.dila.gouv.fr/IMG/pdf/rapport_dila_2025-_web_accessible.pdf ; 2012: https://www.dila.gouv.fr/IMG/pdf/ra_dila_2012.pdf ; 2013: https://www.dila.gouv.fr/IMG/pdf/ra_dila_2013.pdf
- Dossier de presse « Vie-publique.fr fête ses 20 ans » (2022, p. 12): https://www.dila.premier-ministre.gouv.fr/IMG/pdf/maqu_2209_com_01_dossierpresse_vp_v4.pdf ; fiche « www.vie-publique.fr Au cœur du débat public »: https://www.dila.gouv.fr/IMG/pdf/contenus_vie-publique.fr.pdf
- DILA news, « Les interviews télévisées des présidents de la République pour le 14 juillet »: https://www.dila.gouv.fr/actualites/toutes-les-actualites/informations-citoyennes/les-interviews-televisees-des-presidents-de-la-republique-pour-le-14-juillet

SIG (info.gouv.fr, via Internet Archive):
- Histoire du SIG: https://web.archive.org/web/20240403161756/https://www.info.gouv.fr/organisation/service-d-information-du-gouvernement-sig/histoire-du-sig
- SIG landing page: https://web.archive.org/web/20260115210819/https://www.info.gouv.fr/organisation/service-d-information-du-gouvernement-sig
- Répertoire d'informations publiques du SIG: https://web.archive.org/web/20240815054438/https://www.info.gouv.fr/organisation/service-d-information-du-gouvernement-sig/repertoire-dinformations-publiques
- Les marchés publics: https://web.archive.org/web/20240403161541/https://www.info.gouv.fr/organisation/service-d-information-du-gouvernement-sig/les-marches-publics
- SIG datasets on data.gouv.fr: https://www.data.gouv.fr/api/1/organizations/service-d-information-du-gouvernement/datasets/

Cour des comptes, Parliament:
- Cour des comptes, Organisation et fonctionnement du service d'information du Gouvernement, communication au Premier ministre, September 2012 (p. 31): https://www.vie-publique.fr/files/rapport/pdf/124000512.pdf
- Sénat, rapport n° 394 (2002-2003), La Documentation française : la réforme nécessaire pour un éditeur public de référence, ch. IV: https://www.senat.fr/rap/r03-394/r03-3944.html
- Assemblée nationale, question écrite n° 11845 (17e législature), question JO 23 Dec 2025 p. 10411, réponse JO 3 Mar 2026 p. 1872: https://questions.assemblee-nationale.fr/dyn/17/questions/QANR5L17QE11845.pdf

Secondary (used only for pointers, not for claims): Jurisguide fiche « Vie.publique.fr » (BIU Cujas, updated 15 July 2026): https://www.jurisguide.fr/fiches-documentaires/vie-publique-fr-1 ; Wikipédia « Vie-publique.fr » (cites the arrêté du 5 juillet 2002): https://fr.wikipedia.org/wiki/Vie-publique.fr

Blocked today (tagged UNVERIFIED where relied on): Légifrance (Cloudflare challenge, décrets 2010-31 and 2000-1027 and arrêté du 5 juillet 2002 not re-read); info.gouv.fr live pages (403); vie-publique.fr live pages, RSS and sitemaps (JS challenge); calame.ish-lyon.cnrs.fr (connection reset); data.gouv.fr discussions endpoint (connection reset); CADA search.

---

## Appendix A. `thematiques` values with record counts (whole collection, file of 2026-09-05)

Relations bilatérales France (13157), Politique gouvernementale (8062), Parti politique (6421), Politique économique (3064), Politique étrangère (3064), Construction européenne (2568), Distinction (1895), Guerre (1648), Terrorisme (1628), Santé publique (1623), Politique de la défense (1518), Diplomatie (1484), Syndicat (1434), Logement (1433), Relations bilatérales Europe (1428), Fonction publique (1423), Aide internationale (1370), Sport (1362), Budget de l'État (1315), Élection présidentielle (1300), Histoire (1280), Emploi (1200), Commerce international (1158), Aménagement du territoire (1133), Femme (1121), Outre-mer (1083), Tourisme (1076), Politique agricole (1073), Retraite (980), Immigration (966), Enseignement supérieur (933), Politique commune (929), Situation économique (902), Climat (895), Coopération (891), Politique de l'emploi (885), Jeune (879), Maladie (849), Personnalité politique (846), Protection de l'environnement (840), Handicapé (830), Politique de l'enseignement (804), Armement (802), Art (791), Politique culturelle (786), Justice (786), Urbanisme (770), Sécurité sociale (762), Décentralisation (748), Profession (723), Politique sociale (716), Institutions européennes (688), Chômage (684), Francophonie (675), Collectivité locale (664), Temps de travail (659), Épidémie (658), Formation (641), Personne âgée (640), Parlement (631), Économie numérique (628), Politique de l'environnement (625), Élection (617), Relations du travail (609), Ordre public (599), Politique industrielle (596), Organisation internationale (587), Droits de l'homme (586), Production agricole (583), Politique des transports (572), Internet (570), Famille (554), Police (550), Média (542), Armée (527), Politique de l'énergie (525), Pollution (522), Traité européen (520), Ukraine (496), Fiscalité (473), Constitution européenne (472), Catastrophe naturelle (468), Salaire (455), Délinquance (431), Politique agricole commune (424), Monnaie (422), Religion (418), Politique de l'immigration (412), Mineur (404), Situation internationale (401), Soin médical (391), Hôpital (390), Transport ferroviaire (388), Violence (385), Sécurité routière (385), PME (381), Télévision (381), Télécommunications (373), Politique de la recherche (369), Français à l'étranger (365), Technologie (350), Scolarité (340), Marché financier (338), Président de la République (337), Politique budgétaire (336), Transport aérien (336), Politique judiciaire (335), Proche-Orient (332), Commerce (331), Consommation (329), Élections européennes (326), Gouvernement (321), Élevage (319), Secteur industriel (316), Idéologie (312), Presse (308), Mouvement politique (301), Antisémitisme (293), Transport routier (292), Pêche (285), Gestion d'entreprise (284), Régime politique (283), Union économique et monétaire (282), Irak (280), Patrimoine culturel (279), Laïcité (279), Élections municipales (274), Élargissement de l'UE (273), Région (272), Loi (268), Banque (268), Étranger (265), Drogue (261), Conditions de travail (256), Israël (255), Otage (254), OTAN (253), Patrimoine naturel (253), Gendarmerie (250), Prison (245), Cinéma (244), Livre (243), Exclusion sociale (242), Service public (238), Zone euro (234), Artisanat (229), Eau (225), Assurance maladie (225), Procédure judiciaire (223), Assurance chômage (219), Transport maritime (216), Racisme (214), État (214), Matière première (212), Loisir (210), Profession judiciaire (210), Investissement (210), Banlieue (210), Établissement public (209), Relations économiques internationales (208), Réforme constitutionnelle (208), Mer (207), Espace (204), Industrie automobile (203), Médicament (203), Élections législatives (203), Situation sociale (203), Réforme de l'État (202), Enseignant (201), Militaire (199), Prix (199), Liban (196), Industrie aéronautique (196), Pauvreté (196), Ville (193), Sommet international (193), Enseignement professionnel (191), Budget européen (189), Enseignement privé (187), Énergie nucléaire (186), Ministère (186), Établissement scolaire (186), Relations administration usager (186), Association (185), Musée (182), Carburant (181), Enseignement en alternance (181), Bioéthique (178), Finances locales (178), Profession médicale (177), Simplification administrative (177), Recherche développement (169), Programme scolaire (169), Contrat de travail (167), Politique fiscale (163), Mayotte (160), Organisme public (159), Afghanistan (159), Insertion professionnelle (158), Propriété intellectuelle (158), Iran (154), Discrimination (154), Kosovo (152), Syrie (146), Alimentation (146), Patronat (145), Niveau de vie (145), Impôt (144), Déchet (143), Allemagne (138), Insertion sociale (137), Référendum (137), Produit agroalimentaire (136), Création d'entreprise (134), Code (133), Élu (133), Intervention militaire (132), Criminalité (131), Peine (130), Revenu (128), Institution (125), Zone rurale (125), Situation politique (125), Algérie (124), Transport en commun (123), Minorité (122), Taxe (121), Étudiant (120), Médecine (120), Électricité (119), Gestion publique (119), Financement des partis politiques (119), Enseignement secondaire (118), Partenaires sociaux (116), Chine (116), Économie sociale (116), Coopération européenne (116), Droit du travail (115), Protection du patrimoine (112), Royaume-Uni (111), Sécurité nucléaire (111), Organisation judiciaire (111), Secteur public (111), Prestation sociale (110), Langue (110), Polynésie française (108), Démographie (106), Préfecture (105), Lycée (105), Bâtiment et travaux publics (104), États-Unis (103), Russie (102), Dette publique (102), Libye (100), Égalité professionnelle (100), Licenciement (99), Moyen-Orient (98), Afrique subsaharienne (98), Industrie nucléaire (98), Crédit (97), Grève (96), Épargne (95), Situation matrimoniale (92), Marché commun (91), Entreprise en difficulté (90), Crime contre l'humanité (90), Assurances (89), Diplôme (86), Arménie (85), Énergie renouvelable (85), Qualité des produits (85), Structure d'entreprise (85), Droit public (84), Consommation d'énergie (82), Profession artistique (82), Innovation (80), Frontière (80), Égalité des chances (80), Risque professionnel (80), Migration (79), Biodiversité (79), Construction navale (79), Renseignement (78), Tabac (78), Constitution (78), Entreprise de services (78), Citoyenneté (77), Commune (76), Juridiction (76), Entreprise publique (76), Pouvoir exécutif (76), Marine nationale (75), Enfant (74), Concurrence (74), Afrique du Sud (74), La Réunion (74), Élections régionales (74), Compétitivité (73), Droit civil (73), Guyane (72), Marché du travail (72), Élection cantonale (71), Droit des sociétés (70), Nationalité francaise (70), Droit européen (69), Premier ministre (68), Libre circulation des personnes (68), Transport fluvial (67), Enseignement primaire (65), Politique européenne de sécurité et de défense (65), Droit international (64), Stratégie politique (64), Haïti (62), Jeux Olympiques et Paralympiques (62), Côte d'Ivoire (62), Équipement culturel (61), Libre échange (60), Bibliothèque (60), Coopération intercommunale (60), Écologie (59), Identité nationale (59), Formalité administrative (58), Organisme de recherche (57), Profession paramédicale (57), Prélèvement obligatoire (57), Archives (56), Inégalité sociale (56), Organisation administrative (55), Département (55), Droit (55), Négociation collective (55), Conseil de l'Europe (54), Téléphone (54), Catégorie socioprofessionnelle (54), Littoral (52), Maltraitance (52), Déconcentration (52), Mutuelle (52), Pouvoir judiciaire (52), Organisation du travail (51), Élève (51), Communication (51), Niveau scolaire (51), Politique monétaire (51), Droit commercial (51), Mali (50), Industrie culturelle (50), Radio (50), Équipement médical (50), Vacances (49), Pologne (49), Intelligence artificielle (47), Harcèlement (46), Libertés publiques (46), Élections prud'homales (46), Mers et océans (45), Travail dissimulé (45), Soudan (43), Métropole (43), Retraite complémentaire (43), Exploitation agricole (42), République démocratique du Congo (42), Éthique (42), Nouvelle-Calédonie (41), Libéralisme (41), Turquie (40), Transport des marchandises (40), Coopération interrégionale (40), Italie (39), Pratique culturelle (39), Grèce (39), Administration locale (39), Reconversion industrielle (39), Japon (37), Protection des données (37), Industrie textile (36), Établissement sanitaire (36), Europe de l'Est (36), Afrique (36), Rwanda (35), Géorgie (35), Programme européen (35), Niger (35), FMI (35), Illettrisme (35), Canada (34), Police municipale (34), Liberté d'expression (34), Élections sénatoriales (34), Justice Affaires intérieures (34), Carrière professionnelle (33), Marine marchande (32), Inde (31), Guadeloupe (31), Cambodge (30), Profession libérale (30), Aviation civile (30), Fiscalité locale (30), GRH (30), Droit pénal (29), Venezuela (29), Tunisie (29), Industrie sidérurgique (28), Éthiopie (28), Enseignement public (28), Transport urbain (28), Moldavie (27), Roumanie (27), Maroc (26), Libertés individuelles (26), Amérique centrale (26), Brésil (25), Épargne salariale (25), Madagascar (25), Serbie (25), Sexualité (25), Australie (24), Espagne (23), Sénégal (23), Alcool (23), Administration centrale (22), Indonésie (22), Qatar (22), Angola (21), Martinique (20), Pouvoir législatif (20), Azerbaïdjan (19), Lituanie (19), Corée du Nord (19), Télétravail (19), Assurance vieilllesse (19), Protectionnisme (19), Arabie saoudite (18), Groupe de pression (18), Somalie (18), Albanie (17), Égypte (17), Cameroun (17), Timor oriental (17), Parlement européen (17), Entreprise à l'étranger (17), OCDE (17), Chypre (16), Transition écologique (16), Corée du Sud (16), Tchad (16), Djibouti (16), Équipement collectif (16), Entreprise étrangère (15), ONU (15), Chili (15), Belarus (15), Prévision économique (15), Opinion publique (15), Sécurité civile (14), Émirats arabes unis (14), État de Palestine (14), Suisse (13), Togo (13), Pays-Bas (13), Clinique (13), Salvador (13), Santé mentale (12), Suède (12), Comores (12), Congo (12), Mexique (11), République centrafricaine (11), Myanmar (11), Panama (11), Namibie (11), Développement durable (11), Macédoine (11), Sri Lanka (11), Argentine (10), Andorre (10), Technique agricole (10), Irlande (10), Réseaux sociaux (10), Vietnam (10), Kazakhstan (10), Nigéria (10), Portugal (10), République Tchèque (10), Risque (10), Cuba (9), Danemark (9), Guatémala (9), Géographie (9), Luxembourg (9), Burkina Faso (9), Burundi (9), Cybercriminalité (8), Protection civile (8), Fin de vie (8), Commémoration (8), Hongrie (8), Données numériques (8), Ouzbékistan (8), Taïwan (8), Jordanie (8), Nicaragua (8), Philippines (8), Yémen (8), Guinée (8), Kenya (7), Thaïlande (7), Bénin (7), Pakistan (7), Croatie (7), Dissuasion nucléaire (6), Mongolie (6), Koweït (6), Colombie (6), Finlande (6), Bulgarie (6), Élections départementales (6), Enseignement préscolaire (6), Antarctique (5), Mauritanie (5), Slovénie (5), Malaisie (5), Maurice (5), Papouasie-Nouvelle-Guinée (5), Secte (5), Slovaquie (5), Mozambique (5), Érythrée (5), Monténégro (4), Norvège (4), Bosnie-Herzégovine (4), Macédoine du Nord (4), Singapour (4), Bahreïn (4), Ghana (4), Libéria (4), Nouvelle-Zélande (4), Guinée-Bissau (4), Asie du Sud-Est (4), Pays du pacifique (4), Bangladesh (4), Malte (4), France (4), Français de l'étranger (3), Gabon (3), Vatican (3), Monaco (3), Océan (3), Équateur (3), Suriname (3), Belgique (3), Monde (3), Estonie (3), Vanuatu (3), Décès (3), Tadjikistan (3), Afrique occidentale (3), Lettonie (3), Bolivie (3), Oman (2), Droit d'asile (2), Conseil d'État (2), Mer méditerranée (2), Tanzanie (2), Cour des comptes (2), Sécurité maritime (2), Sierra Leone (2), Guyana (2), Amérique du Sud (2), Costa Rica (2), Sahara occidental (2), Union européenne (2), Guinée équatoriale (2), Conseil constitutionnel (1), Islande (1), Économie circulaire (1), Antigua-et-Barbuda (1), Géopolitique (1), Kirghizistan (1), Rénovation énergétique (1), Espace Schengen (1), Paraguay (1), Bhoutan (1), Laos (1), Autriche (1), Europe centrale (1), Jamaïque (1), Barbade (1), Culture - Médias (1), Énergie - Transports (1), Pérou (1), Botswana (1), Concours (1), Honduras (1), Asie (1), Népal (1), Fidji (1)
