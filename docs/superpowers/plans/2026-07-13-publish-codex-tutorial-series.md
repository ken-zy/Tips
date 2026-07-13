# Codex Tutorial Series Publishing Implementation Plan

**Goal:** Publish the approved overview and six tutorials as seven linked Hugo posts while preserving the existing site and all legacy URLs.

**Architecture:** Copy only the public article bodies into `site/content/post/`, add Hugo front matter, and translate series links to Hugo `relref` references. The existing GitHub Actions workflow remains the sole publisher.

**Tech stack:** Markdown, Hugo Extended `0.105.0`, PaperMod, Git, GitHub Actions, GitHub Pages.

## Task 1: Establish the verified baseline

- Create `feat/publish-codex-tutorials` from the latest `origin/master` in an ignored `.worktrees/` directory.
- Initialize PaperMod and verify its exact gitlink.
- Run the pinned Hugo build, 73-path verifier, and repository-state verifier before edits.
- Audit time-sensitive OpenAI claims against official OpenAI sources.

## Task 2: Create the seven Hugo posts

- Copy the overview and six numbered public articles; do not copy `P-Codex使用教程.md`.
- Add front matter and remove duplicate H1 headings.
- Map all series navigation links to the seven stable Hugo routes with `relref`.
- Keep R2 image references and public source links.

## Task 3: Validate content and generated output

- Assert exactly seven new posts and seven generated routes.
- Reject remaining relative `.md` links or accidental live Obsidian wiki-links.
- Check remote image and documentation URLs.
- Run the pinned production build and existing migration/repository verifiers.
- Inspect representative generated HTML and local rendered pages.

## Task 4: Publish through GitHub

- Commit lifecycle documentation and content as separate concerns.
- Rebase onto the latest `origin/master`, verify the merge base, and push with lease protection if rewritten.
- Open a PR and require the PR Build job to pass while Deploy remains skipped.
- Merge through GitHub, then verify the `master` push Build and Deploy jobs, Pages workflow state, seven new routes, and legacy route matrix.
- Synchronize local `master` and remove the temporary worktree and branch.
