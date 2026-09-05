# Seed catalogue: Appearances since 27 August 2026 and declared candidates

Resolves issue #12 of the wayfinder map (#5). Catalogue date: **2026-09-05**. Written before the data-model ticket (#14) closed, so the format is this Markdown file; the rows are meant to be re-keyed into whatever `data/` layout that ticket fixes. Every row records what was checked and when; `UNVERIFIED` marks a field that could not be read from a primary source on the catalogue date (YouTube blocked anonymous metadata reads during the second half of the session, so several durations come from programme listings, not from the video).

Conventions used here (see `CONTEXT.md` and ADR 0003):

- **Acquisition basis** per Appearance: `mining-exception` for Public Sénat, LCP and parties' own channels; `tolerated` for TF1/LCI, France Télévisions, Radio France, CNews/Europe 1, BFMTV/RMC (all opted out of text-and-data mining, see `docs/research/source-terms.md`); `by-ear` if a Source objects; `licensed` if one is granted. Libération is not in the source-terms inventory yet, so its row says `tolerated (to check)`.
- **Copy to download and embed**, in ADR 0003 order: the Source's own YouTube or Dailymotion upload, then a co-broadcaster's, then the organiser's; other carriers listed.
- **Account wall**: flagged when the only replay sits behind TF1+ or RMC+; those are the cases the off-air fallback of ADR 0003 would need.
- **Candidate** is read as `CONTEXT.md` defines it (a Speaker who has publicly declared a run). Contenders in a primary and "putative" candidates are listed separately and every Appearance that involves one is flagged **borderline**; whether they belong in the seed corpus is a decision for the map, not for this catalogue (see section 5).

## 1. Row counts

| Table | Rows |
|---|---|
| Multi-candidate debates since 27 Aug 2026, core (only declared Candidates) | 2 |
| Multi-candidate debates since 27 Aug 2026, borderline (a primary contender or a putative candidate on stage) | 2 |
| Announced debates after the catalogue date (not yet Appearances) | 3 |
| Declared candidates to the election | 22 (+2 listed by a single secondary source) |
| Contenders in a primary | 10 (7 socialist primary, 3 united-left primary) |
| Long TV or radio interviews found, one per person | 11 of 32 with a TV or radio interview since 1 July 2026; 7 more with an earlier 2026 one; 14 with none found or only a non-broadcast video |

## 2. Multi-candidate debates since 27 August 2026

### 2.1 Core rows (every participant is a declared Candidate)

| # | Date | Source (producer) | Host medium | Participants | Duration | Official replay | Platform / copy to download and embed | Acquisition basis | Account wall | Verified |
|---|---|---|---|---|---|---|---|---|---|---|
| D1 | 2026-08-27, 16:45 | **LCI** (TF1 group), exclusive live; organiser MEDEF (REF 2026, court Philippe-Chatrier, Roland-Garros); presenter Amélie Carrouër; questions from five business owners chosen after a MEDEF/OpinionWay consultation | TV (news channel), simulcast TF1 Info, LCI YouTube and X | Gabriel Attal, Raphaël Glucksmann (primary contender, see 2.2 note), Marine Le Pen, Jean-Luc Mélenchon, Édouard Philippe, Bruno Retailleau, Marine Tondelier (primary contender) | 3 h 04 min 15 s (LCI YouTube, `PT184M15S`) | LCI YouTube `https://www.youtube.com/watch?v=rpURHoN54bQ` (archived live, **embedding disabled**); franceinfo "REPLAY" article; TF1+ replay (account) | Download: LCI copy `rpURHoN54bQ`. Embed: organiser's copy MEDEF `@MEDEFtv` `https://www.youtube.com/watch?v=z0gJwsrODEw` ("#LAREF26 \| DÉBAT \| PRÉSIDENTIELLE 2027", published 2026-09-01, 3 h 12 min 34 s, `playableInEmbed:true`). Other carriers: TF1 Info, X | `tolerated` (TF1 opt-out, CG TF1+ I.10 / CGU TF1 Info art. 9, tdmrep) | No (public YouTube); TF1+ copy needs an account | 2026-09-05 |
| D2 | 2026-09-04 (day event 9h–18h) | Colloquium of the movement **Utiles** (Bertrand Pancher), Palais du Luxembourg (Sénat), theme "Préparer le monde de demain et l'alternative"; the Bertrand–Cazeneuve exchange was covered by BFMTV | In-room debate; broadcaster unknown | Xavier Bertrand, Bernard Cazeneuve (Marine Tondelier also on the programme; François Hollande invited, attendance UNVERIFIED) | UNVERIFIED | **None located** on the catalogue date: no Utiles, Public Sénat or Sénat video found; BFMTV published extracts | UNVERIFIED (Sénat's own video portal `videos.senat.fr` does not carry external colloquia by default) | UNVERIFIED (depends on who recorded it) | Unknown | 2026-09-05 |

Note on D1: Glucksmann and Tondelier are contenders in primaries, not declared candidates to the election itself; the debate stays "core" because five of seven participants are declared Candidates and it is the seed of the whole effort (ADR 0003 makes it the prototype's first import). Note on D2: it counts as core only if a recording exists; otherwise it is a two-person exchange with no Source and cannot be imported.

### 2.2 Borderline rows (a primary contender or an undeclared "putative" candidate on stage)

| # | Date | Source (producer) | Host medium | Participants | Duration | Official replay | Platform / copy | Acquisition basis | Account wall | Why borderline |
|---|---|---|---|---|---|---|---|---|---|---|
| D3 | 2026-08-29, 16:45 | **LCI**, presenter Darius Rochebin, from the 3rd summer university of the Laboratoire de la République (Jean-Michel Blanquer), Sens (Yonne); title "France 2027, quelles perspectives ?" | TV (news channel), simulcast TF1 Info, LCI YouTube and X | Édouard Philippe (declared), François Hollande (undeclared; says he will decide in December 2026) | UNVERIFIED (listing shows a 16:45 slot; programme guide gives 16:45–17:00 which is a slot length, not the debate) | LCI YouTube `https://www.youtube.com/watch?v=sp-2F_cTTxA` ("Le débat entre Édouard Philippe et François Hollande｜LCI", oEmbed answers, so embeddable) | Download and embed: LCI copy `sp-2F_cTTxA` | `tolerated` | No | Hollande is not a Candidate |
| D4 | 2026-09-02, 19:00–20:30 | **Libération** ("Libé 2027", first public meeting), Académie du Climat, Paris, before 250 citizens; moderated by Sonia Delesalle-Stolper and Thomas Legrand; carried live by BFM2 and the BFM app | Newspaper's own live stream (Twitch, YouTube) plus BFM2 | François Ruffin (united-left primary contender), Dominique de Villepin (undeclared) | about 1 h 30 (scheduled 19:00–20:30; UNVERIFIED against the video) | Libération YouTube `https://www.youtube.com/watch?v=D7vTQp2iM00` ("«Libé 2027» : suivez François Ruffin et Dominique de Villepin en débat", live archive of 2 Sept 2026, oEmbed answers) | Download and embed: Libération copy `D7vTQp2iM00`; other carrier BFM2 / BFM app (RMC+) | `tolerated (to check)`: Libération's CGU and tdmrep not yet inventoried in `source-terms.md` | No for YouTube; BFM2 replay via RMC+ needs an account | Neither participant is a declared Candidate; Ruffin runs in the united-left primary |

### 2.3 Announced after the catalogue date (socialist primary debates, not yet Appearances)

| Date | Source | Status on 2026-09-05 | Contenders concerned |
|---|---|---|---|
| 2026-09-16 | TF1 | Proposed; Raphaël Glucksmann refuses any debate other than the public-service one, the other contenders want all three (LCP, 2 Sept 2026) | Socialist primary contenders |
| 2026-09-29 | BFMTV | Proposed, same dispute | Socialist primary contenders |
| 2026-10-06 | France 2 and France Inter | Set; falls after the 5 Oct voter-registration deadline of the primary | Socialist primary contenders |

The united-left primary (Massard, Ruffin, Tondelier; vote 11 Oct 2026) has no debate announced. Fabien Roussel (PCF) is expected to declare on 6 Sept 2026.

## 3. Declared candidates as of 2026-09-05

### 3.1 Declared to the presidential election

Sources: `fr.wikipedia.org/wiki/Candidatures_à_l'élection_présidentielle_française_de_2027` (read 2026-09-05), LCP "la liste des candidats déjà en lice" (updated 2026-09-04), Sud Radio "le point sur toutes les candidatures" (2026-08-24), franceinfo. Where sources disagree the row says so.

| Name | Party | Declaration date | Declaration occasion / source | Note |
|---|---|---|---|---|
| Nathalie Arthaud | Lutte ouvrière | 2025-12-08 | Party announcement (frwiki) | 4th run |
| François Asselineau | UPR | 2023-08-31 | Interview, Le Dauphiné libéré (frwiki) | |
| Gabriel Attal | Renaissance | 2026-05-22 | Public event, Mur-de-Barrez (Aveyron) (frwiki, LCP) | |
| Delphine Batho | Génération écologie | 2025-11-25 | Interview, Le Nouvel Obs (frwiki, franceinfo) | |
| Xavier Bertrand | Nous France (ex-LR) | 2024-02-03 (frwiki, Ouest-France) / confirmed 2026-08-27 at the MEDEF REF (LCP, franceinfo) | He says the formal declaration comes "à la fin de l'année" | Date disputed between sources; catalogue keeps both |
| Karim Bouamrane | PS (outside the primary) | 2026-06-09 | Interview, France Inter (frwiki) | Refuses the socialist primary |
| Bernard Cazeneuve | La Convention | 2026-07-16 (frwiki, Le Parisien) / "official since 16 June" (Sud Radio) | Interview, Le Parisien | Refuses the socialist primary |
| Nicolas Dupont-Aignan | Debout la France | 2025-03-08 | Rally, Yerres (frwiki) | Rentrée 19 Sept 2026 |
| Sylvain Durif | Elvita | 2026-08-23 | Video on social networks (frwiki, cultinfos) | |
| Clara Egger | Solution démocratique | 2026-04-20 | Press release on the movement's site (LCP, Sud Radio) | Not in the frwiki list as read |
| Anasse Kazib | Révolution permanente | 2026-06-01 | Campaign clip on social networks (frwiki) | |
| Selma Labib | NPA – Révolutionnaires | 2026-06-17 | Party announcement (frwiki) | |
| Francis Lalanne | France Libre | 2026-08-19 | Announcement, first rally planned in Paris (frwiki, LCP) | |
| Marine Le Pen | Rassemblement national | 2026-07-07 | Journal de 20 heures, TF1 (Gilles Bouleau), the evening of the appeal ruling (frwiki, coulisses-tv) | "Candidate naturelle" since Sept 2023 |
| David Lisnard | Nouvelle Énergie | 2026-03-31 | Announcement (frwiki, LCP) | frwiki files him under "other primaries" (a right-wing primary that does not exist yet); LCP lists him as declared |
| Benoît Mathieu | Sans étiquette | 2026-03-30 | Campaign-tour announcement (frwiki) | |
| Jean-Luc Mélenchon | La France insoumise | 2026-05-03 | Journal de 20 heures, TF1 (frwiki) | 4th run |
| Antoine Mikolajczak | Équinoxe | 2026-06-27 | Before party members (LCP, Sud Radio) | Not in the frwiki list as read |
| Manolo Mlekuz | Trajectoire | UNVERIFIED | Tour de France for endorsements (frwiki) | Youngest declared candidate |
| Édouard Philippe | Horizons | 2024-09-03 | Interview, Le Point (frwiki) | |
| Florian Philippot | Les Patriotes | 2026-05-09 | Announcement on France 2 (frwiki) | Sud Radio: "Sovereign Union" |
| Bruno Retailleau | Les Républicains | 2026-04-19 | Internal party consultation (frwiki) | |
| Benjamin Lucas | Génération.s | UNVERIFIED | Sud Radio only | Single secondary source; not in frwiki or LCP as read |
| Juan Branco | — | 2025-12-19 | Sud Radio only | Single secondary source; not in frwiki or LCP as read |

### 3.2 Contenders in a primary

| Name | Party | Primary | Declaration date | Occasion / source |
|---|---|---|---|---|
| Philippe Brun | PS | Socialist primary (9–10 Oct, 2nd round 16–17 Oct 2026) | 2026-06-30 | RMC (frwiki, franceinfo) |
| Olivier Faure | PS | Socialist primary | 2026-08-30 | Message to deputies 29 Aug, then Journal de 20 heures TF1 (Anne-Claire Coudray) at the close of the PS campus in Blois (frwiki, coulisses-tv) |
| Raphaël Glucksmann | Place publique | Socialist primary | 2026-08-23 | Journal de 20 heures, TF1 (Audrey Crespo-Mara) (coulisses-tv, RTS) |
| Jérôme Guedj | PS | Socialist primary | 2026-02-05 (France Inter) / joined the primary 2026-08-23 | frwiki, LCP |
| Emmanuel Maurel | Gauche républicaine et socialiste | Socialist primary | 2026-09-04 | Announcement (frwiki, LCP); medium UNVERIFIED |
| Ségolène Royal | PS | Socialist primary | 2026-07-10 | Announcement (frwiki, LCP) |
| Fabien Verdier | Divers gauche | Socialist primary | 2026-09-02 (Libération interview) / 2026-09-03 (AFP) | frwiki, LCP |
| Lydie Massard | Union démocratique bretonne | United-left primary (11 Oct 2026) | 2026-04-02 | Announcement (frwiki) |
| François Ruffin | Debout ! | United-left primary | 2025-04-01 | Rally, Montreuil (frwiki) |
| Marine Tondelier | Les Écologistes | United-left primary | 2025-10-22 | Party nomination (frwiki) |

Withdrawn: Clémentine Autain (L'Après) left the united-left primary on 2026-07-11. Putative (not Candidates on 2026-09-05): François Hollande (decision in Dec 2026), Dominique de Villepin, Fabien Roussel (announcement expected 6 Sept 2026), Éric Zemmour, Bruno Le Maire, Élisabeth Borne, Olivier Becht.

## 4. One recent long TV or radio interview per person

"Long" here means a sit-down political interview of 20 minutes or more, or the channel's flagship political interview format. Where only a short news-bulletin slot was found since the MEDEF debate, the row says so and gives the last long one. Ordered as in section 3.

### 4.1 Declared candidates

| Candidate | Date | Source | Programme, journalist | Medium | Duration | Official replay | Copy to download / embed | Acquisition basis | Account wall | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| Nathalie Arthaud | 2026-05-20 | BFMTV | "Interview-débat" on the crisis (per Lutte ouvrière's portal) | TV | UNVERIFIED | Linked from `lutte-ouvriere.org/portail/multimedia` | BFMTV YouTube copy UNVERIFIED | `tolerated` | No | Also France TV "Les 4 Vérités" 2026-04-25 (short). Nothing found since 27 Aug |
| François Asselineau | none found in 2026 | — | Last found: Sud Radio "Bercoff dans tous ses états", 2025-09-18 | Radio | — | sudradio.fr | — | Sud Radio not inventoried | — | **Gap** |
| Gabriel Attal | 2026-09-01 | France 2 | Journal de 20 heures, new rubric "France 2027 – l'invité du 20h" (Jean-Baptiste Marteau, Neila Latrous, Benjamin Duhamel) | TV | about 20 min (format announced as 20 min) | franceinfo JT replay `https://www.franceinfo.fr/replay-jt/france-2/20-heures/jt-de-20h-du-mardi-01-septembre-2026_8143940.html` (whole JT, 1 h 00) | France Télévisions player (export for "particuliers" only); franceinfo YouTube copy UNVERIFIED | `tolerated` | No | Last hour-long: "Face à BFM" with Alain Duhamel, BFMTV, 2026-05-03 |
| Delphine Batho | 2026-06-07 | franceinfo (Radio France / France Télévisions) | "8h30 franceinfo" | Radio + TV | about 25 min | `https://www.franceinfo.fr/replay-radio/8h30-fauvelle-dely/affaire-lyhanna-presidentielle-2027-l-interview-de-delphine-batho_7997384.html` | franceinfo YouTube `https://www.youtube.com/watch?v=K8_1whQek38` | `tolerated` | No | Nothing found since 27 Aug |
| Xavier Bertrand | 2026-08-27 | MEDEF REF (stage), reported by LCP and franceinfo | Stage Q&A at the REF where he confirmed he "will be" a candidate | In-room | UNVERIFIED | UNVERIFIED (MEDEF `@MEDEFtv` uploads to check) | — | organiser copy would be YouTube ToS only | — | No TV or radio long interview found since July; Ouest-France print interview (Aug 2026). **Gap** |
| Karim Bouamrane | 2026-09-02 | BFMTV | Face-to-face with Charles Consigny (programme name UNVERIFIED) | TV | UNVERIFIED | bfmtv.com article (titrespresse relay) | BFMTV YouTube copy UNVERIFIED | `tolerated` | RMC+ replay needs an account | Last verified long one: CNews "La grande interview", 2026-06-29, 20 min 46 s, `https://www.youtube.com/watch?v=chF4leeEITk` (embeddable) |
| Bernard Cazeneuve | 2026-09-04 | Utiles colloquium (see D2) | Debate with Xavier Bertrand | In-room | UNVERIFIED | none located | — | — | — | No TV or radio interview found since July. Last long: BFMTV/RMC "Face à Face", 2026-02-23, `https://www.youtube.com/watch?v=kKO15Fugb0w`. **Gap** |
| Nicolas Dupont-Aignan | early 2026 | franceinfo TV, CNews | Interviews Jan–Feb 2026 (Sud Radio relay) | TV | UNVERIFIED | UNVERIFIED | — | `tolerated` | — | Rentrée 2026-09-19 (Yerres). **Gap** since 27 Aug |
| Sylvain Durif | none | — | Declaration video 2026-08-23 on social networks only | — | — | — | — | — | — | **Gap** |
| Clara Egger | none as interviewee | — | She runs a Sunday video series "Présidentielle 2027" interviewing other candidates (Solution démocratique Substack) | — | — | — | — | — | — | **Gap**; her series is itself a possible Source for small candidates (Mathieu #1, Mlekuz #2, Massard #3, Dupont-Aignan #6) |
| Anasse Kazib | 2026-06-01 | own channels | Campaign clip announcing the candidacy (Dailymotion `xacr9l6`) | — | short | `https://www.dailymotion.com/video/xacr9l6` | — | — | — | Not an interview. **Gap** |
| Selma Labib | none | — | — | — | — | — | — | — | — | **Gap** |
| Francis Lalanne | none | — | — | — | — | — | — | — | — | **Gap** |
| Marine Le Pen | 2026-07-02 | LCI | "Le Grand Entretien", Darius Rochebin (eve of the appeal ruling) | TV | UNVERIFIED (LCI's flagship long format) | LCI YouTube `https://www.youtube.com/watch?v=C6XkrrKR5OA` (also `hErXRs9wvro`; both answer oEmbed) | LCI copy | `tolerated` | No | 2026-07-07 Journal de 20 heures TF1 (Gilles Bouleau) is the declaration (about 15 min, 5.85 M viewers). Nothing since 27 Aug; rentrée 13 Sept (Hénin-Beaumont) |
| David Lisnard | 2026-09-03 | CNews with Europe 1 | "La Grande Interview", Laurence Ferrari (La Matinale) | TV + radio | about 20 min | `https://www.cnews.fr/emission/2026-09-03/la-grande-interview-david-lisnard-1913297`; Europe 1 page | CNews YouTube `https://www.youtube.com/watch?v=ESHmQJtoEtE` (oEmbed answers) | `tolerated` | No | |
| Benoît Mathieu | 2026 (date UNVERIFIED) | Solution démocratique (Clara Egger) | "Présidentielle 2027 #1" | Video | UNVERIFIED | `solutiondemocratique.substack.com/p/presidentielle-2027-1-clara-egger` | UNVERIFIED | — | — | Interview by another candidate |
| Jean-Luc Mélenchon | 2026-08-22 | TF1 | Journal de 13 heures, from the AMFIS (Valence) | TV | short (bulletin slot) | melenchon.fr entry; copy `https://www.youtube.com/watch?v=5F2dS9aoyrM` (his channel) | TF1 Info copy UNVERIFIED | `tolerated` | No | No long interview found since the LCI "interview exceptionnelle sur l'international" of 2026-05-08. His 2 Sept 2026 "conférence sur le moment politique" (Paris, before LFI activists, own stream) is not an interview. **Gap** |
| Antoine Mikolajczak | none | — | — | — | — | — | — | — | — | **Gap** |
| Manolo Mlekuz | 2026 (date UNVERIFIED) | Solution démocratique (Clara Egger) | "Présidentielle 2027 #2" | Video | UNVERIFIED | Substack link as above | — | — | — | |
| Édouard Philippe | 2026-08-30 | BFMTV | "Longue interview" in Tourcoing, at Gérald Darmanin's rentrée | TV | UNVERIFIED | bfmtv.com (Yahoo/shango relays); BFMTV YouTube copy UNVERIFIED | UNVERIFIED | `tolerated` | RMC+ replay needs an account | Also "C à vous la suite", France 5, 2026-09-04 (talk-show segment); Réunion La 1ère 2026-08-24 |
| Florian Philippot | none found in 2026 | — | Last: Sud Radio Sept 2025 | — | — | — | — | — | — | **Gap** |
| Bruno Retailleau | 2026-08-26 | BFMTV | Evening interview (19h slot; programme name UNVERIFIED), first "rentrée" interview | TV | UNVERIFIED | BFMTV YouTube extract `https://www.youtube.com/watch?v=8_qNhqsCk7I` (published 2026-08-26); full replay UNVERIFIED | UNVERIFIED | `tolerated` | RMC+ | Last verified long: CNews "La grande interview", 2026-06-30/07-01, `https://www.youtube.com/watch?v=I73AOEJVU1Y` |

### 4.2 Contenders in a primary

| Contender | Date | Source | Programme, journalist | Medium | Duration | Official replay | Copy | Acquisition basis | Account wall | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| Philippe Brun | 2026-06-30 | RMC | Declaration interview | Radio | UNVERIFIED | UNVERIFIED | — | `tolerated` | — | Nothing found since |
| Olivier Faure | 2026-08-30 | TF1 | Journal de 20 heures, Anne-Claire Coudray (declaration) | TV | short (bulletin slot) | TF1+ / TF1 Info | UNVERIFIED | `tolerated` | TF1+ | No long interview found since; **Gap** |
| Raphaël Glucksmann | 2026-08-30, 13:20 | France 2 + France Inter | "Franc-jeu", Benjamin Duhamel (first episode of the new Sunday programme) | TV + radio | 38 min 32 s | `https://www.franceinfo.fr/replay-magazine/france-2/franc-jeu/franc-jeu-avec-raphael-glucksmann_8163872.html` | France Télévisions player; franceinfo YouTube copy UNVERIFIED | `tolerated` | No | Also BFMTV/RMC "Face à Face", Apolline de Malherbe, 2026-09-04, `https://www.youtube.com/watch?v=YIw00fecnDU` |
| Jérôme Guedj | 2026-02-05 | France Inter | Declaration interview | Radio | UNVERIFIED | — | — | `tolerated` | — | Panel with Aurore Bergé at Sens, 2026-08-29 (Laboratoire de la République). **Gap** since |
| Emmanuel Maurel | none | — | Declared 2026-09-04 | — | — | — | — | — | — | **Gap** |
| Ségolène Royal | 2026-09-02 | BFMTV / RMC | "Face-à-Face", Apolline de Malherbe | TV + radio | about 30 min (format) | bfmtv.com | BFMTV YouTube copy UNVERIFIED | `tolerated` | RMC+ | Also "Les 4 Vérités", Télématin, France 2, 2026-08-31 (short) |
| Fabien Verdier | 2026-09-02 | Libération (print) | Declaration interview | Print | — | — | — | — | — | No TV/radio. **Gap** |
| Lydie Massard | 2026-04-22 | Bretagne 5 (regional radio) | Matinale, Stéphane Hamon | Radio | UNVERIFIED | `bretagne5.fr/podcasts/...`; `https://www.youtube.com/watch?v=NiOJR9zlYR4` | — | Bretagne 5 not inventoried | — | Also Clara Egger's series #3 |
| François Ruffin | 2026-09-02 | Libération × BFM2 | Debate with Villepin (D4) | Stream + TV | about 1 h 30 | see D4 | see D4 | `tolerated (to check)` | — | No solo long interview found since 27 Aug |
| Marine Tondelier | 2026-08-22 | LCI | Rentrée interview, Darius Rochebin, from the Écologistes' Journées d'été (Grenoble) | TV | 26 min 57 s | LCI copy UNVERIFIED; party copy Les Écologistes `https://www.youtube.com/watch?v=pqJ8J3oJm1A` (published 2026-08-22, embeddable) | Download: LCI copy if found, else the party copy | `tolerated` (Source is LCI even when the copy sits on the party channel) | No | Also "8h30 franceinfo", 2026-09-02, 23 min 26 s, Agathe Lambret and Paul Larrouturou, `https://www.franceinfo.fr/replay-radio/8h30-fauvelle-dely/le-8h30-franceinfo-de-marine-tondelier_8144867.html` |

## 5. Open points for the map

1. **Who is a Candidate for the seed.** Two of the seven MEDEF debaters (Glucksmann, Tondelier) and the whole Libé debate involve primary contenders; the Sens debate pairs a Candidate with an undeclared ex-president. The invariant "balanced coverage across candidates" needs a rule: election-declared only, or declared plus primary contenders, and whether two-person encounters count as "multi-candidate debates". This catalogue flags rather than decides.
2. **Coverage is thin and skewed.** Since 27 Aug only Attal, Lisnard, Glucksmann, Royal, Bouamrane, Tondelier, Philippe and Retailleau have a dated long TV/radio interview; Le Pen and Mélenchon have none since early July and May respectively; 17 of 32 people have no 2026 TV/radio interview found at all. "One recent long interview per declared candidate" cannot be filled from the broadcasters for the small candidates, and the balance audit will show it.
3. **Replays not located**: the Utiles debate (D2), Philippe's 30 Aug BFMTV interview, Retailleau's 26 Aug BFMTV interview in full, Bouamrane's 2 Sept BFMTV slot, Royal's Face-à-Face. BFMTV usually uploads full interviews to YouTube within a day; these should be re-checked from the Mac with `yt-dlp` search, which was not possible from the session (YouTube blocked anonymous metadata calls).
4. **Sources not yet in `source-terms.md`**: Libération (D4), Sud Radio, Bretagne 5, Solution démocratique's video series, MEDEF's own channel as an organiser copy.
5. **Refresh.** This is a snapshot; the socialist-primary debates of 16 Sept, 29 Sept and 6 Oct and the united-left primary will add multi-candidate Appearances within weeks.

## 6. Sources consulted (all read 2026-09-05)

- fr.wikipedia.org: Candidatures à l'élection présidentielle française de 2027; Élection présidentielle française de 2027; Primaire présidentielle socialiste française de 2026; Primaire de la gauche unitaire de 2026
- en.wikipedia.org: 2027 French presidential election; 2026 United Left primary
- lcp.fr: "Présidentielle 2027: la liste des candidats déjà en lice et des prétendants" (updated 2026-09-04); "ce qu'il faut retenir du débat entre les candidats devant le Medef"; "Primaire sociale-démocrate: pourquoi Raphaël Glucksmann et les autres candidats s'opposent sur les débats télévisés" (2026-09-02); "2027: figure de la droite, Xavier Bertrand confirme qu'il sera candidat"; "à Sens, la nécessité d'une union des démocrates"
- franceinfo.fr: REPLAY article of the MEDEF debate; Attal at the "20 Heures" of France 2 (2026-09-01); Ruffin–Villepin convergences (2026-09-02); Mélenchon and the veil (2026-09-02); Cazeneuve–Hollande colloquium of 4 Sept; Tondelier "8h30 franceinfo" (2026-09-02); Batho "8h30 franceinfo" (2026-06-07); Franc-jeu replay index; JT de 20h du 1er septembre 2026
- france24.com: "Premier débat de la présidentielle 2027 : les principales propositions" (2026-08-27)
- sudradio.fr: "Présidentielle 2027 : le point sur toutes les candidatures" (2026-08-24); souverainiste primary items (Sept 2025)
- parlons-politique.fr: "Rentrée politique 2026 : les dates clés"; "À Paris, Hollande, Cazeneuve, Philippe et Bertrand testent déjà leur capacité à rassembler"
- lelaboratoiredelarepublique.fr: "Université d'été de Sens 2026 : revivez les débats"; stephanelarue.com "LCI : deux grands rendez-vous politiques les 27 et 29 août"; programmetele.com listing of the Hollande–Philippe debate
- eventbrite.fr: "Libé 2027 Débat entre François Ruffin et Dominique de Villepin" (2 Sept, 18:30–20:30, Académie du Climat)
- coulisses-tv.fr: Glucksmann at the 20h of TF1 (2026-08-23); Faure at the 20h of TF1 (2026-08-30); Le Pen at the 20h of TF1 (2026-07-07); Franc-jeu of 2026-09-06
- tv-programme.com and leblogtvnews.com: "France 2027" rubric of the France 2 JT; "Franc-jeu" launch
- cnews.fr and europe1.fr: La Grande Interview, David Lisnard (2026-09-03); La grande interview, Karim Bouamrane (2026-06-29)
- melenchon.fr: entries of 22, 23, 27 Aug and 2 Sept 2026
- YouTube metadata (read directly where the page answered): `rpURHoN54bQ` (LCI, 3 h 04 min 15 s, embed disabled), `z0gJwsrODEw` (MEDEF, 3 h 12 min 34 s, embeddable, published 2026-09-01), `pqJ8J3oJm1A` (Les Écologistes, 26 min 57 s, 2026-08-22), `chF4leeEITk` (CNEWS, 20 min 46 s, 2026-06-28), `cNXiMekCD50` (BFMTV, 2024-07-03, not used), oEmbed titles for `D7vTQp2iM00`, `sp-2F_cTTxA`, `C6XkrrKR5OA`, `kKO15Fugb0w`, `yoL9CeJC54s`, `I73AOEJVU1Y`, `8_qNhqsCk7I`, `ESHmQJtoEtE`
- Repo: `docs/research/source-terms.md`, `docs/research/prior-art.md`, `docs/adr/0003-media-acquisition-from-opted-out-sources.md`
