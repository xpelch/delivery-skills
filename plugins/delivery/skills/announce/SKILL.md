---
name: announce
description: Writes the team-chat message that announces a set of open pull requests to review and merge - the ticket title with its link, the change in plain words, and the PRs in merge order with what each one does - in the team's language and header, and can leave it as a draft in a channel. Reads the project profile (.agents/project.json, announce) for the chat, channel, header and language. Use after opening pull requests when the user asks for a message, announcement or preview of them. Even when casual - "message pour les PRs", "annonce les PRs", "fais le message pour les PRs", "mets-le en preview dans le channel".
compatibility: Works in Claude Code and Codex. Needs gh and the tracker's access; the Slack or Teams MCP only for a draft.
allowed-tools: Bash(gh pr view *), Bash(gh pr list *)
---

# announce

Produce one message that lists the open PRs of a piece of work in the order they must be merged, and hand it over (see *Hand-off*).

## Template

<pr_announce_template>
<header> <ticket title, verbatim> ([<KEY>](<ticket URL>))

<a short summary of the work done: what a user can now do, then what the PRs built, two sentences at most>

<N> PR à merger dans l'ordre :

* [<repo>#<n>](<PR url>) (<type>) : <what this PR does, a few words>
* [<repo>#<n>](<PR url>) (<type>, <dependency or note when needed>) : <what this PR does, a few words>
</pr_announce_template>

`<header>` is the profile's `announce.header` (an emoji like `:pr-open:`, or nothing). The connecting words follow `announce.language` (default French: « PR à merger dans l'ordre », « stackée sur », « indépendante », « captures dans la PR »; English: "PRs to merge in order", "stacked on", "independent", "screenshots in the PR").

<sample_input>SHOP-315 open PRs: shop-web#181 (base is shop-web#179's branch, carries screenshots), shop-api#175 (base is shop-api#173's branch), shop-gateway#38.</sample_input>

<ideal_output>
:pr-open: Compare a discount against a shop setting value ([SHOP-315](https://acme.atlassian.net/browse/SHOP-315))

Une règle de rabais peut maintenant se comparer à la valeur d'un shop setting, au lieu d'une valeur fixe. Une seule règle suit ainsi le seuil propre à chaque boutique.

3 PR à merger dans l'ordre :

* [shop-api#175](https://github.com/acme/shop-api/pull/175) (backend, stackée sur [shop-api#173](https://github.com/acme/shop-api/pull/173)) : évalue la règle contre le shop setting
* [shop-gateway#38](https://github.com/acme/shop-gateway/pull/38) (gateway) : expose les shop settings à l'UI
* [shop-web#181](https://github.com/acme/shop-web/pull/181) (UI, stackée sur [shop-web#179](https://github.com/acme/shop-web/pull/179), captures dans la PR) : ajoute "Shop setting" comme source de valeur
</ideal_output>

Why ideal: the subject is the ticket's own title, untouched; the paragraph says what a user can now do, then what was built; each line is a labeled link, never a bare URL, and says in plain words what the PR does.

## Gather the facts

Do not rely on memory for URLs, numbers, order or titles.

- For each PR, read it with `gh pr view <n> --repo <owner/repo> --json number,title,url,state,baseRefName,headRefName,labels`.
- Keep only PRs that are open. A cancelled ticket gets no line and is not mentioned.
- The ticket keys come from the PR titles or branches.
- For each key, read the ticket title from the tracker (profile `tracker`), the title field only. If the tracker cannot be reached, ask the user for the title rather than writing one.
- The count `N` is the number of lines you list.

## The change in plain words

The paragraph under the subject is a short summary of the work done, for a teammate who has not read the ticket: two sentences at most, the first on what a user can now do, the second on what the PRs built to get there.

- Build it from the work itself: each PR's `## Summary`, and the session's plan and Pre-QA when the work just ran here (`delivery`), so every word names something a PR delivers.
- Say what it does, not how the code does it: "les règles qui ne se sont pas déclenchées apparaissent maintenant dans la liste", not "la strategy retourne une liste untriggered".
- Plain words around the team's vocabulary: a term from *Language* stays as it is, and the sentence around it stays simple.
- One idea per sentence; no history of the decisions, no list of edge cases (they live in the PRs and the ticket).

## Subject line

- The subject is the ticket title copied as it is, in its own language, followed in parentheses by the key linked to the ticket's URL. Do not translate or rephrase it.
- Several tickets: `<title 1> ([<KEY 1>](<url 1>)) + <title 2> ([<KEY 2>](<url 2>))`.

## Order

List in the order the PRs have to be merged, so that someone merging from the top never breaks a deploy:

1. A stacked PR comes after the PR its base branch belongs to (follow `baseRefName` to the head of another PR).
2. At one level of a stack, data and backend first, then gateways and APIs in front of them, then UI, because a screen reads fields the API must already return.
3. A `chore` that unblocks CI goes first.
4. A PR that depends on nothing goes last.

## Each line

- Start the line with `* ` and the PR as a labeled link, `[<repo>#<n>](<url>)`, then the type in parentheses. Never a bare URL: a chat shows it as a chip with the whole domain and path.
- The type is the role of the repo: `backend`, `gateway`, `UI`, `mobile`, `infra`, `chore`, or the plainest word for its role.
- After the parentheses, ` : ` and what this PR does in its repo, a few plain words ("évalue la règle", "expose le champ à l'UI"), never the code identifiers.
- In the parentheses, after the type, comma-separated, only what the order alone does not show:
  - a PR stacked on a PR outside this list: `stackée sur [<repo>#<n>](<url>)`;
  - a PR that depends on nothing: `indépendante`;
  - a `chore` line: a few words on why it is there (e.g. `débloque le CI`);
  - a UI PR that carries screenshots: `captures dans la PR`.

## Language

Careful written language in `announce.language`: full sentences, correct accents and punctuation, no slang. It is an announcement read by the whole team, not a chat reply. Tech and domain terms stay as the team says them, and names from the code or the app as they are spelled; a translated term makes the reader stop and decode it.

- Take the team's terms from the profile's `glossary` when it has one.
- Quote UI labels exactly as the app shows them.
- When unsure whether to translate a term, keep it as the code spells it.

## Hand-off

- Give the message in chat in one code block, as written in the template (markdown links, `* ` bullets). Say that a pasted `[text](url)` stays raw text in the Slack composer, so the draft below is the way to get clean links.
- When the user asks for a **preview** or **brouillon** in a channel, also create a draft there with the chat's MCP (Slack: `slack_send_message_draft`), the message without the code block, in the profile's `announce.channel` unless the user names another. A named channel is found with `slack_search_channels` (private ones included). A group chat is invisible to that search: take its ID from the profile's `announce.channel_id`, or from a recent announcement found with `slack_search_public_and_private` (`channel_types: mpim`). Ask for the link when none or several match. A channel holds one attached draft: on `attached_draft_exists`, tell the user to send or delete the existing one first.
- Never send the message yourself: the user sends the draft.
- Done when the code block is shown and, when asked, the draft waits in the channel's composer.

## Rules

- The message starts with the header and the subject on that same line: an emoji alone on its line wastes a line. Nothing before it, no greeting, no closing line, no emoji elsewhere.
- Plain chat text: no headings, no tables, one blank line between the subject, the paragraph and the list.
- If a PR is not open yet, or a number is unknown, ask rather than guess.
