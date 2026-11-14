---
name: pr
description: Writes the title and description of a pull request in the team's format - Summary, Changes, Notes on top for the reviewer, then the repo's own PR template filled in - with no AI attribution line, and answers the review threads on your own PR with a fix or a short reply. Reads the project profile (.agents/project.json) for the title pattern, reviewers and reply voice. Use when opening a PR with gh pr create, rewriting or filling a PR body, when another skill adds a section to one, or when teammates commented on your PR. Even when casual - "ouvre la PR", "écris la description de la PR", "remplis le template de PR", "update le body de la PR", "réponds aux commentaires de ma PR", "address the review".
compatibility: Works in Claude Code and Codex. Needs git, gh and python3 (python on Windows).
allowed-tools: Bash(git diff *), Bash(git log *), Bash(gh pr view *), Bash(gh api repos/*/pulls/*/comments*)
---

# pr

Write the PR title and body in the format below, then answer review threads on your own PR.

A PR description has two parts. The **top** (Summary, Changes, Notes) is written for the reviewer: what the PR does and what to know before reading the diff. The **bottom** is the repo's own template, filled in, so the checkboxes and links the team expects are there.

## Steps

1. **Gather the facts.** Read the diff against the base (`git diff <base>...HEAD`, `git log <base>..HEAD`), the ticket key from the branch or commits, and the repo's template (`.github/PULL_REQUEST_TEMPLATE.md`, `.github/pull_request_template.md`, `docs/pull_request_template.md`, or `.gitlab/merge_request_templates/`). For each feature flag the diff newly reads, check that the flag exists in the flag service before any reviewer sees it, and say in Notes where it is on.
2. **Review the diff before a reviewer does.** List the comments the branch adds with `python3 scripts/comment-check <base>` (in this skill's folder; `python` where `python3` is the Windows Store stub) and keep only a non-obvious why or a trap. Then run the agent's own review on the branch (Claude Code: `/simplify`, then `/code-review`; Codex: `/review` against the base branch; any other agent: the `pr-review` skill's Triage applied to your own diff), and fix or skip each finding. Re-run the repo's lint and tests after the fixes (the profile's `commands`, or the repo's scripts). Done when every finding is fixed or has a stated reason to skip, and the checks are green.
3. **See a UI change on screen first.** When the diff changes what a screen shows, run the branch and look at every state the diff touches: shown and hidden, edit and view mode, each customer type or setting it gates on. Capture them with the `pr-screenshots` skill (its capture step) before `gh pr create`, and upload them once the PR exists. Done when each state has a capture that matches what the PR claims.
4. **Write the title** with the profile's `pr.title` pattern, else conventional-commit form with the ticket key as scope: `feat(PROJ-123): emit date format for date fields`. Max 72 characters.
5. **Write the body** in the template below, into a temp file, and pass it with `--body-file`.
6. **Check it**: `gh pr view <n> --json title,body` shows the body as written, with no attribution line, and every identifier in backticks in the body (keys, fields, functions, flags) appears in `git diff <base>...HEAD` spelled the same way. Deploy and data-update steps are where a stale name hurts most: a configuration key spelled differently from the code is written but never read.

## Template

The top three sections, then the repo's template:

<pr_body_top>
## Summary
<one or two sentences: what the PR does and why, in plain words>

## Changes
- <one bullet per change a reviewer will see in the diff>

## Notes
- <what a reviewer would otherwise ask about: drift picked up, no runtime change, follow-ups, stacked PRs>
</pr_body_top>

- When the repo's template has its own "Description" or "Describe your changes" section, these three take its place and the rest of the template stays as it is.
- When the repo has no template, the body is these three sections and a link to the ticket.
- Fill the template's ticket link with the tracker's URL for the key, tick only the boxes that apply, and leave the author's own checklist for the author unless the user asks you to tick it.

<sample_input>Branch feat/PROJ-137/date-format; diff maps the Date type to "format": "date" in the schema generator, adds TestDateFormat, regenerates 14 schemas; unit tests run.</sample_input>

<ideal_output>
## Summary
Emit `"format": "date"` for `Date` fields in the generated JSON Schemas, so the rules editor can offer them as date fields.

## Changes
- Map `Date` to `"format": "date"` in the schema generator
- Add `TestDateFormat`
- Regenerate the 14 JSON Schemas

…then the repo's template, with the ticket link filled, New feature and Unit tests ticked…
</ideal_output>

Why ideal: regenerated files as one bullet, Notes dropped because nothing would surprise a reviewer.

## Filling it in

- **Summary**: one or two sentences, no preamble. Say the effect, then the reason.
- **Changes**: short imperative bullets ("Map ...", "Add `TestX`", "Regenerate ..."), code identifiers in backticks. Mention regenerated files as one bullet, not file by file.
- **Notes**: only what would surprise a reviewer. Drop the section if there is nothing.
- **Testing**: tick only what was actually run; never tick a box for a test that was not run.
- The language of the repo's existing PRs (usually English).

## Answering review on your PR

- Read the human threads, one PR at a time and in parallel: `gh api repos/<owner>/<repo>/pulls/<n>/comments` for the line threads and `gh pr view <n> --repo <owner>/<repo> --json reviews,comments` for the review summaries and the conversation. Skip bot comments.
- Each thread gets a fix on the branch or a reply. Replies use the profile's `pr.reply_voice` (default: short, plain, the author's own voice).
- Show the replies and the push before posting either.
- Post a reply only on the user's word: `gh api -X POST repos/<owner>/<repo>/pulls/<n>/comments/<id>/replies -f body=...`, `<id>` being the thread's first comment.

## Rules

- No AI attribution anywhere in the body: no "Generated with" line, no "generated by", no mention of the AI agent. The agent is already a co-author on the commits when the team keeps that line.
- When another skill adds a section (screenshots, "Tested locally"), insert it before the template's first checklist section and never replace what is already there.
- Adding reviewers: map the names the user says through the profile's `pr.reviewers`; ask for a login you do not have rather than guess. Then move the ticket to the profile's review status when it has one.
