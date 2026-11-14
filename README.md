# delivery-skills

**Understand the code, then build the change with Claude, instead of handing the work over.**

Agent skills for people who want to stay the developer. Claude traces the code and makes sure you can explain it back; it lays the whole job out before writing anything; it stops where a decision is yours; it hands you the pieces you want to write yourself, with a failing test, and reviews what you wrote. When the work is done it tells you what you learned and what the project should remember, and the next session starts from there.

Two plugins for [Claude Code](https://claude.com/claude-code), in the open Agent Skills format, so the same files also serve Codex and other agents that read skills:

- **`pair`**, the core: four skills and one guardrail hook. No ticket, no tracker, no setup.
- **`delivery`**, optional: a ticket-to-QA workflow built on top of `pair`, for teams that want the whole pipe.

## Quick start

In a Claude Code session:

```
/plugin install pair --marketplace xpelch/delivery-skills
```

Then, in any repository:

```
explain this module: src/billing/
```

```
let's pair on this: fees must never go below the floor in settings
```

That is all the setup there is. The skills also trigger on their own from what you type, in English or in French.

## The four skills

| Skill | What it does |
|---|---|
| `explain` | Builds your understanding of a ticket, a flow, a module or a diff before any code: the current flow traced with `file:line`, the traps, the open questions, the files opened in your editor in reading order. It ends by asking you to say one or two key points back, and corrects only the gap. |
| `pair` | Builds a change with you from one sentence of goal. A work overview first; plumbing steps chained and committed; a stop on each decision, uncommitted, with a marker in the code; any step you want to write yourself, prepared with a signature and a red test, then reviewed. It writes the smallest change that does the job, and diagnoses a failure with you instead of guessing. |
| `review-standards` | Reviews your branch the way the developer who gets paged for it would: correct, safe, holds at the load the project expects, tested, by the project's own rules, lean. It reads the code your change touches, not only the diff, and explains each finding in four parts: what the code does, the problem, the fix, what happens if you skip it. |
| `debrief` | Closes the session with proposals you pick from: what you now hold, where it snagged, what the project should remember (a check rather than a written rule, a pointer, a glossary term, a trap), what is left, and where the next session starts. |

And one hook, `pair-marker-check`: it refuses a `git commit`, `git push` or `gh pr create` that still carries a pairing marker, naming the file and the line. Details in [plugins/pair/hooks/README.md](plugins/pair/hooks/README.md).

```
explain ──► pair ──► review-standards ──► debrief
   ▲                                         │
   └──── learner notes · glossary · traps ◄──┘
```

Each skill works on its own and hands to the next. What `debrief` writes is what the next `explain` and the next `pair` read first.

## What a pairing session looks like

1. **Work overview.** The whole job in one message, and in a `PLAN-<name>.md` file kept outside the repo: everything the change must reach (callers, tests, config), numbered steps, which ones stop for you, the end-to-end check. Decisions that need no code to answer come in one round, each with a recommended answer. Nothing is written until you agree.
2. **Steps.** A plumbing step is written, tested, committed and ticked without a question. A step that holds a decision stops uncommitted, so your editor's source-control view shows exactly that diff, with a `GATE(pair)` comment on what you validate and a short block that says what was done, why, and where:

   ```
   Step 2/6 · fee formula · 17 tests ✅
   GATE fee.go:31 — the floor comes from config, not a constant
   → ok / your remark
   ```

3. **Your turn.** Take any step, at any time. You get the code around the piece, its signature with a `TODO(pair)`, and a failing test that says what it must do, never how. Ask for a hint and you get the smallest one that unblocks. Say you are done: the tests run, and you get at most three remarks, your code untouched.
4. **When the plan breaks.** If an assumption turns out false in the code, it stops and says what it assumed, what it found, and the options. If something simply will not work, it builds a command that fails on that exact bug first, then shows you ranked hypotheses before testing any.
5. **Pre-QA.** When the change shows on a screen, you see it in the running app, with a short script that says what each step proves.

Lost at any point? Say so (« attends, quoi ? »): the last thing said is pitched again, one step further back, with the premise that was missing.

## It remembers what you know

`explain` and `pair` keep one small Markdown file per project, `~/.agents/learner/<project>.md`: the zones you have seen, the ones you hold (you said them back right, or wrote code there that passed review), the terms you no longer need defined, the confusions that came back, and how you like to pair.

The next explanation in a zone you hold folds it into a line and spends its words on what is new. A confusion that came back gets the next question. A zone you held a while ago gets one question again, because what was recalled once fades.

The file is yours: plain text you can read and edit, never in a repository, never shared with a team. It records what was observed, not a judgement of you.

## How to tell it is working

- `explain`: every hop has a `file:line`; it says which branch it read; it ends with one or two open questions and a way to skip them; a second explanation in a zone you hold says what it skips.
- `pair`: no code before you agree on the overview; plumbing commits arrive without a question; a decision stops uncommitted with a `GATE(pair)` marker; taking a step gives you a signature and a red test, never the body; a step's diff fits on a screen.
- `review-standards`: each finding names a concrete case and what happens if you skip it; findings are numbered so you can answer "fix 2 and 5"; it ends on what it did not check.
- `debrief`: nothing in the repo changes before you pick; your learner notes carry today's date afterwards.
- The hook: a commit that still carries a pair marker is refused.

## The `delivery` plugin

For teams that work from tickets. It installs `pair` with it.

```
/plugin install delivery --marketplace xpelch/delivery-skills
```

`delivery` carries one ticket through seven phases, with a gate wherever a decision is yours or work leaves your machine, and a notes file per ticket so a later session resumes where the last one stopped:

1. **Situate**: the ticket, its siblings, the repos it touches, what the code contradicts in the ticket.
2. **Understand**: `explain`.
3. **Decide**: the open questions and the gaps of the spec, settled with you, then written to the ticket once.
4. **Work overview** and 5. **Pair implementation**: `pair`.
6. **Review and PR**: `review-standards`, then one gate for the PR descriptions, the reviewers and the announcement.
7. **Deliver**: merges in order under your merge rules, release, cleanup, then `debrief`.

| Skill | What it does |
|---|---|
| `delivery` | The conductor of the seven phases. Runs only when you invoke it: `/delivery:delivery PROJ-123`. |
| `project-setup` | Reads what your repos already say (remotes, branches, commands, reviewers), asks once for the rest, and writes the project profile. |
| `ticket` | Writes a ticket (need, scope, GIVEN/WHEN/THEN acceptance criteria), records decisions, cuts a ticket into vertical sub-tasks. Jira, GitHub Issues or Linear. |
| `pr` | PR title and description, a sweep of the comments the branch adds, answers to review threads on your PR. |
| `pr-review` | Reviews a teammate's PR: verified findings, comments in your team's voice, posted only on your go. |
| `announce` | The team-chat message that announces the PRs in merge order, left as a draft. |
| `pr-screenshots` | Screenshots of the running app, put into the PR description. |

What differs from one project to another (tracker, statuses, branches, commands, reviewers, merge rules, glossary, your own domain skills) lives in one optional file, `.agents/project.json`. `explain` and `pair` work without it. Every field is described in [profile.md](plugins/delivery/skills/delivery/references/profile.md), with a full example in [profiles/example.json](profiles/example.json).

## Install, in detail

**From a terminal**, or on a Claude Code older than 2.1.275:

```bash
claude plugin marketplace add xpelch/delivery-skills
```

```bash
claude plugin install pair@delivery-skills
```

**For a whole team**, enable it from the project, so every teammate gets it when they trust the repository:

```bash
claude plugin install pair@delivery-skills --scope project
```

**From a local clone**, pass its path instead of `xpelch/delivery-skills`. To try it without installing: `claude --plugin-dir /path/to/delivery-skills/plugins`.

**Codex and other agents:** clone the repository and run `./install` (on Windows: `bash install` from Git Bash). It copies the skills to `~/.claude/skills/` and `~/.agents/skills/`. `--core` copies the four core skills only, `--project <repo>` installs into one repository, `--dry-run` shows what it would do. The hook is not installed this way; [its README](plugins/pair/hooks/README.md) shows how to register it by hand.

After installing, run `/reload-plugins` in an open session. Skills are invoked as `/pair:explain`, `/pair:pair`, `/pair:review-standards`, `/pair:debrief` and `/delivery:<skill>`.

**To update:** `/plugin marketplace update delivery-skills`, then `/reload-plugins`.

## Requirements

- `git` and Python 3. Every script uses the standard library only.
- Optional, for the core: an editor command line (`code`, `cursor`) so files open at the right line, and a browser the agent can drive for Pre-QA. Without them you get links in the chat.
- For `delivery`: `gh` signed in, and access to your tracker (the Atlassian or Linear connector; GitHub Issues goes through `gh`).
- On Windows: Git for Windows. The hook starts through its `sh`, and picks `python` when `python3` is the Microsoft Store placeholder.

`pair`, `explain` and `delivery` use a few well-known skills when you have them installed (test-driven development, debugging, prototyping, grilling, a project glossary; for example those of [mattpocock/skills](https://github.com/mattpocock/skills)), and carry their own short version when you do not.

## Status and limits

This is a young project. What has been checked, and what has not:

- **Checked:** `python3 check` and `claude plugin validate --strict` pass; the hook has 18 tests and was exercised in real sessions; six eval cases run the core skills against a baseline with no plugin, three runs each.
- **Developed and tested on Windows** with Git for Windows. The scripts are POSIX `sh` and standard-library Python, and are expected to run on macOS and Linux, where they have not been run yet.
- **Written by a French speaker.** The skills answer in your language, but the sample lines inside them and the short command words (« à moi », « fait », « indice », « passe », « attends, quoi ? ») are French. Their equivalents in your language are meant to work the same; only the French ones have been tested. The labels of the explain page are French.
- **`delivery` has been used on one team's workflow** and generalised from it. Its tracker and chat steps have not been run against Linear or Teams.
- `delivery` runs only on an explicit invocation. Remove `disable-model-invocation` from its frontmatter to let it trigger from "let's start PROJ-123".
- Deployments are not a skill here: the profile describes your merge and release rules, and your own skill can be plugged in.

## Develop

```bash
python3 check
```

It verifies that every JSON file parses, each `SKILL.md` has a `name` equal to its folder and a valid `description`, every skill and script the docs name exists, the marketplace lists both plugins and their dependencies, the explain fixtures render, and the hook tests pass. Before sharing a change, also run `claude plugin validate --strict .`.

The `pair` plugin has an eval suite under `plugins/pair/evals/`. Each case is a prompt, a small fixture repository and graders, run with the plugin and without it:

```bash
cd plugins/pair
```

```bash
claude plugin eval . --tag read-only --scaffold --allow-tools Write
```

A seventh case, tagged `shell`, grants Bash, which `claude plugin eval` only runs inside a sandbox (macOS, Linux, or WSL2 with Claude Code installed there):

```bash
claude plugin eval . --tag shell --scaffold --allow-tools Bash Write Edit
```

```
.claude-plugin/marketplace.json    the marketplace, listing the two plugins
plugins/pair/                      the core plugin
  skills/<skill>/                  explain, pair, review-standards, debrief
  hooks/                           the pair-marker hook and its tests
  evals/<case>/                    the eval suite
plugins/delivery/                  the workflow plugin; depends on pair
  skills/<skill>/                  the seven workflow skills
profiles/example.json              a full project profile
install                            copies the skills for Codex and other agents
check                              the checks above
```

When you add or change a skill: its `name` equals its folder; its `description` leads with the verb and the phrases people actually type, then says which sibling handles the neighbouring topic; the body stays under 500 lines, with detail in `references/`. Bump `version` in the plugin's `plugin.json`, since that is what delivers a change to people who installed it.

## Credits

Parts of these skills adapt ideas from two MIT-licensed repositories, [mattpocock/skills](https://github.com/mattpocock/skills) and [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail). [CREDITS.md](CREDITS.md) says which idea went where.

## License

[MIT](LICENSE)
