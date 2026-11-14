---
name: pair
description: Pair-programs a change with the user in the loop - the whole job laid out before any code, plumbing steps chained and committed, one short stop wherever a decision is theirs, the pieces they choose to write prepared with a signature and a red test then reviewed, an unplanned stop when the plan stops holding, and the change seen in the running app. Starts from one sentence of goal, a plan or a ticket; needs no tracker and no project profile. Use when the user wants to build something together, step by step, validating or writing each piece as it lands. Even when casual - "on code ça ensemble", "pair avec moi sur", "on le fait en pair", "étape par étape", "c'est moi qui écris, guide-moi", "let's pair on this", "pair with me". Carrying a ticket from start to QA belongs to delivery, which calls this skill; understanding a ticket or a flow before coding belongs to explain.
compatibility: Works in Claude Code and Codex. Needs git; optionally an editor CLI (code, cursor), a browser the agent can drive for Pre-QA, and TDD, debugging and prototype skills (for example mattpocock-skills). Installed as the pair plugin, its pair-marker-check hook backs the marker rule.
allowed-tools: Bash(code -g *), Bash(code --add *)
---

# pair

Build a change with the user beside you: lay the whole job out, then implement it step by step, stopping only where a decision is theirs, a piece is theirs to write, or the plan stops holding.

The user works beside you in their editor and stays in the loop: they see the whole job before any code, they see each piece of code as it lands, and every decision is theirs. The least friction for them: one short stop where a decision is theirs, nothing to do otherwise.

A **gate** (⛔) is a stop: say what is about to happen, then wait for the user's go before crossing it.

What you write to the user follows the project profile's `language` when there is one (`.agents/project.json`), the user's language otherwise; the labels and samples below are the French ones. The profile is optional here: it gives the `editor`, the `commands` and the domain `skills` when it exists, and the repo's own scripts and instructions file do otherwise.

## What it starts from

- **Called from `delivery`**: the ticket, its `## Scope`, the decisions and the worktrees are already there. The plan is named after the ticket's key, and the notes are the ticket's notes file.
- **Called alone**: a goal in a sentence is enough. Say back in one line what will be true when it is done and how it will be checked, and ask only what the goal leaves open. Work in the current checkout; on the repo's default branch, create a working branch first and say so. When the user does not know the zone the change lands in, offer the `explain` skill first. Decisions come from the user as the overview and the stops raise them.

## Who writes

Two roles, set per step and switched by a word at any time:

- **« tu valides »**, the default: you write, the user validates at the stops.
- **« tu écris »**: the user writes the piece that holds the logic; you prepare it and review it.

The user takes one step with « à moi » or « j'écris celle-là », a kind of step with « j'écris les tests », every step with « j'écris », and hands back with « prends-la » or « reprends la main ». A switch applies to the current step when its code is not written yet, to the next one otherwise; never discard what is written without asking. Record it in the plan, so a later session keeps it: ✍ on the steps the user writes, and their line says what the piece must do, never how (a formula written there before the user took the step goes).

## What the user already knows

Before the overview, read the user's learner notes: `~/.agents/learner/<project>.md` (`<project>` is the profile's `project`, else the repo folder's name; `$LEARNER_DIR` names another folder). No file: nothing to adapt.

- The file's format, enough to read and write it (the `explain` skill's references/learner.md has the finer rules):
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

- `Préférences`: propose ✍ on the kind of step the user likes to write, and say so in the overview; they still decide.
- A step in a zone marked `à revoir`, or one a recurring gap touches: offer it as ✍, or keep its stop's explanation full. In a zone marked `solide`, a stop's explanation goes straight to the decision.
- When the job is done, update the notes: a zone where the user wrote a step that passed review with no blocking remark becomes `solide`, with the date and that fact; a review remark made twice goes under `Écarts récurrents`; a role the user took more than once goes under `Préférences`. Facts that were observed, never a judgement.

## The smallest change that does the job

Understand the code first, then be lazy about the solution, never about the change. For each step, take the first of these that fully works:

1. Does it need to exist? What nobody asked for (an option, a layer, flexibility "for later") is left out, and named in one line.
2. Already in this codebase (a helper, a component, a pattern)? Use it the way the code around it does.
3. In the standard library or the platform? Use it, unless the project has its own.
4. In a dependency already installed? Use it; a few lines never justify a new one.
5. Otherwise the least code that works, written so a reader gets it at a glance.

- The change is finished everywhere it reaches: the callers, tests, fixtures, config and exports it touches. Validation at a trust boundary, error handling that protects data, security and accessibility are never what gets cut.
- A small diff is also what makes a stop worth having: the user validates ten lines they understand, not two hundred they skim.
- A limit taken on purpose is written where it lives, and it ships: a comment `shortcut: <the limit>, <when to revisit it>`. Unlike a pair marker, it stays in the code.

## 1. Work overview ⛔

Before any code, the whole job in one message.

- Numbered steps grouped by PR and repo (one group when there is one repo), each with what it does and the decision that lands in it; what is still to verify on the way; the merge order when there are several PRs, and the end-to-end check.
- **Reach**: list every place the change must touch (the callers of what changes, tests, fixtures, config, exports) and what it could break for a user (data lost or exposed, a caller that stops working). That list is the scope, and the steps cover all of it.
- **Decisions that need no code to answer are asked now, in one round**: numbered, each with your recommended answer, worded so that « oui » accepts it. A question that hangs on another one's answer waits for the next round. A fact the code or the docs can give is looked up, never asked. A decision that needs the code in front of the user stays a ⛔ stop.
- Mark the steps that stop: ⛔ on those holding a decision, ✍ on those the user writes. Plumbing steps chain without a stop. Say in one line that the user can take any step or move any mark, now or later (« à moi pour la 3 », « arrête-toi aussi à la 4 », « enchaîne jusqu'à la fin »).
- Write it to `PLAN-<KEY>.md` (called alone: `PLAN-<slug>.md`) in the user's plans folder, outside every repo so it is never committed and outlives the worktrees: one plan per job, however many repos it spans. The folder comes from the user's memory or instructions file; when none is known, ask once and record the answer (an agent without memory uses the profile's `notes` folder). Open it in the editor. One checkbox per step, with its ⛔ or ✍. You keep it up to date; the user reads it only when they want, and it is how a later session finds where the work stands.
- Gate: the user agrees on the steps, their order, the stops and who writes what.

## 2. Steps ⛔ at the plan's stops

- Recommend the agent's auto-accept mode for this part: the stops are the validation, so an edit-by-edit approval would only double them. Never change the user's permission settings yourself.
- Comments, from the first step: only a non-obvious why or a trap, in as few lines as it takes. No doc comment that restates the name and signature, beyond what the repo's linter asks of a public identifier, and no test comment that restates the test's name. A later comment sweep then finds nothing to cut.
- Each step, test-first where it holds logic (a TDD skill when installed, such as `tdd` or `mattpocock-skills:tdd`); format, lint and test with the profile's `commands` (or the repo's own scripts), the way CI runs them. Before the first test, say where the tests go (which public entry point) and what each one catches and misses. A test's expected values come from the spec, a worked example or a literal, never recomputed the way the code computes them.
- **A plumbing step**: write it, run its tests, commit it, tick it once the commit exists, and chain to the next step without stopping. The next stop shows it.
- **A stop step** (⛔): write it with its markers, run its tests, and leave it uncommitted, so the editor's source-control view shows exactly this step's diff, side by side. Open the first marker with `<editor> -g <path>:<line>`, then stop with a short explanation and the stop block.
  - The explanation comes first, so the developer understands the step before reading the diff. 2 to 4 numbered points, one per thing done, each in three short parts on their own lines, so no line carries too much:
    ```
    **1. Formule portée côté serveur** : `max(base × taux, plancher)`, arrondi au cent
    - Pourquoi : même valeur que l'avertissement affiché dans l'app (AC 02, D3)
    - Où : **web** (frontend) · *checkout* · `computeFee` → **api** (backend) · *pricing* · `feeFor` · [fee.go:36](…)
    ```
  - The title says what, in a few words. « Pourquoi » names the decision, the acceptance criterion or the fact. « Où » holds every location detail: the repo in bold with its layer (frontend, gateway, backend, data), the package or app in italics, the function, the file link; `→` from the source to the destination of a port. Nothing else goes in bold, and no abbreviation the team would not write in full.
  - One last « Vérifié : » line for what you checked on the way when it changed something, for example a constant compared with the other implementation.
  - Then the stop block, three lines at most:
    ```
    Étape 2/6 · formule des frais · 17 tests ✅
    GATE fee.go:31 — plancher = la valeur de la config, pas une constante
    → ok / ta remarque
    ```
  - A decision the user cannot make from a description (a look, a feel, how a state moves): offer something to react to, a throwaway on a scratch branch that never merges (a prototype skill when installed). The answer comes back as one line, and the real code is written properly afterwards.
  - « ok » in the chat validates: you delete the markers yourself. A remark, in the chat or as an edit in the code, is acted on first: read `git diff` and the editor's diagnostics to pick up the user's edits, apply the remark, run the tests, then stop again only if the remark changed a decision. Then commit the step and tick it.
- **A step the user writes** (✍): write what surrounds the piece yourself (imports, wiring, fixtures), then its signature with a `TODO` marker where the body goes, and a red test that says what it must do. Run the tests to show it red, leave everything uncommitted, open the marker, and stop: 1 to 3 points in the same three-part form on what you prepared and what the piece must do, never how, then the block:
  ```
  Étape 3/6 · à toi · 1 test rouge
  TODO fee.go:31 — `feeFor(base, rate)` : applique le plancher de la config
  → écris, puis « fait » · « indice » · « prends-la »
  ```
  - « indice »: the smallest hint that unblocks, one level per ask: where to look (`file:line`), then the approach in a sentence, then the code.
  - « fait »: read `git diff` to see what they wrote, and run the tests. Say what the tests say first, then at most three remarks, each with its `file:line` and what it costs (a wrong result, a missed case, a rule of the repo), never what the formatter fixes. Their code stays theirs: change nothing in it unless they say so. Green and no remark that blocks: delete the marker, commit, tick, chain. Otherwise stop on the remarks.
  - « prends-la »: write the body yourself; the step becomes a stop step, with a `GATE` marker on what you chose.
- **An unplanned stop**, on any step, when the plan no longer holds: an assumption it rests on is false in the code (a function, a field or a value that is not what the plan says), a decision appears that the plan did not name and that changes what a user sees, the data or a contract, the step outgrows its line in the plan (files or a repo it did not name), or the same test still fails after two different fixes. Stop where you are, commit nothing of the step, and say it in four lines at most:
  ```
  Stop imprévu · étape 4/6
  Supposé : `feeFor` reçoit déjà la config
  Trouvé : elle est lue plus haut, dans `Checkout.build` (checkout.go:88)
  → A : passer la config en paramètre (reco) · B : la relire ici
  ```
  On the answer, update the plan first (steps added, changed or dropped, the decision in its step), then carry on. What changes neither the plan nor a decision is not a stop: it goes in the next stop's « Vérifié : » line.
- **When it does not work** (a test that stays red, a behaviour nobody can explain, a bug the user brings): stop guessing and diagnose it together, following references/diagnosis.md: a command that fails on this exact bug first, then ranked hypotheses the user sees before any is tested.
- « attends, quoi ? » or « je suis perdu », at any point: re-pitch what you just said, one step further back, with the premise that was missing, in plain words with the real identifiers kept. Shorter is not the fix; the missing context is. Keep the point for the learner notes.
- Markers, only where they earn it: `// GATE(<owner>): <decision to validate>` on a decision inside a stop step, never on plumbing; `// TODO(<owner>): <what to write>` on a piece the user writes. `<owner>` is `pair`, or the value of `$PAIR_MARKER_OWNER` when the user set one (their first name, usually); the comment sign is the file's own. Markdown files never carry them. A marker still in a file blocks the commit (with this set's plugin, the `pair-marker-check` hook refuses it anyway).
- Questions that do not block a step are kept for the end, not asked one by one.

## 3. Pre-QA ⛔

The last step, when the change shows on a screen or crosses services: the user sees it from the user's side, in the running app. A change with nothing to run (a library, a script) has its tests as the check: say so and skip this.

- You carry every repetitive step (stack, data, images, navigation, captures), so the user's attention goes only to what the change means. Hand the user a command only when it needs them (a login, a secret manager to unlock), as one line for everything.
- The browser tools are loaded first (Claude in Chrome, a Playwright or Chrome DevTools MCP); without them, ask the user to connect a browser rather than relaying clicks.
- *Before*: reproduce the current behaviour on the local stack with realistic data (the profile's `commands.run`, and the domain skill of the stack when `skills` names one); the ids of the test data go under `## Local QA` (in the ticket's notes file when `delivery` called, in the plan file otherwise).
- *After*: run the branch's code in the stack (for a docker compose stack, references/local-branch-images.md), then hand the user the whole test script in one message: the 2 or 3 witnesses to follow, each with why it behaves that way; one table `# | Tu fais | Tu dois voir | Ce que ça prouve`, the last column naming the acceptance criterion or decision; the starting state of the data.
- A field the screen does not show is usually behind a conditional: read what triggers it in the form's schema or component before looking anywhere else. A per-customer setting or a flag flipped for a test is often cached: clear its cache, and put the value back afterwards.
- Gate: the user has seen every acceptance criterion the job owns and says the change reads right.

## Done

Done when every acceptance criterion the job owns has a test, every plan step is ticked, and `rg -n '(GATE|TODO)\(<owner>\)' -g '!*.md'` comes back empty in every repo touched.

- **Called from `delivery`**: hand back to its Review and PR, with the questions kept on the way.
- Either way, update the learner notes first (see What the user already knows).
- **Called alone**: say in a few lines what is committed and on which branch, the `shortcut:` limits the job took, and what was left out or not checked, with any risk the user should know. Ask the questions kept on the way. Nothing is pushed and no PR is opened unless the user asks. Then offer the next two steps of the loop: the `review-standards` skill on the branch, and the `debrief` skill to keep what the session taught.

## Resuming

A job started before: read its plan file, then `git status --short` and `git log --oneline` on the branch. Where the plan and the repo disagree, the repo wins: fix the ticks, then say in one line which step comes next. An uncommitted diff is a step waiting for the user: show its block again (the stop block for a `GATE`, the « à toi » block for a `TODO`).

`<editor>` is the profile's `editor` (default `code`; `cursor` and the other VS Code builds take the same flags). With no editor CLI, or `editor` set to `none`: give each `<path>:<line>` as a link in the chat and open nothing.
