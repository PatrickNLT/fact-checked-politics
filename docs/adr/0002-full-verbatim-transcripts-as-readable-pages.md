---
status: accepted
---

# Full verbatim transcripts as readable pages, on the Vie-publique posture

A permanent verbatim transcript of a studio debate or broadcast interview is legally amber in France: the candidate's words are protected, the political-speech exception covers rally speeches while they are news, not studio debates or archives, and only tolerance covers the rest (see `docs/research/legal-france.md` sections 1, 2 and 9). The State itself has nevertheless published full verbatim broadcast interviews on Vie-publique.fr for twenty years, including every 2002 candidate, with no licence from broadcasters or speakers and no recorded challenge (`docs/research/vie-publique.md`). We decided to publish each Transcript as one continuous readable page, speaker-labelled, every Segment anchored and permalinkable, the Source's official replay embedded or deep-linked with timestamps, and to rely on the same mitigations as the State's practice rather than on consent: attribution of Source, programme, date, speaker and journalist on every page; a takedown channel with a stated response time; a public corrections log; media never hosted; machine-produced text labelled until verified. The transcript is published in full because the data files already live in the public repository, so any display that hides the full text is theatre.

## Considered options

- **Segments shown only when attached to a note**, full text searchable but never shown whole (the legal file's "transcripts as analysis, not corpus"). Rejected: v1 has no analysis to attach to, the repository publishes the full text anyway, and the reference value of "who said what, when" is the continuous page.
- **Consent letters to every campaign asking for a licence**, with segment-only display for refusers. Rejected: a written refusal converts tolerated publication into knowing infringement for that candidate, and a per-candidate fallback breaks the balanced-coverage invariant. No letters go out before the site has proved its value.

## Consequences

- Journalists' questions and third-party voices are transcribed verbatim and attributed; they are Speakers, not Candidates.
- Each Segment carries a Validation status on its text and on its speaker attribution; speaker attribution is verified on every Segment before a Transcript is public, the text may stay a labelled draft.
- A Transcript outlives its replay: when the Source removes it, the page says so and keeps the timestamps; no fallback to unofficial copies.
- After the second round no new Appearances are imported; the site stays online as an archive and corrections stay open.
- Licence Ouverte 2.0 covers everything Patrick authors (metadata, timestamps, segmentation, attributions, corrections, editorial text); the verbatim words remain their speakers' rights, reproduced under the exceptions of the Code de la propriété intellectuelle with attribution, no licence granted.
- The site is built privately (repository private) and goes public when Patrick decides; `docs/launch-checklist.md` lists what must be true on that day.
- How the pipeline obtains audio from broadcasters that have opted out of text-and-data mining is a separate decision (map ticket "Media acquisition under broadcasters' mining opt-outs").
