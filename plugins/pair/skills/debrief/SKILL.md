---
name: debrief
description: Closes a working session so that what it taught is kept - what the user now understands and where they stumbled, what the project should remember (a trap, a term, a check worth automating), the shortcuts and loose ends the work left, and where the next session starts. Proposes, and changes nothing without a yes. Use at the end of a pairing or explaining session, after a bug is fixed, or when the user wants to take stock. Even when casual - "on fait le point", "debrief", "qu'est-ce qu'on a appris", "on ferme la session", "qu'est-ce qu'il reste", "wrap up", "what did we learn". Reviewing the code of the branch belongs to review-standards; improving the agent's own setup in depth to a retro skill when one is installed.
compatibility: Works in Claude Code and Codex. Needs git. Reads the learner notes of the explain and pair skills, the plan file of pair when there is one, and the project profile (.agents/project.json) when it exists.
allowed-tools: Bash(git log *), Bash(git diff *), Bash(git status *), Bash(git grep *)
---

# debrief

Take stock of the session with the user: what they learned, what the project should remember, what the work left open, and where to pick up. The output is one short message of proposals; the user picks, and only what they pick is written.

A session ends with knowledge in two places that vanish: the conversation, and the user's head. This skill moves what matters into the three places the next session reads: the user's learner notes, the project's own files, and the plan.

## 1. Gather

Read what the session left, not your memory of it:

- The commits and the uncommitted diff of the branch (`git log <base>..HEAD --oneline`, `git status --short`).
- The plan file when `pair` wrote one: the steps ticked, the stops, the unplanned stops, who wrote what.
- The learner notes (`~/.agents/learner/<project>.md`), and what the « redis-le-moi » prompts and the reviews of the user's code showed in this session.
- The `shortcut:` comments the branch adds: `git grep -nE '(#|//|/[*]|--) ?shortcut:'` on the changed files.
- The questions kept on the way, and anything set aside.

Done when each of the four sections below has its facts, or is known to be empty.

## 2. Say it, in four short sections

Skip a section that is empty. Facts that were observed, never a judgement of the person.

<debrief_template>
**Ce que tu tiens maintenant**
- <a zone or a point, with the evidence: said back right, wrote it, found the bug>

**Où ça a accroché**
- <a gap that was corrected, or a point re-pitched after « attends, quoi ? », with its `file:line`> · <seen before? how many times>

**Ce que le projet devrait retenir**
1. <a proposal, with where it would go> — <why: what it cost this session>

**Ce qui reste**
- <a `shortcut:` limit with its `file:line` and when to revisit it>
- <a question still open, and who can answer it>
- <what was not checked, and the risk>

Prochaine session : <one line: where to start, and from which file>
</debrief_template>

**What the project should remember** is the part that pays next time. Sort each thing the session tripped on before proposing where it goes:

- **A rule a tool can check** (a format, an import that must not exist, a test that must run): propose the check itself, a lint rule, a test or a CI step. A check that already exists but is not wired, or is broken, is the finding. A written rule comes second: it is read once and then forgotten.
- **A judgement call** the team keeps making the same way: one line in the repo's standards file (`CODING_STANDARDS.md`, or the file the repo already has), where a review reads it.
- **Something that took long to find** (where a thing lives, which command runs it): one pointer line in the repo's instructions file (`CLAUDE.md` or `AGENTS.md`). That file is loaded into every session: it holds pointers, not explanations.
- **A term** the session had to define: the glossary (the profile's `glossary`, or a root `GLOSSARY.md`), one or two sentences on what the thing is, once the user has used it rightly.
- **A trap** that cost time and that the code cannot show: the profile's `traps`, one sentence.
- **An instruction that changed nothing** (it was there and the mistake happened anyway): propose deleting or sharpening it, not adding a second one.

Number the proposals, so the user can answer « 1 et 3 ». Three or four at most: the ones that would have saved the most time today.

## 3. Write what the user picked ⛔

Gate: the user says which proposals to apply. Then:

- **The learner notes** are yours to update without asking, in their format (the `explain` skill's references/learner.md): the zones with their level and today's date, the gaps new or seen again, the preferences. Say in one line what you changed.
- **Everything in the repo** is written only on a yes, as an uncommitted change the user can read: a line in a standards or instructions file, a glossary entry, a check. A proposal for the team's profile (`.agents/project.json`) is shown as the exact line to add.
- **The plan file** gets the open items and the next-session line, so a later `pair` resumes from it.

Done when the notes are updated, each picked proposal is on disk, and the user has the one line that says where the next session starts.

## Handing over to someone else

Only when the work moves to another person or another agent session: write a short note that points at what already exists (the plan, the commits, the ticket) instead of copying it, leaves out every secret and personal detail, and marks apart what was verified from what is only assumed, since the reader will take each sentence as a fact. Put it where the user says; a note in transit does not belong in the repo.
