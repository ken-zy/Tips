# AGENTS.md

## 仓库定位

这是 `ken-zy/Tips` 的 Hugo 博客仓库，也是网站源码的唯一事实来源。

- 生产地址：`https://ken-zy.github.io/Tips/`
- 默认分支：`master`
- Hugo 源码：`site/`
- 发布方式：GitHub Actions 构建并部署 GitHub Pages
- 主题：`site/themes/PaperMod` Git 子模块

不要把本仓库当成“提交生成后 HTML 的静态站点仓库”。根目录旧静态成品已经删除，今后的内容、配置和主题改动都必须从 `site/` 构建。

## 目录边界

| 路径 | 用途 | 修改规则 |
|---|---|---|
| `site/content/` | 文章和文章资源 | 日常内容修改的主要入口 |
| `site/archetypes/` | Hugo 内容模板 | 仅在明确修改模板时编辑 |
| `site/config.yml` | Hugo 站点配置 | 保持生产 `baseURL` 和 `/Tips/` 前缀 |
| `site/themes/PaperMod` | PaperMod gitlink | 不直接改主题文件，不擅自升级提交 |
| `.github/workflows/hugo.yml` | Pages 构建和部署 | 保持 PR 只构建、`master` 推送才部署 |
| `scripts/` | 固定版本安装与迁移验证 | 修改时必须同时验证本地和 CI 行为 |
| `docs/migration/legacy-public-paths.txt` | 73 个历史路径兼容基线 | 它是迁移基线，不是当前文章目录；不要因新增文章随意改动 |
| `docs/superpowers/`、`docs/reviews/` | 设计、计划和审查证据 | 重大迁移或发布机制变更时保留证据 |

根目录不得重新出现以下生成物：

- `404.html`、`index.html`、`index.xml`
- `robots.txt`、`sitemap.xml`
- `assets/`、`categories/`、`page/`、`post/`、`tags/`
- 任意根目录 `._*` AppleDouble 文件

`scripts/verify-repository-state.py` 会检查这条边界。不要绕过或削弱该检查。

## 生成文件规则

以下路径只能作为本地或 CI 临时产物，禁止提交：

- `site/public/`
- `site/resources/`
- `site/.hugo_build.lock`
- `.DS_Store` 和 `._*`

构建前可以删除 `site/public/` 和 `site/resources/`，但不要删除 `site/content/`、`site/config.yml` 或主题 gitlink。

## 内容编辑规则

1. 新文章和文章资源放在 `site/content/`，不要写入根目录 `post/`。
2. 路径和文件名区分大小写。现有 URL 中包含中英文混合和大小写混合名称，Linux CI 与 macOS 本地行为可能不同。
3. 保持现有文章的 Markdown 字节和换行语义。历史内容中的行尾空格可能表示 Markdown 强制换行，不要批量清理、格式化或重写。
4. 不做与当前任务无关的主题、SEO、URL、文章格式或内容重构。
5. `site/config.yml` 的生产地址必须保持为 `https://ken-zy.github.io/Tips/`。
6. 生成结果中不得出现旧主机 `jiadingyi.github.io`。
7. 新增正常内容不需要修改 73 路径迁移清单；只有明确改变历史兼容承诺时，才能在独立评审中修改该清单和验证器。

## 固定版本和供应链约束

以下版本是当前可复现构建的一部分，升级必须作为独立任务审查：

- Hugo Extended：`0.105.0`
- PaperMod gitlink：`efe4cb45161be836d602d5cd0f857e62661dae8b`
- GitHub Actions：全部使用经过审查的 40 字符 commit SHA

禁止把 Action SHA 改成 `main`、`master`、`vN` 等浮动引用。不要在内容修改中顺手升级 Hugo、PaperMod 或 Actions。

初始化主题：

```bash
git submodule update --init --recursive
test "$(git -C site/themes/PaperMod rev-parse HEAD)" = \
  "efe4cb45161be836d602d5cd0f857e62661dae8b"
```

`scripts/install-hugo.sh` 会下载指定平台的 Hugo 压缩包并核对 SHA-256。不要使用系统中碰巧存在的其他 Hugo 版本代替验收。

## 本地构建和验证

完整验证使用临时 Hugo 目录：

```bash
git submodule update --init --recursive

hugo_bin_dir="$(mktemp -d "${TMPDIR:-/tmp}/tips-hugo.XXXXXX")"
scripts/install-hugo.sh "$hugo_bin_dir"

rm -rf site/public site/resources
"$hugo_bin_dir/hugo" \
  --source site \
  --gc \
  --minify \
  --baseURL https://ken-zy.github.io/Tips/

python3 scripts/verify-migration.py \
  --manifest docs/migration/legacy-public-paths.txt \
  --generated site/public

python3 scripts/verify-repository-state.py
git check-ignore -q site/public/index.html
```

预期的迁移验证结果：

```text
verified 73 legacy paths; old host absent; new origin present
```

支持文件的附加检查：

```bash
bash -n scripts/install-hugo.sh
shellcheck scripts/install-hugo.sh

pycache_dir="$(mktemp -d "${TMPDIR:-/tmp}/tips-pycache.XXXXXX")"
PYTHONPYCACHEPREFIX="$pycache_dir" \
  python3 -m py_compile \
  scripts/verify-migration.py \
  scripts/verify-repository-state.py

git diff --check origin/master -- . \
  ':(exclude)site/content/**' \
  ':(exclude)site/archetypes/**'
```

不要对 `site/content/**` 或 `site/archetypes/**` 执行会要求清理历史行尾空格的全树格式化。

## GitHub Actions 和 Pages 语义

`.github/workflows/hugo.yml` 必须保持三种事件语义：

| 事件 | Build + Verify | Upload + Deploy |
|---|---:|---:|
| `pull_request` 到 `master` | 是 | 否 |
| `push` 到 `master` | 是 | 是 |
| `workflow_dispatch` | 是 | 是 |

PR 中 `deploy` 显示 `skipped` 是正确行为，不是失败。合并后必须检查由合并提交触发的 `push` 工作流，Build 和 Deploy 两个 job 都成功后，才能宣布上线完成。

Pages Source 必须保持 `GitHub Actions`。根目录已经没有静态成品，不能把 Pages 切回 `master / root` 并期待站点恢复。

## 生产验收

发布机制、Hugo 配置、主题或内容路径发生变化时，至少检查：

1. GitHub Actions Build 和 Deploy 都来自目标 `master` 提交。
2. Pages 状态为 `built`，`build_type` 为 `workflow`。
3. 首页、标签页、代表性文章、RSS、站点地图和静态资源返回正常内容。
4. `docs/migration/legacy-public-paths.txt` 中 73 个历史路径全部在新域名下可访问。
5. 响应内容不包含 `jiadingyi.github.io`，并包含新站地址。
6. 本地 `master`、`origin/master` 和部署使用的 SHA 一致。

不得仅凭首页返回 HTTP 200 就判定迁移或发布成功。

## 回滚原则

Pages 已经完全依赖 Actions artifact。出现发布问题时按以下顺序处理：

1. 重新运行最近一次成功或当前修复后的 Pages 工作流。
2. 回滚导致问题的 PR 或提交，让 `master` 重新触发部署。
3. 只有先恢复根目录旧静态成品后，才可能临时切回分支发布；不要直接切换 Pages Source。

任何回滚都禁止强制推送 `master`。

## Git 工作流

1. 禁止直接在 `master` 开发。
2. 新分支必须基于最新 `origin/master`：

   ```bash
   git fetch origin
   git checkout -b <type>/<topic> origin/master
   ```

3. 推送或创建 PR 前：

   ```bash
   git fetch origin
   git rebase origin/master
   test "$(git merge-base HEAD origin/master)" = "$(git rev-parse origin/master)"
   ```

4. rebase 后只能使用 `git push --force-with-lease`，禁止 `--force`。
5. 有开放 PR 时通过 GitHub merge commit 合并，不在本地直接合并到 `master`。
6. Commit 使用 `<type>(<scope>): <description>`，一 commit 一件事，不添加 AI/Claude 署名。
7. “提交”只表示 add + commit；只有用户明确说“推送”或流程明确要求创建 PR 时才 push。
8. 需要 worktree 时放在 `.worktrees/`；创建前必须用 `git check-ignore` 确认该目录已被忽略，不能让 worktree 内容污染仓库状态。

## 安全和范围控制

- 禁止读取、搜索或输出 `.env`、私钥、token、密码等真实敏感值。
- 安全扫描只报告可疑文件名，不打印匹配内容。
- 不新增依赖，除非任务明确需要且完成包身份、发布时间、传递依赖、生命周期脚本和完整性审计。
- 不修改仓库外的 `/Users/jdy/Documents/blog/Tips_hugo_source`；它是迁移后的临时备份，不是当前源码入口。
- 发现与当前任务无关的问题时只报告，不顺手重构或扩大范围。

## 完成检查清单

提交或 PR 前确认：

- [ ] 修改发生在正确的源码目录，没有根目录生成物。
- [ ] Hugo 0.105.0 构建成功。
- [ ] 73 路径迁移验证通过。
- [ ] 仓库状态验证通过。
- [ ] PaperMod gitlink 未意外变化。
- [ ] Action 引用仍为完整 SHA。
- [ ] `site/public/`、`site/resources/` 和构建锁文件未被跟踪。
- [ ] PR 的 Build 通过且 Deploy 跳过。
- [ ] 合并后自动 Build、Deploy 和生产路径验收通过。
- [ ] 本地与远程 `master` 一致，工作区干净。
