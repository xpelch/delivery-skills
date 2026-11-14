# Credits

Two open repositories, both under the MIT license, shaped parts of these skills. Nothing is copied from them: the ideas below were adapted to this set's own purpose (understanding code and pairing on it) and rewritten in its own words. Each skill here stands alone; none depends on either repository being installed.

## [mattpocock/skills](https://github.com/mattpocock/skills) (Matt Pocock)

- **Decisions asked in rounds**, each with a recommended answer worded so that "yes" accepts it, and the split between facts the agent looks up and decisions the user makes (its `grilling` skill): `pair`'s work overview.
- **Agreeing where the tests go before writing one**, and expected values that come from an independent source (its `tdd` skill): `pair`'s steps and `review-standards`.
- **A failing command before any theory, then ranked falsifiable hypotheses shown to the user, tagged debug logs, and the cause in the commit message** (its `diagnosing-bugs` skill): `pair`'s references/diagnosis.md.
- **Something to react to when a decision cannot be settled by talk** (its `prototype` skill): `pair`'s stop steps.
- **A one-line repair when a message did not land**, naming the listener's state instead of asking for a shorter answer (its `wait-what` skill): « attends, quoi ? » in `explain` and `pair`.
- **Learning recorded only on evidence**: stated prior knowledge and corrected misconceptions weigh most, coverage is not learning, and what was recalled once fades (its `teach` skill): the learner notes.
- **A root `GLOSSARY.md` as the project's shared language** (its `domain-modeling` skill): `explain`'s vocabulary.
- **A session retrospective that prefers a check to a written rule and keeps always-loaded files to pointers**, and a handover note that points instead of copying and marks what is only assumed (its `retro` and `handoff` skills): `debrief`.
- **Rules for writing a skill**: the verb and the trigger phrases lead the description, each step ends on a completion criterion, the positive target is stated rather than the prohibition (its `writing-for-agents` skill).

Its `grilling`, `tdd`, `diagnosing-bugs`, `prototype` and `domain-modeling` skills are used as they are when installed: `pair`, `explain` and `delivery` name them as the first choice.

## [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) (Dietrich Gebert)

- **The smallest complete change**: the ladder that asks whether the code needs to exist, then whether the codebase, the standard library or an installed dependency already has it, and the list of what is never cut (its `ponytail` skill): `pair`'s "The smallest change that does the job".
- **Listing every place a change must reach before writing it**: `pair`'s work overview.
- **`shortcut:` comments** that name a limit taken on purpose and when to revisit it, and collecting them so a deferral does not become permanent (its `ponytail-debt` skill): `pair` and `debrief`.
- **A review that reads the code a change touches, judges it against the load the project expects, requires a concrete case for every finding, and explains each one in four parts** (what this is, the problem, the fix, what happens if it is skipped), numbered so the user can pick (its `ponytail-review` skill): `review-standards`.
- **Ending on what was not checked**: `pair`, `review-standards` and `debrief`.
