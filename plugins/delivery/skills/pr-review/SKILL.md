---
name: pr-review
description: Reviews a teammate's pull request and drafts, then posts, the review comments in the team's voice - soft, short, questions not prescriptions, behaviour and scope only - with every finding verified before it is kept. Reads the project profile (.agents/project.json, review) for the comment language, voice and the team's review taste. Use when reviewing someone else's PR, drafting or softening review comments on it, or posting or approving a review. Even when casual - "review cette PR", "peux-tu review ça", "check la PR de Sam", "rédige les commentaires", "rends-le plus soft", "poste et approve", "approve-la". Answering comments on your own PR belongs to pr.
compatibility: Works in Claude Code and Codex. Needs gh signed in and python3 (python on Windows); the tracker's access to read the ticket.
allowed-tools: Bash(gh pr view *), Bash(gh pr diff *), Bash(gh pr checks *), Bash(*/pr-review/scripts/pr-anchor *), Bash(python3 */pr-review/scripts/pr-anchor *)
---

# pr-review

Review a teammate's PR, report verified findings to the user in their language, and post approved comments only on the user's word.

A review here is two products: the findings, told to the user in chat (in the profile's `language`), and the comments posted on GitHub (in the profile's `review.comment_language`, default the language of the repo's existing PRs). The team's voice and taste come from the profile's `review` block (fields in the `delivery` skill's `references/profile.md`); the defaults below hold when it is missing.

## Steps

1. **Read the PR.** `gh pr view <n> --repo <owner/repo> --json title,body,baseRefName,headRefName,files,reviews`, then `gh pr checks <n> --repo <owner/repo>`: a red check is a finding, so trace it to the hunk that causes it. Read the diff with the profile's `pr_diff` command when it has one, `gh pr diff <n> --repo <owner/repo>` otherwise. Generated files, lockfiles and vendored code are skimmed by name only; open one only when it matters to a finding, and only that file.
2. **Read the spec.** The ticket key is in the PR title, branch or body. Fetch the ticket and its comments from the tracker (profile `tracker`), where the team records the decisions taken after the ticket was written. The acceptance criteria and those decisions are the spec; the PR body's Notes say what the author already explained.
3. **Review**, yourself or through a review the agent has (Claude Code: `/code-review` on the PR; Codex: `/review` with custom instructions naming the PR's branch). Every finding is **verified** before it is kept: reproduce it against the branch, check the base branch and CI, and confirm it can actually happen with today's data.
4. **Report the findings** to the user, worst first, with what you verified.
5. **Draft the comments** when asked. The default review is an approve with one general comment carrying the worst kept finding; draft more, one per kept finding (see Triage), only when the user asks for inline comments or a finding blocks the merge. Write them in the Voice below, each inline one labelled with where it lands: run `python3 scripts/pr-anchor <owner/repo> <n> <path> <line | L<line> | /regex/>` from this skill's folder (`python` where `python3` is the Windows Store stub). Show them in chat and wait; the user edits, softens or cuts.
6. **Post** only on the user's word. Re-run `scripts/pr-anchor` first: authors force-push, and a line that left the diff makes the whole review call fail. One review per PR, all its comments inline (see Posting). `event` is `COMMENT` unless the user said approve or request changes.

Done when each posted review's `html_url` is given to the user, or the user stopped at the drafts.

## Triage

Keep a comment when it is about:

- behaviour or a bug the diff introduces
- a red CI the diff causes
- scope: changes the ticket did not ask for, or drift the PR body does not mention (user-facing text changed without the ticket or its design asking for it is one of these)
- docs or names that would actively mislead the next reader
- a feature flag the diff newly reads that does not exist yet in the flag service, when the Notes don't say who creates it: the feature stays hidden everywhere until it exists
- an item of the profile's `review.taste` (what this team's reviewers consistently ask for)

Cut, even when true:

- commit title, branch name, PR title format
- naming, style, test structure, duplicated or redundant code comments, unless `review.taste` names them
- theoretical risks that today's data or callers cannot trigger
- asking whether the author tested something
- anything the PR body's Notes already explain

Mention the cut items to the user in one line each, so they can bring one back.

## Voice

The profile's `review.voice` when it has one. The default: lowercase, with commas, periods and question marks; one or two short sentences, each on its own line.

- Open light: "small thing, i noticed…", "i might be missing context, but…", "i think this one is why ci is red:".
- Assume good intent out loud: "probably all expected", "maybe it got regenerated from an older version?".
- Name one or two examples, never the full list, no line numbers, no code blocks.
- Ask for the smallest action that settles it: a line in the notes, a snapshot update, a rerun.

<approved_comment>
small thing, i noticed the regenerated fixtures drop the `refund-partial` and `refund-full` cases, which `refunds_test.go` reads from.
maybe they got regenerated from an older schema? might be worth a quick rerun from main.
</approved_comment>

<approved_comment>
i think this one is why ci is red: `totalWithTax` now shows up in the order response, and the snapshot doesn't have it yet.
probably just needs the snapshot updated, unless you'd rather keep that drift out of this pr?
</approved_comment>

The first finding, drafted wrong:

<draft_to_avoid>
Line 7692: you removed the refund fixtures. Please regenerate from main:
```
make fixtures
```
</draft_to_avoid>

The right version of this draft is the first approved comment above.

## Posting

Write the review to a temp JSON file. `side` and `line` come straight from `pr-anchor` (`LEFT` = a removed line, numbered in the base file):

```json
{
  "event": "COMMENT",
  "body": "",
  "comments": [
    { "path": "test/fixtures/refunds.yaml", "side": "LEFT", "line": 7692, "body": "small thing, i noticed…\nmaybe…?" }
  ]
}
```

```bash
gh api -X POST repos/<owner>/<repo>/pulls/<n>/reviews --input <file> --jq '{state,html_url}'
```

Give the user each review's `html_url`. A general comment with no line goes in `body`.
