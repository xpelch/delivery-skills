# The project profile

One JSON file that every skill of this set reads, in Claude Code as in Codex: `.agents/project.json` at the root of a repo or of the folder that holds the project's repos (the nearest one above the current folder wins; `.claude/project.json` is read too), or the file `$PROJECT_PROFILE` names. Every field is optional; a missing one only skips what depends on it, and a skill that needs it asks once, then offers to save the answer here.

```json
{
  "project": "acme",
  "domain": "facturation pour PME",
  "language": "fr",
  "repos_root": "~/src/github.com/acme",
  "editor": "code",
  "worktree": "../{repo}-{key}",

  "tracker": {
    "kind": "jira",
    "site": "acme.atlassian.net",
    "key": "ACME",
    "statuses": { "start": "In Progress", "review": "In Review", "done": "In QA" },
    "reference_tickets": ["ACME-120", "ACME-214"]
  },

  "branch": "feat/{KEY}/{slug}",
  "commit": "{type}({KEY}): {description}",

  "commands": {
    "test": "make test",
    "lint": "make lint",
    "run": "docker compose up -d && open http://localhost:3000"
  },

  "pr": {
    "title": "{type}({KEY}): {description}",
    "reviewers": { "Jo": "jo-github-login" },
    "reply_voice": "English, lowercase, no punctuation, one or two short lines"
  },

  "review": {
    "comment_language": "en",
    "voice": "lowercase, one or two short sentences, questions not prescriptions",
    "taste": ["one rule in one place, never duplicated", "a named helper over an inline block repeated twice"],
    "rules": ["~/src/github.com/acme/docs/engineering/rules"]
  },

  "announce": {
    "chat": "slack",
    "channel": "dev-acme",
    "channel_id": "",
    "header": ":pr-open:",
    "language": "fr"
  },

  "deliver": {
    "merge": "gh pr merge --merge",
    "no_merge_days": ["friday"],
    "rollout": ["feature flag exists in every environment", "migration reviewed by the DBA"],
    "release": "",
    "notes": "QA tests on the qa environment; staging is shared."
  },

  "glossary": "~/src/github.com/acme/docs/glossary.json",
  "glossary_check": "",
  "pr_diff": "",
  "skills": { "billing": "acme-billing", "the app as a whole": "acme-stack" },
  "traps": [
    "Each customer has its own settings row: a change applies to every customer unless it is guarded."
  ],
  "notes": ""
}
```

## Fields

| Field | Read by | What it does |
|---|---|---|
| `project`, `domain` | explain | The project's name, and what its business is in a few words. |
| `language` | all | The language of what the skills write to people (chat, ticket comments the team reads in it, announcements). Tickets and PRs follow the repo's existing language when it differs. |
| `repos_root` | explain, delivery | The folder the repos are cloned in. |
| `editor` | delivery, explain, pair | The editor's CLI, used to open files at a line and to add or remove a ticket's worktrees from the workspace: `code` (default), `cursor` or another VS Code build with the same flags, or `none` to get links in the chat instead. |
| `worktree` | delivery, explain | Where a ticket's worktree goes, relative to its repo, with `{repo}` and `{key}` (lowercase). Default `../{repo}-{key}`, a sibling of the repo. |
| `tracker.kind` | all | `jira` (Atlassian MCP), `github` (`gh issue`), `linear` (Linear MCP) or `none` (the user pastes the ticket). |
| `tracker.site`, `key`, `repo`, `team` | all | Where the tickets are: the Jira site and project key, the GitHub repo of the issues, or the Linear team. |
| `tracker.statuses` | delivery, pr | The status names for start, review and done. Missing: the skill leaves statuses to the user. |
| `tracker.reference_tickets` | ticket | Well-written tickets to read when unsure of the team's tone. |
| `branch`, `commit` | delivery, pair | Branch and commit patterns, with `{KEY}`, `{slug}`, `{type}` and `{description}`. Default: `feat/{KEY}/{slug}` and conventional commits with the key as scope. |
| `commands` | pair, review-standards, delivery, pr | How to test, lint, format and run the project. Missing: the skill reads the repo's README, Makefile or package scripts and asks. |
| `pr.title` | pr | The title pattern. Default: the commit pattern. |
| `pr.reviewers` | delivery, pr | Names the user says mapped to GitHub logins. |
| `pr.reply_voice` | pr | How the author answers review threads on their own PR. |
| `review.comment_language` | pr-review | The language of the comments posted on a teammate's PR. Default: the language of the repo's existing PRs. |
| `review.voice` | pr-review | How those comments sound. |
| `review.taste` | pr-review | What this team's reviewers consistently ask for; pr-review keeps a finding on these even when it is style. |
| `review.rules` | review-standards | Files or folders of code, design and test rules the team shares across repos, read after each repo's own. |
| `announce` | announce | Where and how a set of PRs is announced: `chat` (`slack`, `teams` or `none` for a message to copy), `channel`, `channel_id` for a group chat a search cannot find, a `header`, its `language`. |
| `deliver.merge` | delivery | The merge command or method (merge queue, squash, merge commit). |
| `deliver.no_merge_days` | delivery | Days nothing is merged. |
| `deliver.rollout` | delivery | What must exist outside the code before a merge reaches QA. |
| `deliver.release` | delivery | A command or checklist that releases the merged work to the QA environment. |
| `deliver.notes` | delivery | Anything about the shared environments a careful teammate would say: who books them, what must be free before a merge. |
| `glossary`, `glossary_check`, `pr_diff`, `skills`, `traps`, `notes` | explain, debrief, delivery | See the explain skill: the project's terms, review diffs, domain skills (a stack, a deploy pipeline, a business area), learned traps, and where notes go when the agent keeps no project memory (default `.agents/notes/` under the repos root). |

## What is not in the profile

The profile is the team's, and may be committed. What is one person's stays out of it:

- The plans folder (`PLAN-<KEY>.md`, written by `pair`): the user's memory or instructions file names it.
- The learner notes (`~/.agents/learner/<project>.md`, written by `explain` and `pair`): what this person already knows of the project. Their format is in the `explain` skill's references/learner.md.
- The pair-marker owner: `GATE(pair)` and `TODO(pair)` by default, or `$PAIR_MARKER_OWNER` (see the pair plugin's hooks/README.md).

## Without a profile

Each skill discovers what it can (git remotes and default branches, `gh`, the tracker from the ticket link or key, the repo's PR template and scripts), asks once for the rest in one message, and offers to save the answers here.
