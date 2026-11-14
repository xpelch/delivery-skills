"""Tests for pair-marker-check. Stdlib only: python3 hooks/test_pair_marker_check.py

Each test builds a throwaway git repo (with an origin for the branch cases), feeds the hook the JSON
Claude Code sends before a shell command, and checks whether it refuses.
"""

import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest

HOOK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pair-marker-check")
# Built from parts so this file never holds a marker the hook would refuse.
GATE = "GATE" + "(pair)"
TODO = "TODO" + "(pair)"
NAMED_GATE = "GATE" + "(sam)"


def git(repo, *args):
    subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", "-c", "core.hooksPath=/dev/null",
                    "-c", "core.autocrlf=false", *args], cwd=repo, check=True, capture_output=True)


def write(repo, path, text):
    full = os.path.join(repo, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def remove(folder):
    def writable(function, path, _):  # git marks its object files read-only, which stops rmtree on Windows
        os.chmod(path, stat.S_IWRITE)
        function(path)
    shutil.rmtree(folder, onerror=writable)


def hook(command, cwd, tool="Bash", owner=None):
    payload = json.dumps({"tool_name": tool, "tool_input": {"command": command}, "cwd": cwd})
    env = {name: value for name, value in os.environ.items() if name != "PAIR_MARKER_OWNER"}
    if owner:
        env["PAIR_MARKER_OWNER"] = owner
    proc = subprocess.run([sys.executable, HOOK], input=payload, capture_output=True, text=True, timeout=30,
                          env=env, encoding="utf-8")
    assert proc.returncode == 0, proc.stderr
    if not proc.stdout.strip():
        return None
    return json.loads(proc.stdout)["hookSpecificOutput"]


class CommitTest(unittest.TestCase):
    def setUp(self):
        self.repo = tempfile.mkdtemp()
        git(self.repo, "init", "-q")
        write(self.repo, "api/t.go", "package api\n")
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-qm", "init")

    def tearDown(self):
        remove(self.repo)

    def test_refuses_a_staged_gate_and_names_its_line(self):
        write(self.repo, "api/t.go", f"package api\n\n// {GATE}: condo list\n")
        git(self.repo, "add", ".")
        output = hook("git commit -m x", self.repo)
        self.assertEqual(output["permissionDecision"], "deny")
        self.assertIn("api/t.go:3", output["permissionDecisionReason"])

    def test_refuses_a_staged_todo(self):
        write(self.repo, "api/t.go", f"package api\n// {TODO}: write the body\n")
        git(self.repo, "add", ".")
        self.assertEqual(hook("git commit -m x", self.repo)["permissionDecision"], "deny")

    def test_ignores_an_unstaged_marker_on_a_plain_commit(self):
        write(self.repo, "api/t.go", f"package api\n// {GATE}\n")
        self.assertIsNone(hook("git commit -m x", self.repo))

    def test_refuses_an_unstaged_marker_when_the_command_stages_it(self):
        write(self.repo, "api/t.go", f"package api\n// {GATE}\n")
        self.assertEqual(hook("git add -A && git commit -m x", self.repo)["permissionDecision"], "deny")

    def test_refuses_an_untracked_file_staged_by_the_command(self):
        write(self.repo, "api/new.go", f"package api\n// {TODO}\n")
        output = hook("git add . && git commit -m x", self.repo)
        self.assertIn("api/new.go:2", output["permissionDecisionReason"])

    def test_follows_git_dash_c(self):
        write(self.repo, "api/t.go", f"package api\n// {GATE}\n")
        git(self.repo, "add", ".")
        repo = self.repo.replace(os.sep, "/")
        self.assertEqual(hook(f"git -C {repo} commit -m x", tempfile.gettempdir())["permissionDecision"], "deny")

    def test_follows_cd(self):
        write(self.repo, "api/t.go", f"package api\n// {GATE}\n")
        git(self.repo, "add", ".")
        repo = self.repo.replace(os.sep, "/")
        self.assertEqual(hook(f"cd {repo} && git commit -m x", tempfile.gettempdir())["permissionDecision"], "deny")

    def test_passes_a_commit_that_removes_a_marker(self):
        write(self.repo, "api/t.go", f"package api\n// {GATE}\n")
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-qm", "with marker")
        write(self.repo, "api/t.go", "package api\n")
        git(self.repo, "add", ".")
        self.assertIsNone(hook("git commit -m x", self.repo))

    def test_skips_markdown(self):
        write(self.repo, "docs/plan.md", f"- {GATE}: documented\n")
        git(self.repo, "add", ".")
        self.assertIsNone(hook("git commit -m x", self.repo))

    def test_ignores_another_owner_and_a_plain_todo(self):
        write(self.repo, "api/t.go", f"package api\n// TODO(jo): later\n// TODO: later\n// {NAMED_GATE}\n")
        git(self.repo, "add", ".")
        self.assertIsNone(hook("git commit -m x", self.repo))

    def test_refuses_the_owner_the_environment_names(self):
        write(self.repo, "api/t.go", f"package api\n// {NAMED_GATE}: threshold\n")
        git(self.repo, "add", ".")
        output = hook("git commit -m x", self.repo, owner="sam")
        self.assertEqual(output["permissionDecision"], "deny")
        self.assertIn("api/t.go:2", output["permissionDecisionReason"])

    def test_still_refuses_the_default_owner_when_the_environment_names_another(self):
        write(self.repo, "api/t.go", f"package api\n// {GATE}\n")
        git(self.repo, "add", ".")
        self.assertEqual(hook("git commit -m x", self.repo, owner="sam")["permissionDecision"], "deny")

    def test_refuses_a_commit_run_through_powershell(self):
        write(self.repo, "api/t.go", f"package api\n// {GATE}\n")
        self.assertEqual(hook("git add -A; git commit -m x", self.repo, tool="PowerShell")["permissionDecision"], "deny")

    def test_ignores_other_commands(self):
        write(self.repo, "api/t.go", f"package api\n// {GATE}\n")
        git(self.repo, "add", ".")
        self.assertIsNone(hook("git status", self.repo))


class BranchTest(unittest.TestCase):
    def setUp(self):
        self.origin = tempfile.mkdtemp()
        self.repo = tempfile.mkdtemp()
        git(self.origin, "init", "-q", "--bare", "-b", "main")
        git(self.repo, "init", "-q", "-b", "main")
        write(self.repo, "api/t.go", "package api\n")
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-qm", "init")
        git(self.repo, "remote", "add", "origin", self.origin)
        git(self.repo, "push", "-q", "origin", "main")
        git(self.repo, "fetch", "-q", "origin")
        git(self.repo, "checkout", "-qb", "feat/SHOP-1/x")

    def tearDown(self):
        remove(self.origin)
        remove(self.repo)

    def commit_marker(self):
        write(self.repo, "api/t.go", f"package api\n// {GATE}\n")
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-qm", "marker")

    def test_refuses_a_push_of_a_branch_that_adds_a_marker(self):
        self.commit_marker()
        self.assertEqual(hook("git push -u origin HEAD", self.repo)["permissionDecision"], "deny")

    def test_refuses_gh_pr_create_on_a_branch_that_adds_a_marker(self):
        self.commit_marker()
        self.assertEqual(hook("gh pr create --draft --title x --body y", self.repo)["permissionDecision"], "deny")

    def test_passes_a_push_once_the_marker_is_removed(self):
        self.commit_marker()
        write(self.repo, "api/t.go", "package api\n")
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-qm", "resolved")
        self.assertIsNone(hook("git push", self.repo))

    def test_passes_a_clean_branch(self):
        write(self.repo, "api/t.go", "package api\n\nconst x = 1\n")
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-qm", "clean")
        self.assertIsNone(hook("gh pr create --fill", self.repo))


if __name__ == "__main__":
    unittest.main()
