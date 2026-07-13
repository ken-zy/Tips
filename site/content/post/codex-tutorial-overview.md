---
title: "人人都会用 Codex · 概览"
date: 2026-07-13T13:20:00+08:00
tags: [Codex, 教程]
draft: false
---

> 这一篇也是教程正文。它负责告诉你 Codex 能做什么、整套教程怎样走、哪些步骤必须完成、哪些步骤可以跳过。后面 6 篇再把每一步讲清楚。

系列：人人都会用 Codex

---

## 一、先看它能帮你做什么

**Codex 不只是回答问题，它还能在你允许的文件夹里真正完成任务。**

例如：

- 你说“整理 BL75 资料，先告诉我应该怎样分类”，它可以阅读现有文件，提出整理方案，等你确认后再修改。
- 你说“帮我做一个简单的个人网页”，它可以创建文件、生成页面，并把结果交给你检查。
- 你说“检查这个项目哪里有问题”，它可以阅读项目、解释原因、修改文件，再汇报具体改了什么。

这套教程不会一次介绍所有高级功能。我们只完成一个真实闭环：**把 BL75 交给 Codex 管理，用 Git 记录版本，用 GitHub 保存公开副本，再用 Obsidian 把它变成个人知识库。**

## 二、Codex 是什么

**Codex 是 OpenAI 的 AI 软件开发智能体。**“智能体”可以理解为：它不只给建议，还能在获得权限后阅读文件、执行操作并交付结果。

你不需要先学会编程，但需要承担三件事：

1. 说清楚想要什么结果。
2. 在修改、上传和公开之前作出确认。
3. 检查 Codex 交付的结果是否正确。

对零基础读者来说，最直观的入口是 ChatGPT 桌面 App 里的 Codex。当前官方快速入门是：安装桌面 App、登录 ChatGPT 账号、选择项目或本地文件夹，再发送第一条任务。

## 三、大陆用户开始前必须知道的风险

OpenAI 当前的 ChatGPT 支持地区列表中不包含中国大陆、香港和澳门。官方同时提醒：从支持列表之外访问或提供访问，可能导致账号被封禁或暂停。

因此，网络篇介绍的是实际连接和排查方法，不代表 OpenAI 对未支持地区作出了服务承诺。继续之前，请自行确认符合所在地法律以及你愿意接受的账号风险。

这套教程仍然要处理三类现实问题：

| 问题 | 具体是什么 | 对应教程 |
|---|---|---|
| 网络 | 桌面 App 需要稳定连接 OpenAI 服务 | 第 1 篇 |
| 账号 | 需要一个自己控制的 ChatGPT 账号 | 第 2 篇 |
| 额度 | Free 可以使用 Codex，但不同套餐额度不同 | 第 3 篇（可选） |

## 四、怎么读这份教程

主路线只有五步：

1. 网络准备。
2. 注册并验证自己的 ChatGPT 账号。
3. 安装桌面 App，打开 BL75。
4. 用 Git 和 GitHub 管理版本。
5. 用 Obsidian 和 Codex 建立个人知识库。

第 3 篇“订阅与支付”是一个**可选分支**：Free 额度够用就直接跳过；遇到额度限制或需要更高使用量时再回来升级 Plus。

- [第 1 篇 · 梯子篇]({{< relref "post/codex-tutorial-network.md" >}})
- [第 2 篇 · 账号注册篇]({{< relref "post/codex-tutorial-account.md" >}})
- [第 3 篇 · 订阅与支付篇（可选升级）]({{< relref "post/codex-tutorial-subscription.md" >}})
- [第 4 篇 · 下载安装与登录篇]({{< relref "post/codex-tutorial-install.md" >}})
- [第 5 篇 · Git 与 GitHub 篇]({{< relref "post/codex-tutorial-git-github.md" >}})
- [第 6 篇 · 个人知识库篇]({{< relref "post/codex-tutorial-knowledge-base.md" >}})

每一篇都会写清“做完的标志”。确认当前一步成功，再进入下一步。

## 五、全流程路线图

| 步骤 | 干什么 | 你要准备 | 是否必需 |
|---|---|---|---|
| 1. 网络 | 让电脑稳定连接 OpenAI | 一条可用线路 | 是 |
| 2. 注册 | 获得自己的 ChatGPT 账号 | 一个长期使用的邮箱 | 是 |
| 3. 可选升级 | Free 额度不够时升级 Plus | 官方支持的付款方式 | 否 |
| 4. 安装登录 | 安装桌面 App，打开 BL75 | 上面的 ChatGPT 账号 | 是 |
| 5. 版本管理 | 用 Git 记录 BL75，并连接 GitHub | 已确认公开范围的 BL75 | 是 |
| 6. 建知识库 | 用 Obsidian 浏览，让 Codex 按来源回答 | 上一步的 BL75 文件夹 | 是 |

## 六、开始前必须知道的三件事

1. **Free 当前可以使用 Codex。** 不同套餐的使用额度不同；额度够用就不需要先付费。
2. **注册 ChatGPT 当前不要求手机验证。** 新设备或异常登录可能触发邮箱验证码或移动端确认；本教程不使用 API key。
3. **本地文件是否公开，由你决定。** Codex 可以阅读本地文件，不等于这些文件会自动出现在 GitHub。创建公开仓库和上传都必须再次确认。

## 七、成本总账

- **最低成本**：Codex 可以从 Free 开始；实际固定成本主要取决于你的网络线路。
- **可选升级**：ChatGPT Plus 官方价格为 `$20/月`，实际本币金额和税费以结账页或应用商店显示为准。
- **Git、GitHub 公开仓库和 Obsidian 基础功能**：完成本教程不需要额外付费。

先用免费额度跑完整套流程，再决定是否升级，比一开始就购买一堆服务更稳。

## 八、一句话安全提醒

账号必须由自己注册和保管；不要购买共享账号或把密码交给代充。任何准备上传 GitHub 的文件，都要先检查密码、密钥、私人笔记和他人隐私。

## 九、概览读完的标志

- [ ] 知道主路线是网络、账号、安装、版本管理和个人知识库
- [ ] 知道第 3 篇 Plus 订阅可以跳过，Free 当前可以开始使用 Codex
- [ ] 知道未支持地区的访问风险，并愿意在继续前自行判断

## 官方依据

- [OpenAI：Codex 与 ChatGPT 套餐](https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan/)
- [OpenAI：ChatGPT 支持的国家和地区](https://help.openai.com/zh-hans-cn/articles/7947663-chatgpt-supported-countries)
- [OpenAI：ChatGPT 桌面 App 快速入门](https://developers.openai.com/codex/app)
- [OpenAI：ChatGPT Plus](https://help.openai.com/en/articles/6950777-what-is-chatgpt-plus)
