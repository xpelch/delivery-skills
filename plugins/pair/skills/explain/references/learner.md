# Learner notes

What the user already knows of a project, so an explanation spends its words on what is new and a pairing session hands over the right pieces. One Markdown file per project and per person, written by `explain` and `pair`, readable and editable by the user.

## Where

`~/.agents/learner/<project>.md`. `<project>` is the profile's `project`, else the name of the repo's top folder. `$LEARNER_DIR` names another folder. The file is the user's own: never in a repo, never in the project profile, never committed. The first time you create it, say where it is in one line.

## Format

<learner_notes_template>
# Learner notes · <project>

## Zones
- `<path or zone>` · <vu | solide | à revoir> · <YYYY-MM-DD> · <one line of evidence>

## Termes acquis
- `<term>`, `<term>`

## Écarts récurrents
- <the confusion, in a few words> · <n> fois · <where it showed, latest date>

## Préférences
- <how the user likes to work: what they write themselves, what they skip>
</learner_notes_template>

<sample_notes>
# Learner notes · shop

## Zones
- `hooks/pair-marker-check` · solide · 2026-11-13 · a redit juste le staging d'un commit ; écart corrigé sur le diff de branche
- `pricing/fees.py` · solide · 2026-11-12 · a écrit `fee_for` en pair, relecture sans remarque bloquante
- `checkout/` · vu · 2026-11-03 · expliqué, « redis-le-moi » passé

## Termes acquis
- `PreToolUse`, `shop setting`, `merge queue`

## Écarts récurrents
- confond le diff de la branche avec le working tree · 2 fois · hooks (2026-11-13), checkout (2026-11-03)

## Préférences
- écrit les tests lui-même en pair
</sample_notes>

## Levels

- `vu`: explained once; the « redis-le-moi » was skipped, or there was none.
- `solide`: the user said it back right, wrote code there that passed review, or said « ça je connais ».
- `à revoir`: the gap was on the heart of the zone, even after the correction.

A zone is the smallest thing that was actually explained or written: a file, a folder, a flow by its entry point. One line per zone: update the line, never add a second one.

## Reading

- `solide`: do not explain it again; fold it, and say in one line that you do. First check it has not moved: `git -C <repo> log --oneline --since=<date> -- <path>`. With commits since, say how many and treat it as `vu`.
- `à revoir`, and any recurring gap the subject touches: lead with it, and aim the « redis-le-moi » or the next stop at it.
- `solide`, dated more than a month ago: still folded, but one « redis-le-moi » prompt goes to it. What was recalled once fades; a retrieval now and then is what keeps it, and the date is renewed when the answer holds.
- `Termes acquis`: use the term bare, no gloss.
- `Préférences`: propose them, never impose them.
- No file, or nothing on this zone: explain as for a newcomer to the zone, with no remark about it.

## Writing

- Facts that were observed, never a judgement of the person: what was said back right, what was corrected, what was written and how the review went.
- Two kinds of evidence weigh more than the rest: prior knowledge the user states, with how deep it goes, and a misconception that was corrected, which predicts where they will stumble next. Being explained something is not evidence: that is `vu`.
- After a « redis-le-moi »: the zone's level, today's date, one line of evidence; the terms glossed that the user then used rightly; a gap, new (`1 fois`) or seen again (count up, add where).
- After a pairing session: a zone where the user wrote a step that passed review with no blocking remark is `solide`; a review remark made twice is a recurring gap; a role the user took more than once is a preference.
- The user's word wins: « ça je connais » records `solide` with their word as the evidence, « oublie ça » removes the line, and an edit they made in the file is kept as it is.
- A gap that did not show the last three times its zone came up is removed.
- Keep it under 60 lines: merge zones of one folder that share a level, and drop the oldest `vu` lines first.
