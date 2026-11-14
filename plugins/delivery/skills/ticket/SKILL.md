---
name: ticket
description: Writes or reformats a ticket in the team's story format - Need, Scope, Questions / Validations, Out of scope, numbered GIVEN/WHEN/THEN acceptance criteria - with the technical decisions in one comment, and cuts a big ticket into vertical-slice sub-tasks. Works with Jira, GitHub Issues or Linear through the project profile (.agents/project.json). Use when creating a story or task, rewriting a thin ticket, adding ACs, recording decisions taken while grilling or building a ticket, or splitting a ticket. Even when casual - "mets le ticket au format", "écris les ACs", "crée une story pour", "documente les décisions sur le ticket", "découpe PROJ-123 en sous-tâches", "split this ticket". A status or assignee change alone is a plain tracker call.
compatibility: Works in Claude Code and Codex. Needs the tracker's access - the Atlassian MCP for Jira, gh for GitHub Issues, the Linear MCP for Linear.
allowed-tools: Bash(gh issue view *)
---

# ticket

Write or reformat a ticket: product-voice description, decisions in one comment, sub-tasks as vertical slices.

A ticket has two audiences. The **description** is product copy: the PO, QA and the next developer read it to know what "done" means. The **comment** is the engineering record: the decisions and why. Keep each in its lane.

The tracker, its key and the team's reference tickets come from the project profile (`.agents/project.json`, `tracker`). When the profile names `reference_tickets`, read one when unsure of the tone. When the team already has its own ticket format (visible on the reference tickets or the sibling stories), follow theirs and use the one below only for what theirs leaves open.

## Steps

1. **Gather.** Read the ticket, its parent and its sibling stories, plus whatever the conversation already settled (a grilling session, merged PRs). Done when every Scope bullet and AC you are about to write traces back to a source you read or a decision the user made.
2. **Draft** the description in the format below, in the tracker's usual language (the sibling tickets show it), and show it to the user in chat. Done when the description holds no code identifier and the user approves it. The reporter (usually the PO) owns the ticket, so nothing is written to the tracker before that.
3. **Write** the description (see *Writing to the tracker*).
4. **Record decisions**, if the work produced any, as one comment (see *Decisions comment*). Done when every decision behind an AC has a row.

## Description format

Sections in this order, each heading in bold on its own line. Questions / Validations and the design link are dropped when empty, never left with "N/A".

<ticket_description_template>
[link to the design or prototype]

**Need**
As a <role>, I need <capability>, so <business outcome>.

<One short paragraph: what happens today and why it falls short.>

**Scope**

* <behaviour the user can observe, one per bullet>

**Questions / Validations**

* <open question> — <who confirms>

**Out of scope**

* <adjacent thing this ticket does not do>, with the ticket that does it when one exists

**Acceptance criteria**

AC 01 – <Short title>
GIVEN <context>
WHEN <action or event>
THEN <observable result>
</ticket_description_template>

Writing rules:

- **Product voice.** Name what the user sees: "the field picker", "data unavailable". Code identifiers (field names, error codes, setting keys, endpoints, metric names) live only in the decisions comment, each spelled once, so a rename is a one-place edit: a key spelled two ways across Scope and ACs ships one name in the code and the other in the deploy steps.
- **One behaviour per AC**, numbered `AC 01`, `AC 02`… with an en dash before the title. Each THEN is checkable by QA without reading code.
- **Close with a no-regression AC** whenever the ticket changes existing behaviour: GIVEN existing data or screens, WHEN loaded, THEN unchanged.
- **Failure paths get their own AC**: a dependency down, data missing, an empty state.
- Scope bullets and ACs agree: every Scope bullet is covered by at least one AC.

<sample_input>Grilling settled: invoice reminders can follow each customer's own delay; a customer without a delay gets none; UI only, no new endpoint names in the ticket.</sample_input>

<ideal_output>
**Need**
As an account manager, I need reminders to follow each customer's own payment delay, so a customer on 60-day terms is not chased on day 31.

Today every customer gets a reminder 30 days after the invoice, whatever their terms.

**Scope**

* The customer form offers a payment delay, in days
* Reminders go out when that delay has passed, not at 30 days
* A customer without a delay gets no automatic reminder

**Acceptance criteria**

AC 01 – Set a payment delay
GIVEN an account manager editing a customer  
WHEN they enter a payment delay of 60 days and save  
THEN the customer shows a 60-day delay

AC 02 – Reminder follows the delay
GIVEN an unpaid invoice of a customer with a 60-day delay  
WHEN 60 days have passed since the invoice  
THEN the reminder goes out, and not before

AC 03 – No delay, no reminder
GIVEN a customer without a payment delay  
WHEN their invoice goes unpaid  
THEN no automatic reminder is sent

AC 04 – No regression
GIVEN existing invoices and customers  
WHEN the reminders run  
THEN invoices already reminded are not reminded again
</ideal_output>

Why ideal: each Scope bullet maps to one AC, the empty case has its own AC, and the no-regression AC needs no Scope bullet of its own.

## Decisions comment

Sections in this order; drop any section but Decisions when empty.

<decisions_comment_template>
## QA
<preview URL, steps to see the feature>

## Decisions
| # | Decision | Rationale |
|---|---|---|
| 1 | <decision> | <why> |

## Wording to validate (PO)
| Where | Text | (other language) |
|---|---|---|
| <screen, element> | <text> | <text> |

## Rollout
- Feature flag `<key>`: <who creates it>, <state per environment>
- Configuration `<key>`: <value per customer or environment>, <where it is created>

## Pull requests (merge order)
1. <repo>#<n>
</decisions_comment_template>

- **QA**: only when QA tests a preview before the merge; it then opens the comment.
- **Decisions**: one row per decision behind an AC.
- **Rollout**: what has to exist outside the code before QA, with who creates it and its state: feature flags (a flag the flag service does not know cannot be turned on anywhere), per-customer or per-environment configuration, data to migrate. The `delivery` skill checks this list before the first merge.
- **Edit, not add**: if such a comment already exists, edit it rather than adding another.

## Sub-tasks

When a ticket is too big for one wave of PRs, it is cut into sub-tasks before any code.

- **Vertical slices.** Each sub-task goes through every repo it needs and can be verified on its own; a prefactor, if any, is its own first slice. Vertical slices, blocking edges, prefactor first (same rules as `mattpocock-skills:to-tickets`, if installed).
- **Show the list first**: title, blocked by, what it delivers. Done when the user approves the granularity and the edges.
- **Create** each one as a child of the ticket (a Jira Sub-task with the ticket as parent, a GitHub sub-issue or a task list item linking a new issue, a Linear sub-issue), blockers first, with a short Need and its own ACs in the format above, then link each to its blockers ("is blocked by"). Leave it unassigned: it is assigned when its work starts.

## Writing to the tracker

- **Jira** (Atlassian MCP): Markdown by default (`contentFormat: "markdown"`); end each GIVEN / WHEN line with two spaces so the line break survives inside the AC paragraph. A description holding a panel, media or a mention comes back as HTML: edit it as HTML so the panel survives.
- **GitHub Issues**: `gh issue edit <n> --repo <owner/name> --body-file <file>`, comments with `gh issue comment`; GitHub Markdown keeps the line breaks.
- **Linear** (its MCP): Markdown.
- Reference other work by key or link; the tracker links them itself.
