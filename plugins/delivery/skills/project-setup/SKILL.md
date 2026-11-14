---
name: project-setup
description: Sets a project up for the delivery skills (delivery, explain, pair, review-standards, debrief, ticket, pr, pr-review, announce, pr-screenshots) - checks the tools and connectors they need, says how to install the skills when they are not yet, discovers what it can from the repos (remotes, default branches, PR templates, test and run commands, ticket keys, reviewers, merge settings), asks once for the rest, and writes the project profile .agents/project.json after the user approves it. Use the first time the skills run on a project, when a skill says the profile is missing or wrong, or to review the profile. Even when casual - "setup le projet", "configure delivery pour ce repo", "crée le project.json", "installe les skills de delivery", "set up this project".
compatibility: Works in Claude Code and Codex. Needs git and python3 (python on Windows); gh for GitHub facts; the tracker's and chat's MCPs are checked, not required.
allowed-tools: Bash(*/project-setup/scripts/discover*), Bash(python3 */project-setup/scripts/discover*), Bash(gh auth status), Bash(git -C * remote *), Bash(git -C * symbolic-ref *)
---

# project-setup

Get a project ready for the delivery skills: the tools are there, the skills are installed, and `.agents/project.json` says what is true for this project. The profile's fields are documented in the `delivery` skill's `references/profile.md`; read it before step 3.

Facts come from the repos first, the user second: never ask what the repos already say, and never write a guess into the profile without showing it.

## Steps

1. **Find the project.** The repos root is the folder that holds the project's repos: the parent of the current repo, or the current folder when it holds several repos. Say which root you take and which repos you found in one line; the user can name another root.

2. **Discover.** Run `python3 scripts/discover --root <root> --gh` from this skill's folder (`python` where `python3` is the Windows Store stub) (drop `--gh` when gh is missing or signed out). It prints, read-only:
   - each repo's remote, host, `owner/name`, default branch, PR template, and the test, lint and run commands its Makefile, package.json, justfile, Taskfile or pyproject declares;
   - the ticket keys seen in recent branches and commit subjects, and the branch-name shapes in use;
   - with `--gh`, each GitHub repo's allowed merge methods and its most frequent recent reviewers;
   - which tools are on the PATH, and any `.agents/project.json` already there.
   An existing profile is the starting point: this run reviews and completes it, it does not start over.

3. **Check the tools and connectors.** From the discovery and the session's own tools, list what each skill needs and whether it is there:
   - `git`, `python3` (all), `gh` signed in (pr, announce, delivery, and GitHub issues);
   - the tracker's access: the Atlassian MCP for Jira, gh for GitHub Issues, the Linear MCP for Linear;
   - the chat's MCP for announcement drafts (Slack), optional;
   - which agent runs the skills (Claude Code, Codex, or both on the team): explain publishes its page with Claude's Artifact tool when there is one, and opens it in the browser otherwise;
   - an editor CLI (`code`, `cursor`) for explain's walk and pair's stops, optional: without one the skills give links in the chat;
   - a grilling and a TDD skill (for example `mattpocock-skills`), optional.
   Say what is missing and what it costs (a missing chat MCP only means the announcement is copied by hand). Installing a connector or signing in is the user's step: name it, do not do it.

4. **Install the skills** when the agent does not list them yet (`delivery`, `explain`, `pair`, `review-standards`, `debrief`, `ticket`, `pr`, `pr-review`, `announce`, `pr-screenshots`). In Claude Code the plugin is the way, since it also brings the pair-marker hook and the updates: installing a plugin is the user's step, so name the command for them (`/plugin install delivery --marketplace <owner/repo>`, which brings the `pair` plugin with it, or the two commands of the repo's README for a local folder). For Codex, or skills without the plugin, gate: show where they would go (Claude Code: `~/.claude/skills/<name>/`; Codex: `~/.agents/skills/<name>/`; for one repo only: its `.claude/skills/` or `.agents/skills/`) and run the `install` script at the root of the repo this skill came from only on the user's go. Never overwrite a skill of the same name without showing the difference first.

5. **Draft the profile.** Fill `.agents/project.json` from the discovery:
   - `repos_root` from step 1; `editor` from the editor CLI on the PATH; `tracker.key` from the most frequent ticket key, and `tracker.kind` and `site` from where that key lives (a Jira link in commit messages or the PR template, GitHub issue numbers, a Linear prefix);
   - `branch` from the most frequent branch shape, `commit` from the commit subjects' shape (conventional commits with the key as scope when they show it);
   - `commands` per repo from what the repos declare, as one line each (`make test (api) · npm test (web)`);
   - `pr.reviewers` from the frequent reviewers, under the first names the user will say (ask for the names when only logins are known);
   - `deliver.merge` from the merge methods the repos allow, and whether a merge queue is in use.
   Then ask, **in one message**, only for what the repos cannot say: the project's domain in a few words, the tracker's statuses for start / review / done, the chat and channel for announcements and its header, the days nothing is merged, what must exist outside the code before a merge reaches QA, how a merge reaches QA (`deliver.release`), and the traps that have burned the team. Offer a sensible default for each so the user can just say yes.

6. **Write it** ⛔. Show the full JSON with each field marked found (and where) or answered. Gate: write it on the user's go, at the root of the repo the team shares (or of the repos root for a multi-repo project). Whether it is committed for the team or kept local is the user's call; say that a committed profile gives every teammate the same setup.

7. **Check it.** Read the written file back as JSON, check that `repos_root` and every path in it exist, that each command's first word is on the PATH, and run the explain fixture once: `python3 <explain skill>/scripts/explain-page --no-fetch <explain skill>/evals/fixture.json <tmp>/fixture.html`. Report each check in one line.

8. **Hand over.** One short paragraph: what the skills can do now on this project, and the first thing to try: « explique-moi <KEY-n> » for one ticket, « on commence <KEY-n> » for the whole pipe. Name anything still missing from step 3 and what it costs.

## Rules

- Read-only until step 4's or step 6's gate: discovery never changes a repo, a branch or a setting.
- One question message, not a quiz: everything the repos could not answer, together, each with a default.
- No secret in the profile: no token, no password, no private URL with credentials. The profile names where things are, not how to log in.
- The profile is in English for its keys and in the team's language for its sentences (traps, notes).
