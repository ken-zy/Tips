# Codex Tutorial Series Publishing Design

## Goal

Publish the seven public Markdown articles from the Obsidian project `P-Codex使用教程` as a navigable Hugo series on `https://ken-zy.github.io/Tips/`.

## Scope

- Publish the overview and six numbered tutorials.
- Exclude the internal project-management note `P-Codex使用教程.md`.
- Leave the source Obsidian vault unchanged.
- Keep existing R2-hosted images and public reference links.
- Do not change Hugo, PaperMod, GitHub Actions, site configuration, or the 73-path migration baseline.

## Content Mapping

| Source article | Hugo source | Public route |
|---|---|---|
| `人人都会用Codex-概览.md` | `site/content/post/codex-tutorial-overview.md` | `/Tips/post/codex-tutorial-overview/` |
| `人人都会用Codex-梯子篇.md` | `site/content/post/codex-tutorial-network.md` | `/Tips/post/codex-tutorial-network/` |
| `人人都会用Codex-账号注册篇.md` | `site/content/post/codex-tutorial-account.md` | `/Tips/post/codex-tutorial-account/` |
| `人人都会用Codex-订阅与支付篇.md` | `site/content/post/codex-tutorial-subscription.md` | `/Tips/post/codex-tutorial-subscription/` |
| `人人都会用Codex-下载安装与登录篇.md` | `site/content/post/codex-tutorial-install.md` | `/Tips/post/codex-tutorial-install/` |
| `人人都会用Codex-Git与GitHub篇.md` | `site/content/post/codex-tutorial-git-github.md` | `/Tips/post/codex-tutorial-git-github/` |
| `人人都会用Codex-个人知识库篇.md` | `site/content/post/codex-tutorial-knowledge-base.md` | `/Tips/post/codex-tutorial-knowledge-base/` |

## Publishing Rules

1. Add Hugo front matter with a stable ASCII slug, publication date, `Codex` and `教程` tags, and `draft: false`.
2. Remove the source H1 because PaperMod renders the front-matter title.
3. Replace every series-relative `.md` link with Hugo `relref`, so links inherit the configured `/Tips/` base path and remain valid if the domain changes.
4. Keep literal Obsidian wiki-link examples inside code spans; they teach Markdown and are not website navigation.
5. Convert the Clash Verge release URL from inline code to a clickable link without changing the recommendation.
6. Preserve article wording unless an official-source fact audit identifies an error.

## Verification

- Build with the repository-pinned Hugo Extended `0.105.0` and PaperMod gitlink.
- Confirm the seven generated `index.html` routes exist and contain the expected titles.
- Confirm every `relref` resolves during the Hugo build.
- Check public Markdown for accidental non-code `[[...]]` links and remaining relative `.md` links.
- Confirm all R2 image URLs and referenced public URLs respond successfully or redirect normally.
- Run the existing 73-path migration verifier and repository-state verifier unchanged.
- On the PR, require Build success and Deploy skipped; after merge, require Build and Deploy success and verify all seven production routes.

## Rollback

If the merged content breaks production, revert the content PR on `master`. The revert triggers the same Pages workflow and restores the previous artifact; no generated output or theme/config rollback is required.
