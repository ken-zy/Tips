# Tips 单仓库 Hugo Pages 迁移设计

## 1. 状态

- 设计状态：已确认
- 设计日期：2026-07-13
- 目标仓库：`ken-zy/Tips`
- 迁移来源：`ken-zy/Tips_hugo_source`
- 发布地址：`https://ken-zy.github.io/Tips/`

## 2. 背景

当前网站由两个仓库共同维护：

| 仓库 | 可见性 | 当前职责 | 基线 |
|---|---|---|---|
| `ken-zy/Tips_hugo_source` | Private | 保存 Hugo 源码，同时重复保存 `public/` 生成结果 | `master` at `7c755e1510d7324f0fb72f24ff4dc7254e8bfd5f` |
| `ken-zy/Tips` | Public | 保存 Hugo 生成后的 HTML、CSS、RSS 和站点地图，并由 GitHub Pages 发布 | `master` at `d4d62e83699b31416ec079dc5a65ce157800fb8d` |

现有流程需要在源码仓库生成网页，再把结果同步到公开仓库。它带来三个问题：

1. 同一份生成结果被两个仓库重复保存。
2. 每次发布需要分别提交和同步，容易漏文件或出现版本不一致。
3. `Tips_hugo_source` 中混有 `public/`、`resources/`、`.hugo_build.lock` 和 macOS `._*` 文件，源码与生成物边界不清晰。

`Tips_hugo_source/config.yml` 的 `baseURL` 已修正为 `https://ken-zy.github.io/Tips/`，但线上网站只有在重新构建并部署后才会使用新地址。

当前生成结果仍引用 `https://jiadingyi.github.io/Tips/`。该旧主机现在返回 404，且不跳转到新主机。本次迁移负责把旧站点的全部内容和路径迁移到 `https://ken-zy.github.io/Tips/`，但不承诺旧主机继续响应或提供跨域名跳转。

## 3. 目标

迁移完成后，只使用公开仓库 `ken-zy/Tips` 维护和发布网站：

1. Hugo 源码、文章、主题引用和发布工作流保存在同一个仓库。
2. Pull Request 只执行构建验证，不修改线上网站。
3. `master` 更新后，由 GitHub Actions 自动构建并部署到 GitHub Pages。
4. Hugo 的 `public/` 目录只作为临时构建产物，不进入 Git 历史。
5. 现有文章、标签、RSS、站点地图和静态资源全部迁移到新域名，并在 `https://ken-zy.github.io/Tips/` 下保持原有路径或提供站内别名跳转。
6. 迁移期间保留可快速恢复到旧发布方式的路径，避免网站中断。

## 4. 非目标

本次迁移不包括：

- 发布 Codex 教程正文或 PDF。
- 升级 PaperMod 主题。
- 升级 Hugo 内容格式或重写旧文章。
- 调整网站视觉、导航、评论、统计或 SEO 文案。
- 删除或归档 `Tips_hugo_source` 仓库。
- 引入自定义域名。

Codex 教程发布将在单仓库迁移完成并稳定后，使用独立功能分支处理。

## 5. 核心决策

### D1：`Tips` 成为唯一维护仓库

`ken-zy/Tips` 继续保持公开，保留现有仓库名和 GitHub Pages 地址。Hugo 源码从 `Tips_hugo_source` 迁入该仓库。

### D2：Hugo 源码放在 `site/`

迁移后的目录结构为：

```text
Tips/
├── .github/
│   └── workflows/
│       └── hugo.yml
├── .gitignore
├── .gitmodules
├── docs/
│   └── superpowers/
│       └── specs/
├── site/
│   ├── archetypes/
│   ├── content/
│   ├── themes/
│   │   └── PaperMod/
│   └── config.yml
```

选择 `site/` 而不是直接放在仓库根目录，有两个原因：

1. 迁移第一阶段可以保留根目录现有网页成品，GitHub Pages 继续按旧方式提供服务。
2. Hugo 源码与仓库级文件、迁移文档和工作流边界清晰。

### D3：使用 GitHub Actions Pages artifact 发布

GitHub Pages 发布源从 `master / 根目录` 切换为 `GitHub Actions`。工作流在运行时生成 `site/public/`，将其作为 Pages artifact 上传并部署，不创建或维护 `gh-pages` 分支。

### D4：迁移分两个 PR 完成

为避免切换发布源时失去回滚路径，迁移分为两个独立 PR：

1. **迁移 PR**：添加 `site/` 源码、主题子模块、忽略规则和工作流，保留根目录旧网页成品。
2. **清理 PR**：Actions 部署验证通过后，删除根目录旧网页成品和 macOS 元数据文件。

### D5：第一次迁移保持旧构建行为

第一次迁移固定使用 Hugo Extended `0.105.0`，与当前线上网页的生成器版本一致。源码仓库记录的 PaperMod gitlink `c07d9ce608155dd1ade3c2828c28f98bee75a442` 已无法从官方上游获取，也没有本地对象可恢复，因此迁移固定使用官方仍可获取的提交 `efe4cb45161be836d602d5cd0f857e62661dae8b`。该提交是源码仓库 2023-10-08 更新主题前最接近的官方可达提交；使用 Hugo Extended `0.105.0` 的临时构建已成功，并生成全部 73 个需要保留的旧页面和内容资源路径。

73 个路径只能证明内容和 URL 完整，不能证明主题渲染一致。根目录当前静态网页作为替代主题的视觉基线；迁移发布前必须对代表性模板做同视口、同明暗主题对照，确认布局、字体、间距、颜色、图片、代码块和交互一致。链接主机从 `jiadingyi.github.io` 变为 `ken-zy.github.io`，以及构建时间导致的版权年份变化，可以直接接受。

发现其他可见差异时，先修复能够在不扩大迁移范围的前提下修复的问题并重新对照。仍然存在但不改变布局结构、内容可读性、导航交互或明暗主题行为的纯装饰差异，必须记录具体页面、截图和原因，并由 jdy 在切换 Pages Source 前显式接受；未获接受不得发布。影响布局、可读性或交互的实质差异始终阻断迁移，必须继续恢复主题行为或重新修订设计。

本次提交替代属于不可恢复 gitlink 的迁移修复，不视为主题升级。除此之外，Hugo 或 PaperMod 的升级属于后续独立任务，不能混入迁移 PR。

### D6：供应链依赖必须固定

工作流只使用官方 GitHub Actions：

- `actions/checkout`
- `actions/configure-pages`
- `actions/upload-pages-artifact`
- `actions/deploy-pages`

实现时必须：

1. 核对 Action 所属官方仓库和目标提交。
2. 选择满足仓库依赖观察期要求的稳定版本。
3. 使用完整 commit SHA 固定 Action，不使用 `main`、`master` 或 `latest`。
4. Hugo Extended 固定为 `0.105.0`，从 Hugo 官方发布页下载，并验证官方 SHA-256 校验值后安装。
5. 不引入第三方 Hugo 安装 Action。

## 6. 迁移文件边界

### 6.1 允许迁移

从 `Tips_hugo_source` 复制到 `Tips` 的内容仅限：

| 来源 | 目标 | 说明 |
|---|---|---|
| `archetypes/` | `site/archetypes/` | Hugo 内容模板 |
| `content/` | `site/content/` | 文章 Markdown 和文章资源 |
| `config.yml` | `site/config.yml` | Hugo 配置，保留已修正的 `baseURL` |
| `themes/PaperMod` gitlink | `site/themes/PaperMod` gitlink | 不复制失效 gitlink；改为固定 D5 选定的官方可达提交 `efe4cb45161be836d602d5cd0f857e62661dae8b` |

目标仓库根目录重新创建 `.gitmodules`，子模块路径必须是 `site/themes/PaperMod`。不能直接复制旧 `.gitmodules`，因为旧路径是 `themes/PaperMod`。

### 6.2 禁止迁移

以下内容不得进入目标仓库：

- `Tips_hugo_source/public/`
- `Tips_hugo_source/resources/`
- `Tips_hugo_source/.hugo_build.lock`
- 任意 `.git/`
- 任意 `.DS_Store`
- 任意以 `._` 开头的 AppleDouble 文件
- 密码、密钥、令牌、账号信息或私人内容

迁移前先做文件名和内容模式检查。检查敏感信息时不输出任何真实密钥值；发现疑似敏感文件立即停止迁移并报告。

### 6.3 忽略规则

目标仓库根目录 `.gitignore` 至少覆盖：

```gitignore
.DS_Store
._*
/site/.hugo_build.lock
/site/public/
/site/resources/
```

## 7. 自动构建与部署设计

工作流文件为 `.github/workflows/hugo.yml`。

### 7.1 触发条件

工作流分为启动状态和稳定状态：

**启动状态（迁移 PR）：**

- Pull Request 指向 `master`：只构建和验证，不部署。
- `workflow_dispatch`：在切换 Pages Source 后，人工触发第一次构建和部署。
- 暂不响应 Push 到 `master`，避免 Pages 仍处于旧发布模式时首次合并产生部署失败。

**稳定状态（清理 PR 合并后）：**

- Pull Request 指向 `master`：只构建和验证，不部署。
- Push 到 `master`：构建并部署。
- `workflow_dispatch`：允许手动重新部署当前 `master`。

### 7.2 Build job

Build job 必须：

1. 检出当前提交并递归初始化子模块。
2. 安装并校验 Hugo Extended `0.105.0`。
3. 在 `site/` 中运行生产构建。
4. 使用 GitHub Pages 提供的站点基地址，确保项目站点 `/Tips/` 前缀正确。
5. 检查生成目录存在且包含 `index.html`。
6. 检查生成结果不包含 `jiadingyi.github.io`。
7. 检查生成结果包含 `https://ken-zy.github.io/Tips/`。
8. 仅在允许部署的事件中上传 `site/public/` Pages artifact。

Build job 只需要 `contents: read` 权限。

### 7.3 Deploy job

Deploy job 必须：

- 启动状态仅在人工触发时运行；稳定状态在 `master` push 或人工触发时运行。
- 依赖成功的 Build job。
- 使用 `github-pages` environment。
- 只授予 `pages: write` 和 `id-token: write`，同时保留所需的最小读取权限。
- 使用上传的 Pages artifact 部署，不向仓库写入生成文件。

### 7.4 并发控制

同一时间只允许一个 Pages 部署。新提交可以替换尚未开始的旧部署，但不能中断已经开始的生产部署。

## 8. 数据流

```mermaid
flowchart LR
    A[修改 site/content Markdown] --> B[创建 Pull Request]
    B --> C[Actions 构建验证]
    C -->|失败| D[修复后重新验证]
    C -->|通过| E[合并到 master]
    E --> F[Actions 生产构建]
    F --> G[上传 Pages artifact]
    G --> H[部署到 GitHub Pages]
    H --> I[验证线上网址]
```

## 9. 无停机迁移顺序

### 阶段 A：迁移前审计

1. 更新两个本地仓库到各自最新 `origin/master`。
2. 确认工作区干净。
3. 记录当前线上首页、文章、标签、RSS 和站点地图 URL 清单。
4. 检查待公开源码的文件清单和敏感信息风险。
5. 确认原 PaperMod gitlink 不可获取，并再次验证替代提交 `efe4cb45161be836d602d5cd0f857e62661dae8b` 与 Hugo Extended `0.105.0` 可以构建。

### 阶段 B：迁移 PR

1. 从最新 `Tips/origin/master` 创建 `feat/consolidate-hugo-site`。
2. 按允许列表复制源码到 `site/`。
3. 重建根目录 `.gitmodules`。
4. 添加 `.gitignore`。
5. 添加固定依赖的 Hugo Pages 工作流，使用启动状态触发条件。
6. 本地构建，并把根目录当前静态网页作为基线，在相同视口和明暗主题下对照首页、标签页、纯代码文章和图文文章；修复非预期差异，记录剩余纯装饰差异并在切换 Pages Source 前取得 jdy 显式接受，实质差异继续阻断。
7. 推送迁移分支并创建 PR。
8. PR 构建通过后合并。

迁移 PR 合并时，根目录旧网页成品仍然存在，因此原有分支发布方式仍有完整回滚材料。

### 阶段 C：切换 Pages 发布源

1. 在 `Tips` 的 Settings → Pages 中把 Source 改为 `GitHub Actions`。
2. 手动触发 `master` 的 Hugo 工作流。
3. 等待 Build 和 Deploy job 成功。
4. 打开 Actions 返回的部署地址。
5. 验证线上首页、标签、文章、RSS、站点地图和静态资源。

### 阶段 D：清理 PR

只有阶段 C 全部通过后，才能创建清理 PR。

清理 PR 删除 `Tips` 根目录中的旧生成文件，包括：

- `index.html`、`404.html`、`index.xml`
- `assets/`
- `categories/`
- `page/`
- `post/`
- `tags/`
- `robots.txt`
- `sitemap.xml`
- 所有根目录 `._*` 文件

同一个清理 PR 将工作流从启动状态切换到稳定状态，开启 Push 到 `master` 后自动部署。

清理后保留 `.github/`、`.gitignore`、`.gitmodules`、`docs/`、`site/` 和其他明确需要保留的仓库级文件。

## 10. URL 兼容性

构建环境从本地 macOS 迁移到 GitHub Actions Linux 后，路径大小写可能发生变化。现有内容中包含 `VSCode中使用正则查找替换` 等大小写混合目录，必须把 URL 兼容性作为发布阻断条件。

本节的兼容性范围是把旧站点内容完整迁移到新主机：比较 URL 时先把旧 URL 的主机从 `jiadingyi.github.io` 归一化为 `ken-zy.github.io`，再比较 `/Tips/` 下的路径。旧主机当前返回 404，本次迁移不保证旧主机 URL 本身继续可访问。

验证方法：

1. 从当前仓库的旧生成文件提取旧页面 URL 清单；如果旧线上 `sitemap.xml` 可访问，则同时提取并核对。
2. 从新构建的 `sitemap.xml` 提取新页面 URL 清单。
3. 把旧 URL 主机归一化为 `ken-zy.github.io` 后，每个旧页面路径必须满足以下一个条件：
   - 新构建中存在同一路径；或
   - Hugo 内容 front matter 提供 `aliases`，旧路径生成跳转页。
4. 标签、分类、RSS、图片和下载文件也必须验证。

不得仅凭首页可打开就判定迁移成功。

## 11. 验证矩阵

| 验证层级 | 检查内容 | 通过标准 |
|---|---|---|
| 文件边界 | 迁移文件清单 | 只包含允许迁移的源码；没有生成物、AppleDouble 或敏感文件 |
| Hugo 构建 | 本地及 PR 构建 | 退出状态为成功，生成 `site/public/index.html` |
| 域名 | 生成文件全文检查 | 旧域名出现次数为 0，新域名存在 |
| URL 兼容 | 归一化主机后的新旧 URL 清单比较 | 每个旧页面路径在新域名下有同路径或站内别名跳转；不要求旧主机响应 |
| 页面视觉 | 根目录旧成品与新构建的首页、标签页、纯代码文章、图文文章 | 同视口、同明暗主题对照；域名和年份差异直接接受；其他差异先修复，剩余纯装饰差异须有截图、原因和 jdy 显式接受，实质差异不得发布 |
| 链接 | 内部导航和外部链接 | 无 404；项目站点 `/Tips/` 前缀正确 |
| Pages | Actions Build/Deploy | 两个 job 均成功，部署环境为 `github-pages` |
| 线上 | 未登录浏览器访问 | 首页、文章、RSS、站点地图返回正常内容 |
| Git | 分支和工作区 | PR 已合并，本地与远程 `master` 一致，工作区干净 |

## 12. 回滚设计

### 切换 Pages 前

关闭或回滚迁移 PR即可。当前 `master / 根目录` 发布方式不受影响。

### 切换 Pages 后、清理 PR 前

如果 Actions 部署失败：

1. 将 Pages Source 改回 `Deploy from a branch`。
2. 选择 `master / 根目录`。
3. 根目录旧网页成品仍然存在，可以恢复旧站点。

### 清理 PR 后

如果后续部署出现严重问题：

1. 优先重新运行最近一次成功的 Pages 工作流。
2. 必要时回滚清理 PR，恢复根目录旧网页成品。
3. 将 Pages Source 临时改回 `master / 根目录`。

任何回滚都不得强制推送 `master`。

## 13. 风险与控制

| 风险 | 控制措施 |
|---|---|
| 私有源码意外公开敏感内容 | 迁移前执行文件 allowlist 和敏感模式审计；发现疑点立即停止 |
| 不可恢复的原主题 gitlink 或替代提交改变页面 | 固定 Hugo `0.105.0` 和替代 PaperMod 提交 `efe4cb45161be836d602d5cd0f857e62661dae8b`；以 73 个旧路径和根目录旧成品为双基线；差异先修复，纯装饰差异须记录并由 jdy 接受，实质差异阻断 |
| Actions 依赖被篡改 | 仅用官方 Action，审计后固定完整 commit SHA |
| Linux 路径大小写导致旧链接失效 | 比较新旧 URL 清单，并用 `aliases` 保留旧路径 |
| 误把路径迁移等同于旧主机兼容 | 明确旧主机不在兼容范围；先归一化主机，再阻断式校验新域名下的全部旧路径 |
| 切换发布源造成停机 | 切换前保留根目录旧网页；新部署验证后才清理 |
| 生成物重新进入 Git | `.gitignore` 忽略 `site/public/`、`site/resources/` 和构建锁文件 |
| 清理误删源码 | 清理 PR 使用明确删除清单，确认 `site/`、`.github/`、`docs/` 不在删除范围 |

## 14. 完成标准

满足以下全部条件，才算单仓库迁移完成：

- [ ] `Tips` 包含可完整构建的网站源码，并将 PaperMod 子模块固定为 `efe4cb45161be836d602d5cd0f857e62661dae8b`。
- [ ] Pull Request 可以自动验证 Hugo 构建，但不会部署。
- [ ] `master` 更新后可以自动部署 GitHub Pages。
- [ ] GitHub Pages 发布源为 `GitHub Actions`。
- [ ] 线上网站使用 `https://ken-zy.github.io/Tips/`。
- [ ] 旧域名不再出现在生成结果中。
- [ ] 所有旧文章、标签、RSS、站点地图和静态资源路径均已迁移到新域名，并以同路径或站内别名跳转形式可访问。
- [ ] 验收记录明确说明 `jiadingyi.github.io` 旧主机不属于本次兼容范围。
- [ ] 代表性模板与根目录旧成品的同视口、同明暗主题对照通过；除域名和年份外的差异已修复，或属于已记录并由 jdy 显式接受的纯装饰差异；不存在影响布局、可读性或交互的实质差异。
- [ ] 根目录旧网页成品已经通过独立清理 PR 删除。
- [ ] `site/public/` 和其他生成目录没有进入 Git。
- [ ] `Tips_hugo_source` 保持不变，作为迁移后的临时备份。
- [ ] 本地 `Tips/master` 与 `origin/master` 一致，工作区干净。

## 15. 后续任务

迁移稳定后再单独执行：

1. 发布“人人都会用 Codex”系列入口页、概览和 6 篇教程。
2. 在 `site/static/downloads/` 发布完整 PDF，并从系列入口链接。
3. 确认一段时间内不再依赖 `Tips_hugo_source` 后，再决定是否归档该仓库。
4. 单独评估 Hugo 和 PaperMod 升级，不与内容发布混合。

## 16. 官方依据

- [Hugo：使用 GitHub Pages 托管网站](https://gohugo.io/host-and-deploy/host-on-github-pages/)
- [GitHub Pages：使用自定义工作流](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)
- [GitHub Pages：配置发布源](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)
