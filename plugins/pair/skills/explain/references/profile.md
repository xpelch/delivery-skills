# The project profile (explain's fields)

The skills of the pair and delivery plugins share one profile; the delivery plugin's `skills/delivery/references/profile.md` documents every field. These are the ones explain reads.

One JSON file per project, `.agents/project.json` at the root of a repo (or of the folder that holds the project's repos), or wherever `$PROJECT_PROFILE` points. Every field is optional; a missing one only skips what depends on it.

```json
{
  "project": "acme",
  "domain": "facturation pour PME",
  "language": "fr",
  "repos_root": "~/src/github.com/acme",
  "editor": "code",
  "worktree": "../{repo}-{key}",
  "tracker": { "kind": "jira", "site": "acme.atlassian.net", "key": "ACME" },
  "glossary": "~/src/github.com/acme/docs/glossary.json",
  "glossary_check": "",
  "pr_diff": "",
  "skills": { "billing": "acme-billing", "the app as a whole": "acme-stack" },
  "traps": [
    "Each customer has its own settings row: a change applies to every customer unless it is guarded.",
    "The mobile app ships weekly; an API field it reads cannot be renamed in one release."
  ],
  "notes": ""
}
```

| Field | What it does |
|---|---|
| `project` | The name the page and its AI prompts use for the project. |
| `domain` | What the business is, in a few words; the page's « Contexte » answers explain terms in that domain. |
| `language` | The language of the prose and of the « redis-le-moi ». The page's own labels stay French. |
| `repos_root` | The folder the repos are cloned in; a station's `repo` is a folder name under it. It becomes the page data's `source.root`. |
| `editor` | The editor's CLI for the walk: `code` (default), `cursor` or another VS Code build with the same flags, or `none` for links in the chat. |
| `worktree` | Where the ticket's worktree goes, relative to its repo, with `{repo}` and `{key}`. Default `../{repo}-{key}`. |
| `tracker` | Where tickets live: `{kind: "jira", site, key}`, `{kind: "github", repo: "owner/name"}`, `{kind: "linear", team}`, or `{kind: "none"}` when the user pastes the ticket. |
| `glossary` | A JSON or Markdown file of the project's terms. Explanations gloss from it first, and step 6 offers to grow it. |
| `glossary_check` | A command that validates the glossary after an edit. |
| `pr_diff` | A command that prints one pull request's diff in a reviewable form, with `{repo}` and `{n}` placeholders; `gh pr diff` otherwise. |
| `skills` | Zones of the code mapped to the skills that know them; the investigation reads the skill of the zone the ticket lands in. |
| `traps` | What has burned this team before, one sentence each; the Terminus checks them after the generic list. |
| `notes` | A folder for the `## Compréhension` notes when the agent keeps no project memory (default `.agents/notes/` under the repos root). |

## Without a profile

The skill discovers, in this order: the origin remote and default branch of the current repo and of its sibling folders (`repos_root` is their parent), the tracker from the link or key the user gave (an `atlassian.net` link is Jira, a `github.com/.../issues/` link is GitHub), `gh` for pull requests. It asks once for what it could not find (usually `domain` and the tracker), then offers to save the profile.
