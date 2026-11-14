# When it does not work: diagnosing together

For a test that stays red after two different fixes, a behaviour nobody can explain, or a bug the user brings. A debugging skill, when one is installed (such as `diagnosing-bugs`), owns this; otherwise follow the phases below. The user is in every phase: they know the system, you run the legwork.

## 1. A command that fails on this bug

Before any theory, one command that goes red on this exact failure and that you can run yourself: a failing test, a script against the running app, a fixture diffed against a snapshot, a replayed request. Make it fast and deterministic; for a flaky bug, raise how often it reproduces before going on.

- When the failure needs a human (a click, a login, a device), write the steps as a numbered script the user runs and reports on. A secret or a login stays with the user: never ask them to paste one.
- No such command can be built: stop, say what you tried, and ask the user for what is missing (access, a captured log with secrets removed, permission to add temporary logging).

Done when the command has been run once and its red output is shown.

## 2. The smallest reproduction

Cut inputs, callers, config and data one at a time until everything left is needed for the failure. Confirm with the user that this is the failure they see, not a neighbour of it.

## 3. Hypotheses, shown before any is tested

Three to five, ranked, each one falsifiable: « si c'est X, alors changer Y le fait disparaître ». Show the list and stop:

```
Diagnostic · étape 4/6 · `test_total_small_amount` rouge
1. `fee_for` arrondit avant d'appliquer le plancher → inverser l'ordre le fait passer
2. le test lit `FEE_FLOOR` d'un autre module de config → l'imprimer le montre
3. `total()` garde un résultat en cache → le vider le fait passer
→ laquelle d'abord ? (je recommande 1) · ou la tienne
```

The user often has the missing fact: a hypothesis they add goes first.

## 4. One variable at a time

Each probe tests one prediction. A debugger first, then targeted logs, each carrying one unique tag (`[DEBUG-a4f2]`) so a single search removes them all. For a slowdown: measure first, then bisect.

## 5. Fix, with the test that would have caught it

Turn the reproduction into a test that fails, fix the root cause once in the shared code after reading every caller of what you touch, watch the test pass, then run the phase 1 command on the original scenario. When the only place a test can go is too shallow to reproduce the real failure, say so instead of writing a test that passes for the wrong reason.

This fix is a stop step: the cause in two lines, the diff uncommitted, a `GATE` marker on the fix, and the usual stop block.

## 6. Leave nothing behind

The tagged logs are gone, the throwaway scripts are deleted, the regression test stays, and the commit message says which hypothesis was right, for whoever debugs here next. Add the cause to the learner notes when it corrected something the user believed.
