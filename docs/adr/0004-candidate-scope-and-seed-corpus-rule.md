---
status: accepted
---

# Candidate scope by reference list, and a seed corpus of Confrontations only

The seed catalogue (`data/catalogue/seed.md`) showed that "a Speaker who has publicly declared a run" does not settle who the site covers: two of the seven MEDEF debaters run in a primary rather than in the election, undeclared figures debate declared ones, and fourteen of the thirty-two people found have no broadcast interview at all, so the charting session's "one long interview per declared candidate" could not be met on launch day and would have forced an editorial pick per person. We decided that a Candidate is whoever LCP's candidates page or French Wikipedia's candidatures page lists as running for the election or in a primary for it (either list suffices, the list and read date are recorded, the Conseil constitutionnel's official list replaces both in March 2027), that primary contenders are Candidates with no distinction, and that the seed corpus is one mechanical class, every Confrontation since 27 August 2026, an Appearance where two or more Candidates speak in the same exchange, with no per-person quota. Non-partisanship then rests on a rule about a class of Appearances, which the method page can state and anyone can check, rather than on choices about people.

## Considered options

- **Election-declared people only**, primary contenders as plain Speakers. Rejected: it hides Glucksmann and Tondelier on the first debate of the effort and leaves the socialist-primary debates outside the seed, while Arcom's own election practice counts declared and presumed candidates alike.
- **A third role, Contender, between Speaker and Candidate**, with a primary label. Rejected as a distinction the site does not need: the label is a fact on the Candidate's page, not a class.
- **No listing threshold** (any dated, sourced declaration). Rejected: it makes the site the judge of who is a candidate, one secondary source at a time; a public reference list is checkable and, with two lists in "either" mode, errs toward inclusion.
- **Keeping the interview quota**, as a per-person floor with a pick rule, or as an exhaustive "every long interview" clause. Rejected for v1: the floor is unfillable and the pick is editorial; the exhaustive clause is mechanical but multiplies the volume for a solo transcriber. It is the natural first extension once pipeline throughput is known.
- **Judging eligibility on the Appearance's date** (was the person a Candidate that day). Rejected: the site is about what the people who ended up running said; roles as known today, with the declaration date shown on the profile, keep it honest.

## Consequences

- **Candidate is a dated role.** It starts on the reference listing and ends with a reason (withdrawal, primary lost, absent from the official list, dropped from the references). An ended role keeps its profile online, labelled with the end date; imports for that person stop; the balance audit lists ended runs in a closed group. Nothing is deleted when a primary is lost.
- **Putative figures have no role.** Their words in an imported Confrontation are Speaker Segments like a journalist's. When they become Candidates, their earlier Confrontations since 27 August enter the seed and show on the profile, labelled with the declaration date.
- **Two-person Confrontations count.** Bertrand–Cazeneuve (4 September 2026) is in the seed if a recording exists; Hollande–Philippe and Ruffin–Villepin enter the day Hollande or Villepin is listed.
- **The balance audit is a distribution, not a target.** The method page publishes, per Candidate, the number of Confrontations they took part in and their speaking time summed from Segments, and names the Candidates with none; the claim is "the whole class was imported", not "everyone got the same".
- **Solo interviews are not in v1.** The data model must still hold them (Appearance is unchanged); only the seed rule excludes them.
- Supersedes the seed sentence of the charting session (map issue #5, Notes) and the coverage line of `docs/launch-checklist.md`.
