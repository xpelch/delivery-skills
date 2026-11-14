---
name: delivery
description: Carries one ticket from start to done (In QA or the project's equivalent) and closes it, with the user in the loop - situate, understand (the code walked in the editor, a page on request), decide (grilling, then spec and decisions written once), work overview, pair implementation with validation at every step, review and PR, deliver - each phase delegated to the skill that owns it, with a gate wherever a decision is the user's or work leaves the laptop. Works on any project through its profile (.agents/project.json). Run only on an explicit invocation (/delivery, or /delivery:delivery from the plugin), to start, resume or close a ticket, when QA sends one back, or to ask where a ticket stands. Explaining a ticket alone belongs to explain; writing, reformatting or cutting a ticket into sub-tasks to ticket.
compatibility: Works in Claude Code and Codex. Needs git and gh; the tracker's MCP for Jira or Linear; optionally an editor CLI (code, cursor). Needs the pair plugin (the explain, pair, review-standards and debrief skills), which installs with this one; uses this plugin's project-setup, ticket, pr, announce and pr-screenshots skills, and a grilling and a TDD skill when installed (for example mattpocock-skills).
disable-model-invocation: true
allowed-tools: Bash(gh pr list *), Bash(gh pr view *), Bash(gh issue view *), Bash(code -g *), Bash(code --add *), Bash(code --remove *)
---

# delivery

Move one ticket through the phases below with the user, stopping at every ⛔ gate for their go.

The user works beside you in their editor and stays in the loop: they know where the ticket stands before any code, they see each piece of code as it lands, and every decision is theirs. A thin conductor: it knows the order of the phases and their gates, and nothing else. Each phase's how-to lives in the skill it names; read that skill when the phase starts.

What differs from one project to another (tracker, statuses, commands, editor, merge rules, release) comes from the project profile: read `.agents/project.json` (or `.claude/project.json`; fields in references/profile.md) before the first phase. No profile: offer the `project-setup` skill first, or discover what you can, ask once for the rest, and offer to save it.

A **gate** (⛔) is a stop: say what is about to happen, then wait for the user's go before crossing it. Gates sit where a decision is the user's, and where work leaves the laptop (the tracker, GitHub, the team chat, a shared environment).

What you write to the user follows the profile's `language`; the labels and samples below are the French ones.

## State

The ticket's notes file carries a `**Phase:**` line naming the last phase completed, next to the usual facts (worktrees, branches, PRs, decisions, the plan file). It lives in the agent's project memory when it has one (Claude Code: a file per ticket, `project-<key>-<slug>.md`, next to `MEMORY.md`), else in the profile's `notes` folder (default `.agents/notes/<key>.md` under the repos root), which is how Codex keeps it. A split ticket's line stays at `split` until the parent reaches Deliver, and the file lists each sub-task with its blockers and its own `Phase`.

## Resume

When the ticket was started before:

1. Read its notes file, and the plan file when it has one.
2. Check the real state: `gh pr list --search <KEY> --state all --json number,title,state,isDraft,headRepository,reviewDecision,createdAt` per repo the notes name, the ticket's status in the tracker (the status field only: a default view returns the whole description), and `git -C <worktree> status --short` per worktree. For a split ticket, the parent's children in one query, and one `gh pr list --search "<KEY-1> OR <KEY-2>…"` per repo.
3. Where the notes and reality disagree, reality wins: fix the notes, then say in one line which phase comes next and why: `Phase <notes> → réelle <observed>; prochaine : <phase> parce que <reason>.` Re-add the worktrees to the editor's workspace (`<editor> --add`) when the window lost them. A ticket QA sends back reopens at Pair implementation, its comment as added spec; `pair` resumes from the plan file.

## Phases

1. **Situate** ⛔
   - Read the ticket and every comment, its parent and its siblings, each summary and description. Later phases need only a status or a summary from the tracker: ask for those fields, never the full issue again.
   - Look at the code just enough to place it: a search and `git -C <repo> show origin/<default branch>:<path>` after a fetch, no subagent.
   - Answer in the chat, no page: a table of the repos with three columns: the repo's role as `<layer> - <a few words>` (e.g. `backend - évalue les règles`), what this ticket changes there, and where in the code: the function or file the change lands in, what it does today in a few words, and its link on the default branch (e.g. [`buildPayload`](…/payload.go#L39) - construit le JSON envoyé à l'évaluation); **what the code contradicts in the ticket** (a ticket says a field "already exists in the app" when it exists only in the browser, never in the backend); the siblings, and each acceptance criterion that restates a sibling's behaviour, named with its key, as context built there. Building what a sibling owns ends in pull requests closed as another story's work.
   - Gate: the scope (this ticket, these repos). Then assign the ticket to the user and move it to the profile's start status.
   - Create the notes file with `**Phase:** situate` and a `## Scope` section: the repos in, the acceptance criteria left to siblings.

2. **Understand**: the `explain` skill, walk only: the investigation, then the TLDR, traps and open questions in the chat, then the walk and its « redis-le-moi ». The page is built only when the user asks for it: the Situate table and the walk already carry the understanding.
   - First create one worktree per repo of `## Scope`, on a branch named by the profile's `branch` pattern, cut from the default branch on origin: `git -C <repo> worktree add -b <branch> <worktree> origin/<default branch>` (the profile's `worktree` pattern, default `../<repo>-<key>`), then `<editor> --add <worktree>`. Each worktree is added for the ticket's life and removed at Deliver. The walk opens files from these worktrees, so the explorer follows them and the line numbers are the default branch's.
   - When the ticket changes something a user sees, show the current behaviour live first: the Pre-QA *before* step of Pair implementation.
   - No gate: the walk opens every station's file at once, in trip order, with one message of one line per station; the user reads at their pace, asks about any station, and answers the « redis-le-moi » or skips it. Done when explain is done and `## Compréhension` is in the notes.
   - No repo file is edited before Pair implementation.

3. **Decide** ⛔: a grilling skill when installed (such as `grilling`, or `mattpocock-skills:grilling`), otherwise one question at a time, each with your recommendation; within `## Scope`, and a choice a sibling owns is left to it.
   - The grilling covers Understand's open questions and the spec's gaps together: what Situate and Understand found that the ticket misses, the missing acceptance criteria, the failure paths and the no-regression.
   - Facts are looked up, not asked: a question that needs one gets the lookup first. One lookup (can a rule compare two fields at all?) can decide a whole branch of the design.
   - Contract check, before the gate, on each decision that changes an endpoint's response or a read path: name every consumer (`gh search code --owner <org>`), show the change is additive for each, and keep a read safe, writing nothing. A first draft of decisions that has a GET insert rows, or drops a field a consumer reads, is caught here.
   - Then draft, once, the final description and the decisions comment (`ticket`): the need as the code shows it, the scope, the acceptance criteria including failure paths and no-regression, and one row per decision.
   - Gate: the shared understanding, on that one draft. On the user's go, write both to the tracker. The reporter owns the ticket and is notified.
   - **Split**, when the work holds more than one slice that can merge and reach QA alone, or one PR per repo would be too big to review: cut the slices with `ticket` (Sub-tasks), iterate the list with the user, then, on a go, create them and record their keys and blockers in the notes. Each sub-task then runs phases 4 to 6 with its own key; the parent reaches its done status after its last one. Skip it, and say so, when one slice is the answer.

4. **Work overview** ⛔: the `pair` skill, its Work overview: before any code, the whole job in one message.
   - Hand it the ticket: the `## Scope`, the decisions comment and the worktrees. The steps are grouped by PR and repo, each naming the decision that lands in it, with the merge order.
   - The plan is `PLAN-<KEY>.md`, one per ticket however many repos it spans; record its path in the notes file.
   - Gate: the user agrees on the steps, their order and the stops.

5. **Pair implementation** ⛔ at the plan's stops: the `pair` skill, its Steps then its Pre-QA, in the ticket's worktrees.
   - Branches and commits follow the profile's `branch` and `commit` patterns; a stop step's « Pourquoi » names the decision or the acceptance criterion from the ticket.
   - Pre-QA runs before the change goes to QA: the ids of its test data go in the notes file's `## Local QA`, and its gate is that the user has seen every acceptance criterion this ticket owns.
   - Questions that do not block a step wait for Review.
   - Done when every acceptance criterion this ticket owns has a test and every plan step is ticked.

6. **Review and PR** ⛔
   - **Markers first**: `rg -n '(GATE|TODO)\(<owner>\)' -g '!*.md'` in every worktree must come back empty. Resolve each one left with the user; the `pair-marker-check` hook also refuses a push or `gh pr create` whose branch adds one.
   - List the comments each branch adds with the `pr` skill's `scripts/comment-check <base>`, and keep only a non-obvious why or a trap.
   - Run the agent's own review on each branch, and fix or skip each finding with a reason. Claude Code: `/simplify`, then the `review-standards` skill (standards and spec, fresh context; spec = the ticket and its decisions comment), and `/code-review` too on a branch whose diff holds logic. Codex: `/review` against the base branch, then `review-standards`.
   - A branch that needs another repo's unmerged branch says so in its PR and pins it the way the language allows; the pin is removed once that PR is released, before this one merges.
   - Gate, one for the whole PR package: the questions kept for Review, the review findings fixed or skipped, the PR titles and bodies (`pr`, captures with `pr-screenshots` for a UI change), the reviewers, and the announcement with the merge order (`announce`). On the user's go, open the PRs, add the reviewers (`pr.reviewers` maps names to logins), move the ticket to the profile's review status, fill the decisions comment's `## Pull requests`, and leave the announcement as a draft, never sent.
   - Address review: answer the teammates' threads with `pr` (Answering review), a fix on the branch or a reply; a round's fixes go through this phase's checks on their own diff, and through Pre-QA first when they change what a user sees. Gate: the replies and the push. A PR with no `reviewDecision` a working day after `createdAt`: offer a nudge as a reply to the announcement. Done when every PR is approved and every human thread has an answer.

7. **Deliver** ⛔: the profile's `deliver` rules, then close.
   - Before the first merge, every item of the decisions comment's `## Rollout` and of the profile's `deliver.rollout` exists; one someone else owns is left aside and said. A shared environment the merge needs is free (`deliver.notes`).
   - A PR pinned to another repo's branch waits for that PR's release, then drops the pin before it merges.
   - Gate, one for the whole sequence: the merge order, every PR approved with green checks, the rollout items ready, never on a day in `deliver.no_merge_days`. Then merge in that order with the profile's `deliver.merge` method, and stop only when something fails (CI, merge queue, conflict).
   - After the merges, run the profile's `deliver.release` when it has one, then move the ticket to the profile's done status.
   - Close: list what the ticket left behind (pinned or local branch images and a backed-up compose override, the test data in `## Local QA`, a shared environment taken only for testing, the worktrees and the plan file), and turn the notes' `## Left aside` into follow-up tickets or one comment (`ticket`).
   - Then the `debrief` skill: what the ticket taught the user, what the project should remember (a trap, a term, a check worth automating), and the `shortcut:` limits the work left.
   - Gate: the cleanup list and the follow-ups together. Then `<editor> --remove` each worktree, remove the merged worktrees, and trim the notes file to what a later reader needs: the PRs, where they run, the follow-ups.

`<editor>` is the profile's `editor` (default `code`; `cursor` and the other VS Code builds take the same flags). With no editor CLI, or `editor` set to `none`: give each `<path>:<line>` as a link in the chat and skip the workspace commands.

## Closing a phase

End every phase with one line in the chat:

<phase_close>
✔ <phase> · prochaine : <phase> (<what needs the user's go>)
</phase_close>

Anything left aside goes to the notes file's `## Left aside`; mention it in the chat only when there is some.

Then update `**Phase:**`.
