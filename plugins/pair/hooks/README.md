# Hooks

The hooks the plugin runs, registered in `hooks.json`. Each one is a stdlib-only Python script that reads the hook JSON on stdin, never fails the tool call (an error means silence), and refuses only through `hookSpecificOutput`.

| Hook | Event | What it does | Depends on |
|---|---|---|---|
| `hooks/pair-marker-check` | PreToolUse, Bash and PowerShell | Refuses a `git commit` whose added lines hold one of the `pair` skill's markers (`GATE(pair)`, `TODO(pair)`), and a `git push` or `gh pr create` whose branch adds one since the default branch. Names each file:line; Markdown is skipped. | `git`, Python 3 |

Handlers carry an `if` rule (`Bash(git *)`, `Bash(gh pr *)`) so the script isn't started for other commands; the script still re-checks its input. `hooks/run` starts it with `python3`, or `python` on a Windows machine where `python3` is the Microsoft Store stub.

## The marker owner

The `pair` skill writes `GATE(pair)` and `TODO(pair)`. To use your own name instead (`GATE(sam)`), set `PAIR_MARKER_OWNER=sam` where both the agent and the hook see it, for example in `~/.claude/settings.json`:

```json
{ "env": { "PAIR_MARKER_OWNER": "sam" } }
```

The hook always refuses the `pair` owner too. A plain `TODO:` and another person's `TODO(name)` pass.

## Using it without the plugin

The script is self-contained and works in any repo.

1. Copy `pair-marker-check` and `run` (and `test_pair_marker_check.py`) into the repo's `.claude/hooks/`.
2. Register it in the repo's `.claude/settings.json`:

   ```json
   {
     "hooks": {
       "PreToolUse": [
         {
           "matcher": "Bash",
           "hooks": [
             { "type": "command", "if": "Bash(git *)", "command": "sh \"$CLAUDE_PROJECT_DIR/.claude/hooks/run\" pair-marker-check", "timeout": 30 },
             { "type": "command", "if": "Bash(gh pr *)", "command": "sh \"$CLAUDE_PROJECT_DIR/.claude/hooks/run\" pair-marker-check", "timeout": 30 }
           ]
         }
       ]
     }
   }
   ```

3. Run its tests from the repo root: `python3 .claude/hooks/test_pair_marker_check.py`.

## Adding a hook

Put the script in `hooks/`, keep it stdlib-only with a docstring saying what it refuses and how to share it, add a `test_*.py` that drives it through stdin, register it in `hooks.json` through `hooks/run`, and add its row to the table. A hook that only makes sense for one project belongs in that project's `.claude/hooks/`, not here.
