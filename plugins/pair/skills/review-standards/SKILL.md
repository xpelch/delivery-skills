---
name: review-standards
description: Reviews the user's own change - a branch, uncommitted work, a diff or a pull request - and explains each finding so that they understand it, in a fresh context. Use whenever the user asks to review, re-read or check a change before committing or opening a PR, even casually - "review ma branche", "relis ce changement", "relis ce que j'ai fait", "check avant de commiter", "check les standards avant la PR", "is this over-engineered", "review this diff". It checks, in order, that the change is right, safe, holds at the load the project expects, has its risky part tested, follows the project's own rules and the ticket's acceptance criteria, and carries no line it does not need; it reads the code the change touches, not only the diff; each finding has a concrete case and four parts (what the code does, the problem, the fix, what happens if it is skipped). Reviewing a teammate's PR to post comments on it belongs to pr-review.
argument-hint: "[PR number | base ref | uncommitted]"
compatibility: Works in Claude Code and Codex. Needs git; gh for a pull request. Runs the review in a subagent with a fresh context when the agent can start one.
allowed-tools: Bash(gh pr diff *), Bash(gh pr view *), Bash(gh pr checks *), Bash(git diff *), Bash(git log *), Bash(git status *), Bash(git grep *)
---

# review-standards

Review the change named by `$ARGUMENTS`: a PR number, a base ref, or `uncommitted`. Empty means the current branch against the repo's default branch, plus what is not committed yet. The report is the whole output; the user decides what gets fixed. It changes no code.

Run the review in a subagent with a fresh context window when the agent can start one, briefed with this whole file and the target: it then judges the code, not the conversation that wrote it. Show its report to the user in full and unchanged, in the shape of step 6: that shape is what makes a finding understood, so it is never condensed into a summary. Without subagents, run the steps yourself.

Order of importance: correct, safe, holds at the expected load, tested, by the project's rules, lean. The reader may not have written this code: every finding is written so that they understand it, not only so that they fix it.

## 1. Understand first

- Get the diff: `gh pr diff <n>` and `gh pr view <n>` for a PR, `git diff <base>...HEAD` for a branch, `git diff HEAD` for uncommitted work. A diff the user hands over as a file or pastes is read as it is.
- Find what was asked: the PR description, the ticket it names, its acceptance criteria and its decisions comment; a `pair` plan file when there is one.
- Read each changed file in full, then the code the change touches: the callers of every changed function, the functions it calls, the tests. A change can break code it does not touch: when a signature, a return value or a behaviour changes, search every caller (`git grep`).
- Trace the real flow: where the data comes in, what is stored, what goes out.
- Find the load the project expects (its README, its deploy config): one person running a script, or many users and processes at once. Judge scale against that, and say which load you assumed.

Done when every changed file is listed with its kind (language, UI, test, config), every acceptance criterion is listed or the report says none was found, and the first line of the report can say what the change does.

## 2. Rules
Load the rules, the nearest first; where two disagree, the nearer wins:

1. The repo's own: `CODING_STANDARDS.md`, `CONTRIBUTING.md`, `CLAUDE.md` or `AGENTS.md`, and `.claude/rules/` or `.agents/rules/`.
2. The project profile's `review.rules` (`.agents/project.json`): files or folders of rules the team shares across repos.
3. The user's: `~/.claude/rules/` (or `~/.agents/rules/`), and the code sections of their global instructions file.

From a folder of rules, read the general files, then only the ones for the kinds of file in the diff. Say in the report which files were loaded. None found: the passes below still run, on what they name; say so under *Not checked*.

## 3. Mechanical checks
Run the repo's format check, lint, typecheck and tests on the changed packages, with the commands the profile's `commands`, the repo's instructions file, `package.json` or `Makefile` give, the way CI runs them. For a PR that is not checked out, read `gh pr checks <n>` instead.

Report each check as pass, fail (with its first failing line) or not run (with the reason). Whatever a linter or the compiler reports belongs to that tool and stays out of the findings.

## 4. Passes
One pass per axis, each over every changed file and the code it touches:

1. **Correct**: each acceptance criterion maps to a code path; a wrong result, a crash, a missed edge case (empty, zero, the last item, rounding, time zones); a caller broken by the change; a fix applied in one caller while the shared function stays wrong.
2. **Safe**: input validated at the boundary, authorization checked, secrets and personal data absent from code and logs; data loss (an error swallowed, writes in the wrong order, no transaction).
3. **Scale**: fine for one user, wrong at the expected load: a check-then-write race, the same work done by every process, a list or a memory that only grows, a query per item, state kept per process that must be shared.
4. **Tested**: each changed behaviour that carries risk (a branch, a parser, money, security, a data write, a bug fix) has a test, at the lowest level that can fail for it, that would fail without the change. Its expected values come from the spec or a worked example, not recomputed the way the code computes them. One good test, not coverage.
5. **By the rules**: the writing, naming, comment, structure and architecture rules loaded in step 2, and the rule file of the language. List the imports of each changed domain file and check which way they point.
6. **Lean**: code that should not exist or should be smaller. Dead code, an option nobody sets, a feature nobody asked for; a helper the repo already has (name its path); what the standard library, the platform or an installed dependency already does; an abstraction with one implementation; near-copies that must change together; one function doing several unrelated jobs. Split by job, never by line count.

Done when every axis has been run over every changed file of its kind, and every rule in the loaded files has been checked.

## 5. Verify
A finding is kept when it has all three:
- a `path:line`;
- a concrete case: this input or this situation leads to this wrong result, or this rule of this file is broken. No case, no finding;
- a second read of the surrounding code confirming it is real and introduced by this change: the caller exists, the value can really be empty, the code really is unused.

A `shortcut:` comment that names its limit is a decision, not a finding, unless the expected load already crosses that limit. A violation that predates the change goes on the single *Pre-existing* line. Propose the smallest fix that works, and prefer one that deletes code. No taste, no "consider", no vague worry.

## 6. Report

Plain words, short sentences. Explain a technical term the first time it appears; keep the code's real names.

Start with `Ce que fait ce changement :` in two or three sentences, and the load you assumed. Then the findings in three groups, numbered across all of them so the user can answer « corrige 2 et 5 »; skip an empty group:

- **À corriger** : wrong behaviour, an unmet criterion, a security hole or a data loss, something that breaks at the expected load, a dependency pointing the wrong way.
- **À corriger ensuite** : risky code without a test, a rule broken at a maintenance cost, real slowness, duplication, code that should not exist.
- **Si tu as le temps** : small speed-ups, shorter forms. Three at most.

Every finding has its four labelled parts, one or two short sentences each, even when the problem looks obvious:

<finding_template>
2. **Les commandes tombent sur le mauvais jour** (`billing/close_day.py:40-52`)
   - **Ce que c'est** : à minuit, ce job ferme la journée et facture toutes ses commandes.
   - **Le problème** : il prend « aujourd'hui » sur l'horloge du serveur, qui est en UTC. Une commande passée à 00 h 30 à Berlin est facturée la veille.
   - **Le correctif** : calculer le jour une seule fois dans le fuseau de la boutique. Une ligne, rien d'autre ne change.
   - **Si on laisse** : les commandes tardives portent la mauvaise date, et la comptabilité les corrige à la main.
</finding_template>

Why this shape: « Ce que c'est » lets a reader who never saw the code follow the rest, and « Si on laisse » lets them decide.

End with:

```
Verdict : prêt | prêt après 1 et 3 | bloqué par 1
Vérifications : lint <résultat> · types <résultat> · tests <résultat>
Règles lues : <files loaded>
Sobriété : -<N> lignes possibles          (when a lean finding exists)
Déjà là avant : <violations that predate the change>
Sans constat : <axes with no finding>
Non vérifié : <what could not be checked, and why>
```

Nothing found: `Ce que fait ce changement :`, then `Rien à corriger. Prêt.` and one line on what you checked.

These labels follow the profile's `language`, or the user's; the ones above are the French ones.
