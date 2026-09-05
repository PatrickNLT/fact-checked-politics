# Pre-launch checklist

The site is built privately and goes public when Patrick decides (map decision, Transcript publication posture, September 2026). There is no launch criterion; this list is what must be true on the day, and it grows as the platform develops. Each item names the decision or ticket it comes from. Tick items only when they are verified on the live build, not when the code exists.

## Repository and hosting

- [ ] The repository is private until launch day, and flipped to public as the last step (posture Q14; the proxy cannot change repository settings, so this is a manual step in GitHub Settings).
- [ ] The site builds from `main` on Cloudflare Pages and the production URL is the chosen domain (Name and domain ticket).
- [ ] Every replay embed has passed its per-Appearance check (oEmbed or Dailymotion API answer, TDM signals read, CGU version, replay expiry date), recorded in the Appearance's metadata (Source terms inventory).
- [ ] Every Appearance records its Acquisition basis and provenance record (fetch date, method, media hash, deletion date), and no working copy of any media remains on the Mac or anywhere else (ADR 0003).

## Content

- [ ] Every published Transcript has speaker attribution verified on every Segment; text may still be draft (posture Q5).
- [ ] Every Segment shows its validation status, and draft text is labelled as machine-produced (invariant 6, AI Act art. 50).
- [ ] Every page carries Source, programme, date, timestamp, speaker and journalist attribution (legal research, risk posture item 5).
- [ ] Journalists' questions and third-party voices are transcribed verbatim and attributed (posture Q3).
- [ ] Coverage is balanced across declared candidates: the seed corpus (every multi-candidate debate since 27 August 2026 plus one long interview per declared candidate) is complete, and no candidate is treated differently in display or depth (invariant 1).
- [ ] No media file is hosted or mirrored anywhere in the repository or the build; replays are embedded from the Source's own upload or deep-linked with a timestamp (invariant 4).
- [ ] Transcripts whose replay has disappeared show "replay no longer available at the Source" with the timestamps kept (posture Q6).

## Legal pages (Legal notice and publication mitigations ticket)

- [ ] Mentions légales: Patrick as directeur de la publication, the host's identity and address, a contact e-mail, a statement that the site is non-commercial and unaffiliated with any candidate or party.
- [ ] "Signaler un contenu" page: copyright, defamation and personal-data notices, stated response time, public log of notices handled.
- [ ] Right-of-reply channel honouring the three-day insertion rule.
- [ ] Corrections policy and public corrections log; every Transcript version dated.
- [ ] Method page: how Appearances are selected, how transcription and verification work, what the validation statuses mean, how the freeze works, and the statement that the archive is frozen after the result but stays online and correctable (posture Q4, Q10).
- [ ] The method page states how media are obtained (official replay downloaded, transcribed locally, deleted, nothing hosted), and that some Sources oppose text-and-data mining and the site does not rely on the exception for them (ADR 0003).
- [ ] The "Signaler un contenu" page covers a Source's request to stop transcribing its programmes: honoured for future imports, Appearance stays listed with its deep link, notice logged (ADR 0003).
- [ ] Licence notice: Licence Ouverte 2.0 (or the licence finally chosen) on metadata, timestamps, segmentation, attributions and editorial text; verbatim words remain their speakers' rights, reproduced under the CPI exceptions with attribution, no licence granted (posture Q7).
- [ ] Short data-protection note (only candidates' public statements are processed; contributors' data; consent-exempt analytics or none).

## Electoral calendar

- [ ] A mechanism freezes active distribution from the eve of each round at 0h and is tested before the first round (invariant 5, L.49).
- [ ] Nothing on the site reads as a call to vote for or against a candidate; no coordination with any campaign.

## Community

- [ ] Contributor guide: how to correct a Segment by pull request, who reviews, what "verified" requires (Community correction workflow ticket).

## Optional before launch, decided later

- [ ] Letters to campaigns (informational or licence) and to DILA and the SIG: deliberately not sent before the site has proved its value (posture Q2, Q13).
- [ ] Civil-liability insurance naming defamation and IP; association loi 1901 (planned before v3).
