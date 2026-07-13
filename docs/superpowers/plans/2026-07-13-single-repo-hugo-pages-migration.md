# Tips Single-Repo Hugo Pages Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce the first, reviewable migration PR that places the Hugo source in `site/`, pins the recoverable PaperMod replacement, validates all 73 legacy public paths, and adds a startup-state GitHub Pages workflow that builds PRs without deploying them.

**Architecture:** The public `ken-zy/Tips` repository remains the source of truth. Hugo source lives under `site/`; generated files stay temporary. A deterministic installer supplies Hugo Extended `0.105.0`, a standard-library verifier enforces host and path compatibility, and a SHA-pinned workflow builds every PR while deploying only an explicit `workflow_dispatch` after the repository owner switches Pages to GitHub Actions.

**Tech Stack:** Hugo Extended `0.105.0`, PaperMod git submodule, Bash, Python 3 standard library, GitHub Actions, GitHub Pages artifact deployment.

## Global Constraints

- Target repository: `/Users/jdy/Documents/blog/Tips`, GitHub `ken-zy/Tips`, default branch `master`.
- Source repository: `/Users/jdy/Documents/blog/Tips_hugo_source`, baseline `7c755e1510d7324f0fb72f24ff4dc7254e8bfd5f`.
- Target baseline when this plan was written: `d4d62e83699b31416ec079dc5a65ce157800fb8d`.
- Hugo Extended is exactly `0.105.0`; Linux SHA-256 is `3cd7b9d2fc3812b5d0a130b1735e5894b273210d6e7c03f68facad26b2d2e8a9`; macOS universal SHA-256 is `7d4189cefa61bb5a6d077880a1f7a6e18c5335a3ac469cc5a1e7ee7ce0512206`.
- PaperMod is exactly `efe4cb45161be836d602d5cd0f857e62661dae8b`; the unrecoverable source gitlink `c07d9ce608155dd1ade3c2828c28f98bee75a442` must not be copied.
- Source allowlist: only `archetypes/`, `content/`, and `config.yml`; exclude `public/`, `resources/`, `.hugo_build.lock`, `.git/`, `.DS_Store`, and every `._*` path.
- Legacy hostname `jiadingyi.github.io` must occur zero times in the production build. `https://ken-zy.github.io/Tips/` must occur at least once.
- The compatibility baseline contains exactly 73 legacy page/content-resource paths. Generated fingerprinted theme files under `assets/css/` and `assets/js/` and AppleDouble files are intentionally excluded.
- PR events build and verify only. Startup deployment is available only through `workflow_dispatch`; `push` deployment belongs to the later cleanup PR after the first production deployment succeeds.
- No secret value may be printed. Security scans report filenames only and stop before public migration if a high-signal match exists.
- No Hugo, PaperMod, Action, visual redesign, content-format, or SEO upgrade is included.
- Legacy Markdown is copied byte-for-byte. Its existing trailing spaces may encode Markdown hard line breaks, so whole-tree `git diff --check` must not be used to rewrite or reject allowlisted legacy content; verify copied trees with `diff`/`cmp` and run whitespace checks only on newly authored support files.
- The repository has no root `AGENTS.md`; reviews must record `no convention file available`.

## Dependency Admission Record

All workflow dependencies are official GitHub Actions, pinned to full SHAs, and were older than the 90-day new-dependency threshold on 2026-07-13:

| Action | Release | Published | Full SHA |
|---|---:|---:|---|
| `actions/checkout` | `v6.0.2` | 2026-01-09 | `de0fac2e4500dabe0009e67214ff5f5447ce83dd` |
| `actions/configure-pages` | `v6.0.0` | 2026-03-25 | `45bfe0192ca1faeb007ade9deae92b16b8254a0d` |
| `actions/upload-pages-artifact` | `v5.0.0` | 2026-04-10 | `fc324d3547104276b827a68afc52ff2a11cc49c9` |
| `actions/deploy-pages` | `v5.0.0` | 2026-03-25 | `cd2ce8fcbc39b97be8ca5fce6e763baed58fa128` |

`upload-pages-artifact@v5.0.0` is composite and invokes official `actions/upload-artifact@v7.0.0` pinned to `bbbca2ddaa5d8feaa63e36b76fdaad77386f024f` (published 2026-02-26). The JavaScript Actions ship precompiled `dist/` bundles; this workflow never runs `npm install`, so their repository `fsevents` optional install script is not executed. No workflow Action references an unpinned branch or floating tag.

## Execution Boundary

This plan produces the migration PR described by Spec Phase B and stops with that PR code-reviewed. The Pages Source switch, first production deployment, and cleanup PR are deliberately not executed before this branch passes Phase 4 Code Review. After this PR is reviewed and merged, create a second plan from the live deployment evidence for Spec Phases C and D; this preserves the required two-PR rollback boundary.

---

### Task 1: Establish the feature branch and legacy compatibility baseline

**Files:**
- Create: `docs/migration/legacy-public-paths.txt`
- Existing evidence: `docs/superpowers/specs/2026-07-13-single-repo-hugo-pages-migration-design.md`

**Interfaces:**
- Consumes: target root static files at baseline `d4d62e8`; source repo at `7c755e1`.
- Produces: a sorted, 73-line path manifest consumed by `scripts/verify-migration.py`.

- [ ] **Step 1: Rename the unpushed branch to the implementation branch and verify its base**

Run:

```bash
cd /Users/jdy/Documents/blog/Tips
git branch -m feat/consolidate-hugo-site
git fetch origin
test "$(git merge-base HEAD origin/master)" = "$(git rev-parse origin/master)"
git status --short --branch
```

Expected: branch is `feat/consolidate-hugo-site`; merge-base equals `origin/master`; only reviewed lifecycle documents under `docs/` are dirty/untracked.

- [ ] **Step 2: Commit the reviewed design, plan, and review artifacts**

Run:

```bash
git add \
  docs/superpowers/specs/2026-07-13-single-repo-hugo-pages-migration-design.md \
  docs/superpowers/plans/2026-07-13-single-repo-hugo-pages-migration.md \
  docs/reviews/claude-code/20260713
git commit -m "docs(site): finalize migration design and plan"
```

Expected: one documentation commit containing the post-review Spec, final plan, and Claude review artifacts.

- [ ] **Step 3: Re-verify immutable source and theme premises**

Run:

```bash
test "$(git -C /Users/jdy/Documents/blog/Tips_hugo_source rev-parse HEAD)" = "7c755e1510d7324f0fb72f24ff4dc7254e8bfd5f"
test "$(git -C /Users/jdy/Documents/blog/Tips_hugo_source status --porcelain)" = ""
test "$(gh api repos/adityatelange/hugo-PaperMod/commits/efe4cb45161be836d602d5cd0f857e62661dae8b --jq .sha)" = "efe4cb45161be836d602d5cd0f857e62661dae8b"
```

Expected: source SHA and clean status checks pass; the last command resolves the approved PaperMod commit.

- [ ] **Step 4: Scan the allowlisted source without printing values**

Run:

```bash
src=/Users/jdy/Documents/blog/Tips_hugo_source
find "$src/archetypes" "$src/content" -type f \( -name '.env' -o -name '.env.*' -o -iname '*secret*' -o -iname '*credential*' -o -iname '*private*key*' -o -iname '*.pem' -o -iname '*.p12' -o -iname '*.key' \) -print
rg -l --hidden --glob '!._*' --glob '!.env*' --glob '!*.min.js' --glob '!*.min.css' -- '(-----BEGIN (RSA |OPENSSH |EC )?PRIVATE KEY-----|AKIA[0-9A-Z]{16}|gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|xox[baprs]-[A-Za-z0-9-]{10,})' "$src/archetypes" "$src/content" "$src/config.yml"
```

Expected: both commands print no filenames. Any filename is a hard stop and must be reported without opening or printing the matched value.

- [ ] **Step 5: Generate the compatibility manifest mechanically**

Run:

```bash
mkdir -p docs/migration
git -c core.quotepath=false ls-files \
  | rg -v '^(docs/|assets/(css|js)/)|(^|/)\._' \
  | LC_ALL=C sort > docs/migration/legacy-public-paths.txt
test "$(wc -l < docs/migration/legacy-public-paths.txt | tr -d ' ')" = "73"
```

Expected: `docs/migration/legacy-public-paths.txt` contains exactly 73 sorted relative paths, including HTML/XML, `robots.txt`, article images, and downloadable article resources.

- [ ] **Step 6: Commit the baseline evidence**

```bash
git add docs/migration/legacy-public-paths.txt
git commit -m "chore(site): record legacy public path baseline"
```

Expected: one commit containing only the compatibility manifest.

### Task 2: Migrate the allowlisted Hugo source and recoverable theme

**Files:**
- Create: `.gitignore`
- Create: `.gitmodules`
- Create: `site/archetypes/default.md`
- Create: `site/config.yml`
- Create: `site/content/**`
- Create gitlink: `site/themes/PaperMod`

**Interfaces:**
- Consumes: source allowlist and approved PaperMod SHA.
- Produces: a self-contained Hugo source tree rooted at `site/`.

- [ ] **Step 1: Copy only allowlisted source paths**

Run:

```bash
mkdir -p site
rsync -a --exclude='._*' /Users/jdy/Documents/blog/Tips_hugo_source/archetypes/ site/archetypes/
rsync -a --exclude='._*' /Users/jdy/Documents/blog/Tips_hugo_source/content/ site/content/
cp /Users/jdy/Documents/blog/Tips_hugo_source/config.yml site/config.yml
```

Expected: `site/` contains `archetypes/`, `content/`, and `config.yml`, but no generated directories.

- [ ] **Step 2: Add and pin the PaperMod submodule**

Run:

```bash
git submodule add https://github.com/adityatelange/hugo-PaperMod.git site/themes/PaperMod
git -C site/themes/PaperMod fetch origin efe4cb45161be836d602d5cd0f857e62661dae8b
git -C site/themes/PaperMod checkout --detach efe4cb45161be836d602d5cd0f857e62661dae8b
test "$(git -C site/themes/PaperMod rev-parse HEAD)" = "efe4cb45161be836d602d5cd0f857e62661dae8b"
git config -f .gitmodules --get submodule.site/themes/PaperMod.path
```

Expected: the path output is `site/themes/PaperMod`; the gitlink points to `efe4cb45...`.

- [ ] **Step 3: Add generated-file ignores**

Create `.gitignore` with exactly:

```gitignore
.DS_Store
._*
/site/.hugo_build.lock
/site/public/
/site/resources/
```

- [ ] **Step 4: Verify the migrated boundary**

Run:

```bash
test ! -e site/public
test ! -e site/resources
test ! -e site/.hugo_build.lock
test -z "$(find site \( -name '.DS_Store' -o -name '._*' \) -print -quit)"
test "$(find site/archetypes -type f | wc -l | tr -d ' ')" = "1"
test "$(find site/content -type f | wc -l | tr -d ' ')" = "43"
diff -qr --exclude='._*' /Users/jdy/Documents/blog/Tips_hugo_source/archetypes site/archetypes
diff -qr --exclude='._*' /Users/jdy/Documents/blog/Tips_hugo_source/content site/content
cmp /Users/jdy/Documents/blog/Tips_hugo_source/config.yml site/config.yml
git diff --check -- . ':(exclude)site/content/**' ':(exclude)site/archetypes/**'
```

Expected: all tests pass; no forbidden generated or AppleDouble file is present.

- [ ] **Step 5: Commit the source migration**

```bash
git add .gitignore .gitmodules site
git commit -m "feat(site): migrate Hugo source into public repository"
```

Expected: the commit contains only source, configuration, ignore rules, and the pinned gitlink.

### Task 3: Add deterministic Hugo installation and migration verification

**Files:**
- Create: `scripts/install-hugo.sh`
- Create: `scripts/verify-migration.py`

**Interfaces:**
- `scripts/install-hugo.sh <target-dir>` produces `<target-dir>/hugo` at version `0.105.0` after SHA-256 verification.
- `scripts/verify-migration.py --manifest <file> --generated <dir>` exits 0 only when all 73 paths exist, `index.html` exists, the old host is absent, and the new host is present.

- [ ] **Step 1: Write the installer contract test and observe failure**

Run before creating the script:

```bash
bash scripts/install-hugo.sh 2>/dev/null
```

Expected: FAIL because `scripts/install-hugo.sh` does not exist.

- [ ] **Step 2: Create `scripts/install-hugo.sh`**

```bash
#!/usr/bin/env bash
set -euo pipefail

target_dir="${1:?usage: scripts/install-hugo.sh TARGET_DIR}"
version="0.105.0"

case "$(uname -s)-$(uname -m)" in
  Darwin-arm64|Darwin-x86_64)
    artifact="hugo_extended_${version}_darwin-universal.tar.gz"
    expected_sha="7d4189cefa61bb5a6d077880a1f7a6e18c5335a3ac469cc5a1e7ee7ce0512206"
    ;;
  Linux-x86_64)
    artifact="hugo_extended_${version}_linux-amd64.tar.gz"
    expected_sha="3cd7b9d2fc3812b5d0a130b1735e5894b273210d6e7c03f68facad26b2d2e8a9"
    ;;
  *)
    echo "unsupported platform: $(uname -s)-$(uname -m)" >&2
    exit 1
    ;;
esac

mkdir -p "$target_dir"
archive="$target_dir/$artifact"
url="https://github.com/gohugoio/hugo/releases/download/v${version}/${artifact}"
curl -fsSL --retry 3 --retry-all-errors -o "$archive" "$url"

if command -v sha256sum >/dev/null 2>&1; then
  actual_sha="$(sha256sum "$archive" | awk '{print $1}')"
else
  actual_sha="$(shasum -a 256 "$archive" | awk '{print $1}')"
fi

if [[ "$actual_sha" != "$expected_sha" ]]; then
  echo "Hugo checksum mismatch" >&2
  exit 1
fi

tar -xzf "$archive" -C "$target_dir" hugo
rm -f "$archive"
"$target_dir/hugo" version | grep -F "v${version}"
```

Make it executable:

```bash
chmod +x scripts/install-hugo.sh
```

- [ ] **Step 3: Write failing verifier fixtures**

Run:

```bash
fixture="$(mktemp -d)"
printf '%s\n' 'index.html' > "$fixture/manifest.txt"
python3 scripts/verify-migration.py --manifest "$fixture/manifest.txt" --generated "$fixture/generated"
```

Expected: FAIL because `scripts/verify-migration.py` does not exist.

- [ ] **Step 4: Create `scripts/verify-migration.py`**

```python
#!/usr/bin/env python3
import argparse
from pathlib import Path, PurePosixPath

OLD_HOST = b"jiadingyi.github.io"
NEW_ORIGIN = b"https://ken-zy.github.io/Tips/"


def fail(message: str) -> None:
    raise SystemExit(message)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--generated", required=True, type=Path)
    args = parser.parse_args()

    entries = [line.strip() for line in args.manifest.read_text().splitlines() if line.strip()]
    if len(entries) != 73:
        fail(f"expected 73 legacy paths, found {len(entries)}")

    invalid = [entry for entry in entries if PurePosixPath(entry).is_absolute() or ".." in PurePosixPath(entry).parts]
    if invalid:
        fail(f"invalid manifest paths: {invalid}")

    if not (args.generated / "index.html").is_file():
        fail("generated index.html is missing")

    missing = [entry for entry in entries if not (args.generated / entry).is_file()]
    if missing:
        fail("missing legacy paths:\n" + "\n".join(missing))

    old_host_files: list[str] = []
    new_origin_found = False
    for file_path in args.generated.rglob("*"):
        if not file_path.is_file():
            continue
        data = file_path.read_bytes()
        if OLD_HOST in data:
            old_host_files.append(str(file_path.relative_to(args.generated)))
        if NEW_ORIGIN in data:
            new_origin_found = True

    if old_host_files:
        fail("old hostname remains in:\n" + "\n".join(old_host_files))
    if not new_origin_found:
        fail("new origin was not found in generated output")

    print(f"verified {len(entries)} legacy paths; old host absent; new origin present")


if __name__ == "__main__":
    main()
```

- [ ] **Step 5: Run syntax and negative-path tests**

```bash
bash -n scripts/install-hugo.sh
python3 -m py_compile scripts/verify-migration.py
fixture="$(mktemp -d)"
mkdir -p "$fixture/generated"
printf '%s\n' 'index.html' > "$fixture/manifest.txt"
printf '%s\n' '<html>https://jiadingyi.github.io/Tips/</html>' > "$fixture/generated/index.html"
if python3 scripts/verify-migration.py --manifest "$fixture/manifest.txt" --generated "$fixture/generated"; then exit 1; fi
```

Expected: syntax checks pass; the final verifier invocation fails.

- [ ] **Step 6: Commit validation tooling**

```bash
git add scripts/install-hugo.sh scripts/verify-migration.py
git commit -m "test(site): add deterministic migration verification"
```

### Task 4: Add the startup-state GitHub Pages workflow

**Files:**
- Create: `.github/workflows/hugo.yml`

**Interfaces:**
- Consumes: `site/`, installer, verifier, legacy manifest.
- Produces: PR build verification and manual-only Pages artifact deployment.

- [ ] **Step 1: Create `.github/workflows/hugo.yml`**

```yaml
name: Hugo Pages

on:
  pull_request:
    branches:
      - master
  workflow_dispatch:

permissions:
  contents: read

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd # v6.0.2
        with:
          fetch-depth: 0
          persist-credentials: false
          submodules: recursive

      - name: Configure Pages
        id: pages
        uses: actions/configure-pages@45bfe0192ca1faeb007ade9deae92b16b8254a0d # v6.0.0

      - name: Install Hugo Extended 0.105.0
        run: scripts/install-hugo.sh "$RUNNER_TEMP/hugo-bin"

      - name: Build site
        working-directory: site
        env:
          HUGO_ENVIRONMENT: production
          HUGO_ENV: production
        run: >-
          "$RUNNER_TEMP/hugo-bin/hugo"
          --gc
          --minify
          --baseURL "${{ steps.pages.outputs.base_url }}/"

      - name: Verify migrated output
        run: >-
          python3 scripts/verify-migration.py
          --manifest docs/migration/legacy-public-paths.txt
          --generated site/public

      - name: Upload Pages artifact
        if: github.event_name == 'workflow_dispatch'
        uses: actions/upload-pages-artifact@fc324d3547104276b827a68afc52ff2a11cc49c9 # v5.0.0
        with:
          path: site/public

  deploy:
    if: github.event_name == 'workflow_dispatch'
    needs: build
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pages: write
      id-token: write
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    concurrency:
      group: pages
      cancel-in-progress: false
    steps:
      - name: Deploy Pages artifact
        id: deployment
        uses: actions/deploy-pages@cd2ce8fcbc39b97be8ca5fce6e763baed58fa128 # v5.0.0
```

- [ ] **Step 2: Verify trigger and dependency pin invariants**

Run:

```bash
rg -n '^  push:' .github/workflows/hugo.yml && exit 1 || true
test "$(rg -c 'uses: actions/' .github/workflows/hugo.yml)" = "4"
test "$(rg -c 'uses: actions/[a-z-]+@[0-9a-f]{40}' .github/workflows/hugo.yml)" = "4"
rg -n 'workflow_dispatch|pull_request|submodules: recursive|pages: write|id-token: write|cancel-in-progress: false' .github/workflows/hugo.yml
```

Expected: no `push` trigger; exactly four fully pinned official Action references; all required trigger, submodule, permission, and concurrency lines are present.

- [ ] **Step 3: Reconfirm pinned Action identities and embedded dependency**

Run:

```bash
git ls-remote https://github.com/actions/checkout.git refs/tags/v6.0.2
git ls-remote https://github.com/actions/configure-pages.git refs/tags/v6.0.0
git ls-remote https://github.com/actions/upload-pages-artifact.git refs/tags/v5.0.0
git ls-remote https://github.com/actions/deploy-pages.git refs/tags/v5.0.0
git ls-remote https://github.com/actions/upload-artifact.git refs/tags/v7.0.0
```

Expected: the five outputs equal the SHAs recorded in `Dependency Admission Record`.

- [ ] **Step 4: Commit the startup workflow**

```bash
git add .github/workflows/hugo.yml
git commit -m "ci(site): add SHA-pinned Hugo Pages workflow"
```

### Task 5: Run full local and visual migration verification

**Files:**
- Verify: all files added by Tasks 1–4
- Temporary only: Hugo binary, build output, HTTP server roots, screenshots under `${TMPDIR}`

**Interfaces:**
- Consumes: complete migration branch.
- Produces: evidence that the branch is ready for Phase 4 Code Review and PR creation.

- [ ] **Step 1: Install the verified local Hugo binary and build production output**

Run:

```bash
hugo_bin_dir="$(mktemp -d "${TMPDIR:-/tmp}/tips-hugo-bin.XXXXXX")"
scripts/install-hugo.sh "$hugo_bin_dir"
rm -rf site/public site/resources
"$hugo_bin_dir/hugo" --source site --gc --minify --baseURL https://ken-zy.github.io/Tips/
```

Expected: Hugo reports `v0.105.0`; build exits 0 and creates `site/public/index.html`.

- [ ] **Step 2: Run compatibility and repository checks**

```bash
python3 scripts/verify-migration.py \
  --manifest docs/migration/legacy-public-paths.txt \
  --generated site/public
git check-ignore -q site/public/index.html
for generated in site/resources site/.hugo_build.lock; do
  if [[ -e "$generated" ]]; then git check-ignore -q "$generated"; fi
done
git diff --check -- . ':(exclude)site/content/**' ':(exclude)site/archetypes/**'
git submodule status
```

Expected verifier output: `verified 73 legacy paths; old host absent; new origin present`. Generated directories are ignored; submodule output begins with one space followed by `efe4cb45161be836d602d5cd0f857e62661dae8b`.

- [ ] **Step 3: Compare representative pages against the committed root baseline**

Start two local servers:

```bash
old_parent=/Users/jdy/Documents/blog
new_parent="$(mktemp -d "${TMPDIR:-/tmp}/tips-visual-new.XXXXXX")"
ln -s /Users/jdy/Documents/blog/Tips/site/public "$new_parent/Tips"
python3 -m http.server 4173 --bind 127.0.0.1 --directory "$old_parent" >"$new_parent/old-server.log" 2>&1 &
old_server_pid=$!
python3 -m http.server 4174 --bind 127.0.0.1 --directory "$new_parent" >"$new_parent/new-server.log" 2>&1 &
new_server_pid=$!
trap 'kill "$old_server_pid" "$new_server_pid" 2>/dev/null || true' EXIT
curl -fsS http://127.0.0.1:4173/Tips/ >/dev/null
curl -fsS http://127.0.0.1:4174/Tips/ >/dev/null
```

Using the browser validation workflow, compare these route pairs at desktop `1440×900` and mobile `390×844`, in both light and dark mode:

```text
http://127.0.0.1:4173/Tips/
http://127.0.0.1:4174/Tips/

http://127.0.0.1:4173/Tips/tags/swift/
http://127.0.0.1:4174/Tips/tags/swift/

http://127.0.0.1:4173/Tips/post/swift中的属性/
http://127.0.0.1:4174/Tips/post/swift中的属性/

http://127.0.0.1:4173/Tips/post/玩转stablediffusion/
http://127.0.0.1:4174/Tips/post/玩转stablediffusion/
```

Expected: layout structure, readability, navigation, images, code blocks, and light/dark behavior match. Hostname targets and copyright year are accepted. Any other visible difference follows the Spec D5 adjudication path and can trigger the single user-premise escalation before Pages Source changes.

- [ ] **Step 4: Rebase and push for Phase 4**

```bash
git fetch origin
git rebase origin/master
test "$(git merge-base HEAD origin/master)" = "$(git rev-parse origin/master)"
git status --short --branch
git push -u origin feat/consolidate-hugo-site
```

Expected: rebase succeeds, branch is based on current `origin/master`, working tree contains no uncommitted implementation changes, and the remote feature branch exists. Phase 4 creates the PR automatically and reviews the full diff before any merge or Pages setting change.

## Post-Review Handoff Gate

After Phase 4 reports LGTM and the PR is merged, the next lifecycle must start from updated `origin/master` and cover, in order:

1. Switch `ken-zy/Tips` Pages `build_type` from `legacy` to `workflow`.
2. Trigger `hugo.yml` manually and verify Build + Deploy and the production route matrix.
3. If deployment fails, restore `master / root` legacy Pages while root artifacts still exist.
4. Create `cleanup/remove-legacy-pages-output` from the deployed `origin/master`.
5. Delete only the root generated files listed in Spec Phase D.
6. Add `push: master` to the workflow and enable artifact/deploy on `push` or `workflow_dispatch`, while PRs remain build-only.
7. Review and merge the cleanup PR, then verify the automatic production deployment and clean Git state.
