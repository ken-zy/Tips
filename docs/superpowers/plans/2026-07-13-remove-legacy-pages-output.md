# Remove Legacy Pages Output Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce the independent cleanup PR that removes the obsolete root-level generated website, prevents it from returning, and deploys Hugo automatically after future pushes to `master` while pull requests remain build-only.

**Architecture:** `site/` remains the only editable Hugo source and GitHub Actions remains the Pages publisher. A standard-library repository-state verifier guards the source/generated boundary, and the existing workflow gains a `push` trigger whose artifact upload and deploy jobs run for `push` and `workflow_dispatch` but never for `pull_request`.

**Tech Stack:** Git, Python 3 standard library, Hugo Extended `0.105.0`, GitHub Actions, GitHub Pages.

## Global Constraints

- Target repository: `/Users/jdy/Documents/blog/Tips`, GitHub `ken-zy/Tips`, default branch `master`.
- Start from deployed `origin/master` commit `c44082e388b4e0ebad51a3beab7b49988848fcae`.
- Phase C evidence: PR #1 merged; Pages `build_type` is `workflow`; run `29222816749` built and deployed successfully from `c44082e`; all 73 legacy paths returned HTTP 200; generated production output contained zero `jiadingyi.github.io` references.
- Delete only the root generated site: `404.html`, `index.html`, `index.xml`, `robots.txt`, `sitemap.xml`, `assets/`, `categories/`, `page/`, `post/`, `tags/`, and root `._*` files.
- Preserve `.github/`, `.gitignore`, `.gitmodules`, `docs/`, `scripts/`, `site/`, and the PaperMod gitlink at `efe4cb45161be836d602d5cd0f857e62661dae8b`.
- Pull requests build and verify only. `push` to `master` and explicit `workflow_dispatch` upload and deploy.
- Keep all existing Action references pinned to their reviewed 40-character SHAs; introduce no dependency.
- Keep Hugo Extended exactly `0.105.0`; do not upgrade Hugo, PaperMod, Actions, content, theme, or SEO behavior.
- Legacy Markdown remains byte-for-byte unchanged. Exclude `site/content/**` and `site/archetypes/**` from whitespace checks.
- Do not merge the cleanup PR during this execution lifecycle. After jdy authorizes merge, the merge commit's `push` run must deploy successfully and the 73-path production matrix must pass again.

---

### Task 1: Add a regression guard and remove root generated output

**Files:**
- Create: `scripts/verify-repository-state.py`
- Delete: `404.html`
- Delete: `index.html`
- Delete: `index.xml`
- Delete: `robots.txt`
- Delete: `sitemap.xml`
- Delete: `assets/**`
- Delete: `categories/**`
- Delete: `page/**`
- Delete: `post/**`
- Delete: `tags/**`
- Delete: root `._*`
- Preserve: `.github/**`, `.gitignore`, `.gitmodules`, `docs/**`, `scripts/**`, `site/**`

**Interfaces:**
- `python3 scripts/verify-repository-state.py` reads the Git index and exits nonzero if any forbidden root generated path is tracked or if a required source/workflow path is missing.
- The verifier prints only repository-relative filenames; it never reads secret-bearing files or file contents.

- [ ] **Step 1: Create the repository-state verifier before deleting production files**

Create `scripts/verify-repository-state.py` with these rules:

```python
#!/usr/bin/env python3
import subprocess


FORBIDDEN_FILES = {"404.html", "index.html", "index.xml", "robots.txt", "sitemap.xml"}
FORBIDDEN_PREFIXES = ("assets/", "categories/", "page/", "post/", "tags/")
REQUIRED_PATHS = {
    ".github/workflows/hugo.yml",
    ".gitignore",
    ".gitmodules",
    "docs/migration/legacy-public-paths.txt",
    "scripts/install-hugo.sh",
    "scripts/verify-migration.py",
    "site/config.yml",
    "site/themes/PaperMod",
}


def tracked_paths() -> set[str]:
    output = subprocess.check_output(["git", "ls-files", "-z"])
    return {item.decode() for item in output.split(b"\0") if item}


def main() -> None:
    tracked = tracked_paths()
    forbidden = sorted(
        path
        for path in tracked
        if path in FORBIDDEN_FILES
        or path.startswith("._")
        or path.startswith(FORBIDDEN_PREFIXES)
    )
    missing = sorted(REQUIRED_PATHS - tracked)

    if forbidden:
        raise SystemExit("legacy root output remains tracked:\n" + "\n".join(forbidden))
    if missing:
        raise SystemExit("required migration paths are missing:\n" + "\n".join(missing))

    print("verified repository cleanup: no legacy root output tracked; migration source retained")


if __name__ == "__main__":
    main()
```

Make it executable with `chmod +x scripts/verify-repository-state.py`.

- [ ] **Step 2: Run the verifier and observe the intended RED failure**

Run:

```bash
python3 scripts/verify-repository-state.py
```

Expected: nonzero exit with `legacy root output remains tracked`; the listed paths include the five root files, generated directories, and root AppleDouble files. This proves the guard detects the pre-cleanup state.

- [ ] **Step 3: Delete only the explicit legacy output allowlist**

Run:

```bash
git rm -r -- \
  404.html index.html index.xml robots.txt sitemap.xml \
  assets categories page post tags \
  ._*
```

Expected: only the paths listed in the task's Delete section enter deletion state. `site/`, `.github/`, `docs/`, and `scripts/` remain present.

- [ ] **Step 4: Run the verifier and repository boundary checks for GREEN**

Run:

```bash
python3 scripts/verify-repository-state.py
test -f .github/workflows/hugo.yml
test -f site/config.yml
test -f docs/migration/legacy-public-paths.txt
test "$(git ls-files -s site/themes/PaperMod | awk '{print $1, $2}')" = "160000 efe4cb45161be836d602d5cd0f857e62661dae8b"
test -z "$(git ls-files | rg '^(404\.html|index\.html|index\.xml|robots\.txt|sitemap\.xml|assets/|categories/|page/|post/|tags/|\._)')"
```

Expected: verifier and all assertions pass.

- [ ] **Step 5: Commit the cleanup boundary**

Run:

```bash
git add scripts/verify-repository-state.py
git commit -m "chore(site): remove legacy Pages output"
```

Expected: one commit containing only the verifier and explicit legacy-output deletions.

### Task 2: Enable stable automatic Pages deployment

**Files:**
- Modify: `.github/workflows/hugo.yml`

**Interfaces:**
- `pull_request` targeting `master`: checkout, repository-state verification, Hugo build, and migration verification; artifact upload and deploy are skipped.
- `push` to `master`: the same build gates, followed by Pages artifact upload and deploy.
- `workflow_dispatch`: the same build gates, followed by Pages artifact upload and deploy.

- [ ] **Step 1: Record the startup workflow's missing stable-state behavior**

Run before editing:

```bash
if rg -n '^  push:' .github/workflows/hugo.yml; then exit 1; fi
if rg -n "github.event_name != 'pull_request'" .github/workflows/hugo.yml; then exit 1; fi
```

Expected: both searches find nothing, confirming the current workflow does not auto-deploy `master` pushes.

- [ ] **Step 2: Apply the minimum stable-state workflow change**

Modify `.github/workflows/hugo.yml` as follows:

```yaml
on:
  pull_request:
    branches:
      - master
  push:
    branches:
      - master
  workflow_dispatch:
```

Add this build step after checkout:

```yaml
      - name: Verify repository source boundary
        run: python3 scripts/verify-repository-state.py
```

Change both current `github.event_name == 'workflow_dispatch'` conditions to:

```yaml
if: github.event_name != 'pull_request'
```

Do not change Action SHAs, permissions, environment, concurrency, Hugo version, build command, or migration verification.

- [ ] **Step 3: Verify stable-state event and permission invariants**

Run:

```bash
test "$(rg -c '^  push:' .github/workflows/hugo.yml)" = "1"
test "$(rg -c "github.event_name != 'pull_request'" .github/workflows/hugo.yml)" = "2"
test "$(rg -c "github.event_name == 'workflow_dispatch'" .github/workflows/hugo.yml)" = "0"
test "$(rg -c 'uses: actions/' .github/workflows/hugo.yml)" = "4"
test "$(rg -c 'uses: actions/[a-z-]+@[0-9a-f]{40}' .github/workflows/hugo.yml)" = "4"
rg -n 'pull_request:|push:|workflow_dispatch:|Verify repository source boundary|pages: write|id-token: write|cancel-in-progress: false' .github/workflows/hugo.yml
```

Expected: one `push` trigger, two non-PR deployment guards, no manual-only guard, four fully pinned official Actions, and all required permission/concurrency lines.

- [ ] **Step 4: Run the full local build and cleanup verification**

Run:

```bash
hugo_bin_dir="$(mktemp -d "${TMPDIR:-/tmp}/tips-cleanup-hugo.XXXXXX")"
scripts/install-hugo.sh "$hugo_bin_dir"
rm -rf site/public site/resources
"$hugo_bin_dir/hugo" --source site --gc --minify --baseURL https://ken-zy.github.io/Tips/
python3 scripts/verify-migration.py \
  --manifest docs/migration/legacy-public-paths.txt \
  --generated site/public
python3 scripts/verify-repository-state.py
git check-ignore -q site/public/index.html
git diff --check -- . ':(exclude)site/content/**' ':(exclude)site/archetypes/**'
bash -n scripts/install-hugo.sh
python3 -m py_compile scripts/verify-migration.py scripts/verify-repository-state.py
if command -v shellcheck >/dev/null 2>&1; then shellcheck scripts/install-hugo.sh; fi
```

Expected: Hugo `0.105.0` builds successfully; all 73 paths exist; the old host is absent and new origin present; repository boundary, ignore, whitespace, shell syntax, Python syntax, and available shell lint checks pass.

- [ ] **Step 5: Commit the stable workflow**

Run:

```bash
git add .github/workflows/hugo.yml
git commit -m "ci(site): deploy Pages from master pushes"
```

Expected: one commit containing only the workflow transition from startup to stable state.

### Task 3: Publish and review the cleanup PR

**Files:**
- Verify: all changes from Tasks 1-2
- Create automatically: `docs/reviews/claude-code/20260713/*-code-r1.md`

**Interfaces:**
- Consumes: the verified cleanup branch.
- Produces: an open cleanup PR with PR build verification and cross-model code review evidence.

- [ ] **Step 1: Rebase on the latest deployed default branch**

Run:

```bash
git fetch origin
git rebase origin/master
test "$(git merge-base HEAD origin/master)" = "$(git rev-parse origin/master)"
```

Expected: rebase succeeds and the branch contains the current remote `master` tip.

- [ ] **Step 2: Repeat the full Task 2 Step 4 verification after rebase**

Expected: every check passes on the exact commit that will be pushed.

- [ ] **Step 3: Push and create the cleanup PR**

Run:

```bash
git push -u origin feat/cleanup-legacy-pages
gh pr create \
  --base master \
  --head feat/cleanup-legacy-pages \
  --title "chore(site): remove legacy Pages output" \
  --body-file <generated PR body file outside the repository>
```

Expected: an open PR targets `master`; its `build` check runs, while `deploy` is skipped because the event is `pull_request`.

- [ ] **Step 4: Complete tmux cross-model code review**

Use Claude Code in explicit tmux pane `3:0.1`. Review against this plan and `origin/master`, apply only verified findings with confidence at least 70, and run another review round after every accepted modification.

Expected: Claude Code reports LGTM or all remaining findings are resolved/rejected through the lifecycle protocol; Codex performs the final safety-net review.

## Post-Merge Handoff

This execution stops with the cleanup PR open and reviewed. After jdy explicitly authorizes merge:

1. Confirm the cleanup PR build check passes and deploy is skipped.
2. Merge through GitHub with a merge commit and delete the remote feature branch.
3. Watch the resulting `push` workflow; require both Build and Deploy to succeed from the merge commit.
4. Re-run the 73-path production HTTP matrix and old-host scan.
5. Confirm Pages remains `build_type: workflow`, local `master` equals `origin/master`, and the worktree/feature branch are cleaned up.
6. If automatic deployment fails, rerun the last successful workflow first; if necessary, revert the cleanup PR to restore the legacy root artifacts. Never force-push `master`.
