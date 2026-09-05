---
status: accepted
---

# Static site with transcripts as versioned files in git

v1 is a searchable reference of verbatim, timestamped transcripts, corrected by the community. We decided to store transcripts and their metadata as files in the public GitHub repository, take corrections as pull requests, and build a static site from them (Astro on Cloudflare Pages with client-side search, mirroring the reasoning guide), rather than run a server with a database and in-site editing.

## Considered options

- **Server-rendered app with a database and accounts** from day one. Rejected for v1: it requires an auth system, a moderation queue and an edit history that git already provides, and it forces the "no data collected" invariant to be re-proven at every feature.
- **Static site plus a small database only for search.** Rejected: client-side search over a few hundred appearances is adequate, and the database would be the first piece of writable infrastructure with nothing yet needing writes.

## Consequences

- Every correction has an author, a diff and a review, which doubles as the neutrality audit trail.
- The data model must be expressible as files (Markdown or JSON per appearance) so that v2 to v4 annotations attach to segments without a migration.
- Layers that need reader writes (in-site suggestions, community tagging) will require a service later. That decision is deferred, not made.
- Nothing in this choice precludes a future real-time layer, which would be a separate system fed by the same segment identifiers.
