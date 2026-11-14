---
name: explain
description: Explains a ticket, a code flow, a module, a file or a pull request until the user really understands it, before any implementation - what it is for, where it lives, the current flow traced in code with file:line, what changes, the traps and open questions, in the real terms of the code - then walks the stations in the editor and has the user say the key points back. Use whenever the user asks to explain, understand or trace code or a ticket, even casually - "explique-moi ce module", "explique-moi PROJ-123", "comment marche ce fichier", "c'est quoi le flow quand on soumet", "trace-moi ce qui se passe quand", "explique-moi cette PR", "je comprends pas ce code", "walk me through this", "qui appelle X". Works on any project with no setup; a project profile (.agents/project.json) plugs in its tracker, repos, glossary and domain knowledge. Starting or resuming a ticket as a whole belongs to delivery; building the change together to pair.
compatibility: Works in Claude Code and Codex. Needs python3 (python on Windows) and git; gh for GitHub issues and pull requests; the tracker's MCP when tickets live in Jira or Linear; optionally the Figma MCP and an editor CLI (code, cursor).
allowed-tools: Bash(git -C * fetch *), Bash(git -C * show *), Bash(git -C * grep *), Bash(git -C * diff *), Bash(git -C * log *), Bash(git -C * rev-list *), Bash(git -C * remote *), Bash(git -C * symbolic-ref *), Bash(gh pr list *), Bash(gh pr diff *), Bash(gh pr view *), Bash(gh issue view *), Bash(code -g *), Bash(code --add *), Bash(*/explain/scripts/explain-page *)
---

# explain

Explain a subject in the code's real terms (a TLDR in the chat for a trivial one, an explain page otherwise), walk its stations in the editor, then have the user say the key points back. The page is the map; the editor is the code itself; the « redis-le-moi » is where a fuzzy picture shows before it costs anything.

The goal is **understanding before implementation**: the user ends this skill able to explain the subject in their own words, in the vocabulary of the code. The opposite of an ELI5: every real name stays (service names, function names, tables, flags), and what goes away is the unstated assumptions.

## The subject

Say in one line which of these it is; it decides what is read and from where.

| Subject | Asked as | The trip | Code read from |
|---|---|---|---|
| **ticket** | a key or a link | the current flow, and what the ticket changes on it | each repo's default branch on origin, fetched: what the ticket will change |
| **flow** | "qu'est-ce qui se passe quand…" | the current flow, end to end; nothing changes | the branch the user is on (`HEAD`) |
| **module** | a file, a folder, a class, "ce module" | what it is for, its entry points, who calls it, what it calls, its main path, and what data comes in, is stored and goes out | the branch the user is on (`HEAD`) |
| **diff** | a pull request, a branch, "ce que je viens de changer" | the flow before, and what the diff changes on it | the base and the head of the diff |

For a flow or a module, say which branch `HEAD` is and how far it is behind origin's default branch when it is (`git -C <repo> rev-list --count HEAD..origin/<branch>`); the user can ask for the default branch instead. Only a ticket has a key; the others are named by a short slug (`fee-floor`, `hooks`), used for the page and the notes.

## The project profile

Optional. When there is one, load it first: `.agents/project.json` (or `.claude/project.json`) in the current repo or the nearest folder above it, or the file `$PROJECT_PROFILE` names. Its fields are in references/profile.md: the project's name and domain, where its repos are cloned, the tracker, the glossary, the domain skills to consult, the traps the team has learned, the editor and the page language.

A flow, a module or a diff in the current repo needs none: go straight to the steps. A ticket with no profile: offer the `project-setup` skill when it is installed, else discover what the session can (the git remotes of the current folder and its siblings, `gh`, the tracker from the ticket link the user gave), ask once for the rest in one short message, and offer to save the answers as `.agents/project.json`. Every step below says what it reads from the profile; a missing field just skips what depends on it.

## Vocabulary

- **The real term leads.** Each code or business term appears as it is spelled in the code or the ticket, in backticks for identifiers.
- **Gloss once.** The first time a term appears, follow it with a one-line definition in parentheses; reuse it bare after that. An analogy may follow the definition when the concept is abstract: `computed field` (un champ calculé à partir d'autres, comme une cellule-formule dans Excel).
- **Glossary first.** When the profile names a `glossary`, or the repo has a `GLOSSARY.md` at its root, take the gloss from it when the term is there, so the same word gets the same definition everywhere. When the user uses a term in another sense than the glossary or the code does, say so: that is usually where the misunderstanding sits.
- The prose is in the profile's `language` (the user's language otherwise, French by default); identifiers stay verbatim.

## What the user already knows

Before picking the depth, read the user's learner notes: `~/.agents/learner/<project>.md` (`<project>` is the profile's `project`, else the repo folder's name; `$LEARNER_DIR` names another folder). No file, or nothing on this zone: explain as for a newcomer to it.

- The file's format, enough to read and write it; references/learner.md has the finer rules (merging, pruning, a sample):
  ```
  # Learner notes · <project>

  ## Zones
  - `<path or zone>` · <vu | solide | à revoir> · <YYYY-MM-DD> · <one line of evidence>

  ## Termes acquis
  - `<term>`, `<term>`

  ## Écarts récurrents
  - <the confusion, in a few words> · <n> fois · <where it showed, latest date>

  ## Préférences
  - <how the user likes to work>
  ```
  `vu`: explained, not checked. `solide`: said back right, wrote code there that passed review, or « ça je connais ». `à revoir`: the gap was on the heart of the zone. One line per zone, updated in place; observed facts, never a judgement of the person.

- A zone marked `solide`: do not explain it again. Its stations fold into one line each, its terms go bare, and the words go to what is new. Check first that it has not moved: `git -C <repo> log --oneline --since=<its date> -- <path>`; with commits since, say how many and treat it as `vu`.
- A zone marked `à revoir`, or a recurring gap this subject touches: lead with it, and aim the « redis-le-moi » at it.
- A term under `Termes acquis`: no gloss.
- Say in one line what you skip and why, so the user can undo it: « Je passe vite sur `action()` et `markers()` (solide, 13 nov) ; dis « reprends tout » pour l'explication complète. »
- A zone marked `solide` more than a month ago: fold it all the same, and aim one « redis-le-moi » prompt at it. What was said back once fades, and retrieving it is what keeps it.
- « ça je connais », about a zone or a term, at any point: stop explaining it, and record it as `solide` with the user's word as the evidence.

## Steps

1. **Pick the depth and say it in one line, with its reason.** Pick it from what the subject touches; the user can say "express", "léger" or "full" at any point, and you switch on the spot.
   - **Express**: no flow to trace, the diff or the file is the whole story (a copy or i18n change, a package bump, a config or flag value, a rename in one place, one short function). The light investigation of step 2, the TLDR in the chat, step 6; no page, no walk, no « redis-le-moi », no step 7.
   - **Léger**: one repo, no API contract, data or configuration change, nothing to decide (a tooltip with a condition, a small UI rule, a module of a few files). Départ, the stations that matter (for a ticket or a diff, those that change), the Terminus.
   - **Full**: everything else. The whole trip.
   - An initiative or an epic is full. Its trip is the end-to-end journey its children deliver together (first actor to last screen), not one story's flow, and the page pins each child ticket on the stations it touches, with the hops no ticket covers yet as gaps.

2. **Investigate.** Facts come from sources, never from intuition:
   - **A ticket**: it and every comment, from the profile's `tracker`: Jira through the Atlassian MCP (`getJiraIssue` + `listJiraIssueComments`), GitHub with `gh issue view <n> --repo <owner/name> --comments`, Linear through its MCP, or the text the user pasted. Decisions in comments override the description. A Figma link → `get_design_context` on that node. An initiative, an epic or a ticket with sub-tasks: its children too, one level down at a time, each with its description and comments.
   - **A diff**: `gh pr view <n>` and `gh pr diff <n>` for a pull request, `git -C <repo> diff <base>...<head>` and `git -C <repo> log <base>..<head>` for a branch, and the ticket it names when it names one.
   - **The code**, on the ref the subject's row names: `git -C <repo> fetch` first for a ticket, then one subagent per repo when the agent can run them (Claude Code's Explore agent, Codex subagents), else one repo at a time yourself, told to read through `git -C <repo> show <ref>:<path>` and `git -C <repo> grep <term> <ref>` and to trace the current flow with `file:line` for every hop (who calls whom, which endpoint, which table or event). For a ticket, a local branch or a worktree lags behind and misses whole callers. Brief each one (or yourself) to return only: <flow_trace> one line per hop (caller → callee, file:line, endpoint/table/event), then <other_callers> of anything the subject changes or exposes, then <obstacles> (files missing on the ref, ambiguous callers, what it could not trace and why). A module of a few files needs no subagent.
   - **The zone's history**: the last merged pull requests that touched the same files (`gh pr list --repo <owner/name> --state merged --search <path or term> --limit 5`), read with the profile's `pr_diff` command when it has one, `gh pr diff <n> --repo <owner/name>` otherwise, when one looks related; without a GitHub remote, `git -C <repo> log --oneline -5 -- <path>`.
   - The domain skills the profile's `skills` maps to the zone the subject lands in.
   Done when every hop of the current flow has a `file:line` and every claim in the sections below can point to a source.
   - Express reads only the subject itself and the lines concerned (for a bump, the dependency line and its changelog): no subagent or per-repo pass, no zone history, no domain skill. Done when each TLDR bullet has a `file:line`.

3. **Explain.** Express: the TLDR in the chat, nothing else. Léger and full: on a page (see Page), the subject as a **métro trip**, one screen at a time, a big picture and few words per screen, the real identifiers kept. Repos are coloured lines, flow hops are stations, a hop that changes repo is a correspondance, and a line map across the top says "Vous êtes ici".
   - **Show first** when the subject is something a user sees: run it live (the raw response through `curl`, or the screen through the browser tools), paste that output into the chat itself, and open the 2 or 3 key files in the editor (`code -g <path>:<line>`). Chat links are relative to the workspace root. A summary and `../`-prefixed links lose the reader; the raw JSON and the real screen bring them back.
   - **TLDR**: 2 or 3 bullets the summary doesn't already say: where it lands or lives (repo and file), the biggest trap, what to check first. On a page it opens Départ under the summary (`tldr`); in express it is the whole answer, each bullet with its `file:line`, the first one saying what changes (a ticket, a diff) or what it does (a flow, a module).
   - **Départ** is the mental map, and its first screen holds the title, the TLDR and the top of the trip map. The map is drawn by the page from the stations themselves (one lane per repo; for a ticket or a diff, Avant / Après on one layout): mark with `links` each segment that is not a direct call, the missing ones, and what the change builds there. Under it, the folds: the summary (with *avant / après* for a ticket or a diff: what the user sees today and after, a few bullets each), *le besoin* (for a module: what it is for and who relies on it), and, with children, the tickets, each pinned to its stations. Its quai lists the 4 or 5 files to open, in order, each with why. The reading budgets and map rules are in references/page.md, and the script warns past them.
   - **One station per hop of the current flow**: the station name is the real identifier with its `layer` beside it (frontend, gateway, backend, data), then one plain sentence, the real call with its `file:line`, a large picture of that hop with the station highlighted, and for a hop that changes, what changes there. A module's trip starts at its entry point and follows its main path; a second path worth knowing is joined with a `links` entry. "Descendre dans le code" opens the quai: the excerpt with the key lines marked, and a sketch diff when the change is mechanical.
   - **Terminus**: the traps, the 1 to 3 that block marked `blocking` so they lead and the rest fold, the open questions (what the ticket and its comments leave unsaid, or what the code does not say about itself; they feed the grilling in delivery, and one that only another person can answer names who), and the lexicon. Look for the traps every codebase has: API contracts consumed elsewhere, other callers of what changes, migrations and shared databases, feature flags and per-customer configuration, generated code, i18n, what burned the team in the zone's recent pull requests, and an equality the change loosens into an overlap or a range (every caller that grouped by it or relied on it being transitive, and every quantifier that holds on an empty set). For a flow or a module, the traps are what a newcomer gets wrong: an invariant nothing enforces, an order that matters, a name that lies. Then the profile's own `traps`.
   In the chat, give the TLDR, plus the page's link when there is one.
   - **Skip the page** when the user asks for the chat only, and when delivery calls (its Situate table has already given the map) unless the user asks for it: the TLDR, the stations in one line each, the traps (blocking first) and the open questions go in the chat, then step 4.

4. **Walk the stations in the editor**, léger and full, once the page is published (or skipped).
   - A flow, a module or a diff: open the files where they are, in the user's checkout.
   - A ticket: the code lives in the ticket's worktree (the profile's `worktree` pattern, default `../<repo>-<key>` beside the repo, on the ticket branch cut from the default branch on origin), added to the editor's workspace with `<editor> --add <dir>` so the explorer reveals each file: never open a snapshot outside the workspace, the explorer cannot follow it. Delivery creates the worktree at this phase; called alone, create it the same way, and say so.
   - Open every station's file at once, in trip order (`<editor> -g <path>:<line>` each, so they sit as tabs in that order), then send one message with one line per station: `n. <station> (<layer>) · <path>:<lines> · what to look at · what changes`.
   - The user reads at their pace and asks about any station; answer that station only, with its `file:line`.
   - No editor CLI on the PATH (or `editor` set to `none`): send the same message with each `<path>:<line>` as a link, and open nothing.
   `<editor>` is the profile's `editor` (default `code`; `cursor` and the other VS Code builds take the same flags).

5. **« Redis-le-moi »**, léger and full, in the same message as the walk: one prompt for léger, two at most for full. Pick the points where a fuzzy picture costs the most: the hop where the change lands, a blocking trap, a correspondance that is not a direct call. Ask the user to say each back in their own words, as an open prompt they answer from understanding, not by scrolling up for a name; never a yes/no and never a quiz on identifiers:
   ```
   Redis-le-moi (ou « passe ») :
   1. Dans tes mots : qu'est-ce qui décide que le plancher s'applique, et à quel moment ?
   2. Qu'est-ce qui casse si `total()` est appelé sans devise ?
   ```
   - What they say right: confirm it in one line, and add what it missed if anything.
   - A gap: correct that point only, with the hop's `file:line`, in two or three lines; never the whole explanation again. When the gap is the heart of the subject, one more prompt on that same point, then move on whatever the answer.
   - « attends, quoi ? » or « je suis perdu », at any point of the explanation: re-pitch that point, one step further back, with the premise that was missing, in plain words with the real identifiers kept. Shorter is not the fix; the missing context is. Record it as a gap.
   - « passe »: the user knows the zone, or wants to move; note it and go on. It is offered every time, and it is never a gate: nothing waits on these answers.

6. **Record**, once the « redis-le-moi » is answered or skipped, where the session keeps its notes (the agent's project memory when it has one, else the profile's `notes` folder, default `.agents/notes/` under the repos root, one `<key or slug>.md` per subject).
   - A ticket or a diff: a `## Compréhension` section of 10 lines or fewer: the flow in one line per hop with its main `file:line`, the traps, the open questions still open (express: the TLDR bullets), and what the « redis-le-moi » showed. A later session restarts from it.
   - A flow or a module: the code already says how it works, so record only what the « redis-le-moi » showed, in two or three lines: the points said back right, and the gap corrected with its `file:line`. Nothing to record when it was skipped.
   - Then, for every subject, update the learner notes (references/learner.md): the zone with its level, today's date and one line of evidence; the terms glossed that the user then used rightly; a gap, new or seen again. The first time the file is created, say where it is in one line.

7. **Grow the glossary** (not for express, and only with a glossary: the profile's, or a root `GLOSSARY.md`). List the terms the explanation glossed that the glossary lacks and that the user then used rightly, and offer to add them in its own format (a `domain-modeling` skill, when installed, owns that format). On a yes, edit the file and run the profile's `glossary_check` command when it has one.

## Page

Léger and full only. The explanation is one HTML page built from a fixed template: write the data as JSON, render, then publish it or open it.

Before writing the page data, read `references/page.md` (JSON shape, map rules); read `evals/fixture.json` only if unsure of a field.

1. Write `<tmp>/<key or slug>.json` (the session's scratch folder, or a temp folder), with its `kind` (`ticket`, `flow`, `module` or `diff`), `project` and `domain` from the profile when there is one, `source.root` set to the folder that holds the repos (the profile's `repos_root`, else the parent of the current repo), and `source.ref` set to the ref you read when it is not the default branch on origin (`HEAD` for a flow or a module).
2. Run `python3 ${CLAUDE_SKILL_DIR}/scripts/explain-page <tmp>/<name>.json <tmp>/<name>.html` (the `scripts/` folder beside this SKILL.md; `python` or `py -3` on a Windows machine where `python3` is the Microsoft Store stub). Without `source.ref` it fetches each repo, reads each `code` range from its fresh default branch, pins the repos' SHAs for the code links (GitHub, GitLab or Bitbucket, from the origin remote) and stamps the date; a failed fetch stops it, and offline `--no-fetch` skips the fetch and the page's date line says so. With `source.ref` it reads that local ref and fetches nothing. The script fills `assets/explain.html`; never read or edit the template to build a page.
3. **Claude with an Artifact tool**: publish the HTML with it (icon `book`, one-sentence description, `capabilities: {sample: {}}`). With `sample`, a reader who selects any other word gets a "Contexte" button: the page asks Claude, on the reader's own account, with the subject and the current station as context, and labels the answer "Généré par Claude"; without it, only lexicon terms open the panel. On a later pass for the same subject, republish the same file path so the link stays. **Codex, or any agent without an Artifact tool**: open the file in the user's browser (`open <file>` on macOS, `xdg-open` on Linux, `start` on Windows) and give its path; the page works as is, its « Contexte » answers aside.
