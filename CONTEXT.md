# fact-checked-politics

A public, non-partisan reference of what French politicians said, when and in what context, built around verbatim timestamped transcripts of their public appearances during the 2027 presidential campaign. Later layers classify what was said by theme, check factual claims, and tag rhetorical techniques.

## Language

English terms are canonical in code and docs; the French label shown on the site follows in parentheses.

### People and events

**Speaker** (intervenant):
Any person who talks in an imported appearance, candidate or not. Only declared candidates get a public profile page in v1.
_Avoid_: politician, candidate (as the general term), personality

**Candidate** (candidat):
A Speaker who has publicly declared a run for the 2027 presidential election. A role of a Speaker, not a separate entity.

**Appearance** (intervention):
One debate, interview, speech or other public occasion where one or more Speakers talk, with a source, a date and a medium. The unit of import.
_Avoid_: debate, interview, discourse, event, video (as the umbrella term)

**Source** (source):
The broadcaster, publisher or organiser that produced the recording of an Appearance, and the official replay it links to. The site links to or embeds the Source's replay; it never hosts the recording.

### What was said

**Transcript** (transcription):
The verbatim, timestamped, speaker-attributed text of one Appearance. Produced by automatic speech recognition and corrected by the community through versioned edits.

**Segment** (extrait):
A timestamped stretch of one Speaker's speech within an Appearance. The unit that everything else (Statement, Technique, Topic) attaches to.
_Avoid_: quote, passage, clip, utterance

**Statement** (affirmation):
A checkable factual claim extracted from a Segment. Introduced in the fact-checking layer (v3).
_Avoid_: claim, fact, assertion

**Technique** (procédé):
A logical fallacy or discourse move tagged on a Segment, drawn from the reasoning guide's catalog. Introduced in the rhetoric layer (v4).
_Avoid_: fallacy (as the umbrella term), manipulation, trick

### Classification

**Theme** (thème):
One of a small fixed set of broad campaign areas (health, environment, education, foreign policy, ...). Introduced in the positioning layer (v2).
_Avoid_: category, domain, area

**Topic** (sujet):
A specific question within a Theme on which candidates take positions (for example, the retirement age within the Theme of pensions). A Segment is tagged with Topics; Topics roll up to one Theme.
_Avoid_: issue, subject, question
