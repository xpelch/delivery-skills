---
name: pr-screenshots
description: Captures screenshots of the running app and puts them into a GitHub pull request description - captured in a browser the agent drives, uploaded through a PR comment box without posting it, and written into the body with gh. Use when the user asks for photos, captures or screenshots in a PR, or to show a UI change in a PR body. Even when casual - "mets des captures dans la PR", "ajoute les screenshots", "photos dans la PR", "montre le changement UI dans la PR". Writing the rest of the PR body belongs to pr.
compatibility: Works in Claude Code and Codex. Needs gh, and a browser the agent can drive (Claude in Chrome, a Playwright or Chrome DevTools MCP, or the agent's own browser); the upload needs that browser signed in to GitHub, otherwise the user drags the saved images in.
allowed-tools: Bash(gh pr view *), Bash(gh pr edit *)
---

# Screenshots in a pull request description

Capture the app's screens, upload them to GitHub, and write them into the PR description with `gh`.

`gh` cannot upload images, so the images reach GitHub through a comment box in a browser signed in as the user, and the **description** is written with `gh`. The comment box is only a host for the upload: nothing is ever posted as a comment. Say so to the user before you start; otherwise the upload looks like a comment being written.

## Which browser

Use what the agent has, in this order:

1. **A browser signed in to GitHub as the user** (Claude Code's Claude in Chrome; a Chrome DevTools or Playwright MCP attached to the user's own browser profile): captures and upload both happen there.
2. **A browser the agent drives but that is not signed in** (a headless Playwright, the agent's built-in browser): capture there, save the images, then hand the upload to the user (step 2's fallback).
3. **No browser at all**: ask the user for the captures, or say which states to capture, then go to step 3 with the URLs they paste.

## Steps

1. **Capture**
   - Size the viewport to 1280×900 so the page lays out as on a laptop, navigate, wait for the data.
   - Capture the content region (drop the side navigation) and save each PNG to a temp folder with a name that says what it shows (`invoice-reminder-delay.png`).
   - Keep round trips low: read what a dropdown or list shows with one script call (`[...document.querySelectorAll('[role="option"]')].map(o => o.textContent)`) rather than a screenshot per check.
   - Close an unsaved form through its Cancel button (and Discard), so no draft is left in the app.

   Done when every screenshot the user asked for exists on disk and shows the state the PR describes.

2. **Upload**, in the signed-in browser:
   - Open any one PR of the set and find the file input of the **new comment** box at the bottom (`input[type=file]` inside the new-comment form).
   - Upload all the images in one call (the browser tool's file upload), wait ~6 s, then read the textarea: each image became `<img width=… alt=… src="https://github.com/user-attachments/assets/…" />`.
   - Empty that textarea (set its value to `""` and dispatch `input`), so no draft lingers. Never click "Comment".

   **Fallback** without a signed-in browser: give the user the saved files and ask them to drag them into the PR's comment box and paste back the `<img …>` lines GitHub writes (without posting), or to drop them straight into the description.

   Done when you hold one `user-attachments` URL per image and the comment box is empty.

3. **Write the description** with `gh pr edit <n> -R <repo> --body-file <file>`:
   - Read the current body (`gh pr view --json body`) and insert a section (for example `## Tested locally`: what was set up, what was entered, what came back) before the repo template's first checklist section (the body follows the `pr` skill's format), never replacing what is there. Add no attribution line.
   - Use `<img width="446" alt="<what it shows>" src="<url>" />`. One uploaded URL can go into several PRs.

   Done when every target PR body contains its `user-attachments` URLs.

4. **Verify**: for each PR, `gh pr view --json body,comments` shows the image in the body and the last comment unchanged.
