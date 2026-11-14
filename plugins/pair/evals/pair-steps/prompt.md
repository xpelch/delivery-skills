---
description: With the overview already agreed, a plumbing step is committed and the decision step stops uncommitted with a pair marker. Needs Bash, so a sandbox (macOS, Linux or WSL2).
model: sonnet
max_turns: 60
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

on code ça ensemble : le frais ne doit jamais descendre sous un plancher. J'ai déjà validé ce plan, pars directement de l'étape 1 sans me redemander : 1. plomberie : `total()` a un test qui couvre un petit montant (aucun changement de comportement). 2. ⛔ `fee_for` applique le plancher `settings.FEE_FLOOR` ; la décision à valider : le plancher s'applique aussi à un montant de 0. 3. plomberie : cas limites. Mon dossier de plans est plans/, dans ce dossier de travail. Pas d'éditeur ici. Les tests : `python3 -m unittest`.
