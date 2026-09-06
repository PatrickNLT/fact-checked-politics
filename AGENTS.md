# fact-checked-politics

## Project stage

The project is at the **prototype stage** (since 2026-09-06): the transcription pipeline (issue #13) is being built and measured on the seed corpus, no site is published yet. Rules that depend on the stage say so; today that is the deletion rule of ADR 0003, which is suspended for recordings downloaded for the prototype (see its 2026-09-06 amendment). Update this section when the stage changes.

## Agent skills

### Issue tracker

Issues live as GitHub issues in `PatrickNLT/fact-checked-politics`, managed with the `gh` CLI. See `docs/agents/issue-tracker.md`.

In a **cloud session** (Claude Code on the web), `gh` is installed but its GraphQL access is restricted: only `gh api repos/...` (REST) works; `gh issue`, `gh pr` and `gh auth status` fail with HTTP 403 or "token invalid". Use `gh api` REST calls or the GitHub MCP tools instead; see the "Cloud sessions" section of the tracker doc. In a local session everything works.

### Triage labels

The five canonical triage roles, each label string equal to its name (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`). See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: one `CONTEXT.md` and `docs/adr/` at the repo root. See `docs/agents/domain.md`.
