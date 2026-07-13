---
title: "人人都会用 Codex · 第 4 篇 下载安装与登录篇"
date: 2026-07-13T13:16:00+08:00
tags: [Codex, 教程]
draft: false
---

> 这一篇把 Codex 真正装进电脑。做完的标志：**你能打开 Codex 桌面端，选择一个本地项目，并让它正确说出项目里有什么。**

系列：人人都会用 Codex · 上一篇：[第 3 篇 · 订阅与支付篇]({{< relref "post/codex-tutorial-subscription.md" >}})

---

## 一、开始前先检查两件事

1. 电脑上的梯子保持开启，Clash Verge 的 TUN 模式也开着。
2. 准备好前两篇完成注册和订阅的 ChatGPT 账号，确认账户设置显示 Plus 或更高付费套餐，并且能在 `chatgpt.com` 正常登录。

Free 当前可以试用 Codex，并且 Free 与付费套餐使用同一套 ChatGPT 登录流程；本教程的不同点是开始安装前必须确认账号已是 Plus 或更高付费套餐。

**成功标志：** 浏览器能打开 ChatGPT，登录后可以看到聊天界面，并在账户设置中确认付费套餐状态。

## 二、下载并打开桌面 App

先说明一个容易困惑的地方：OpenAI 当前把 Codex 放在 **ChatGPT 桌面 App** 中。你安装的是 ChatGPT 桌面 App，登录后再选择 Codex，不需要另外寻找第三方“Codex 安装包”。

1. 打开上面的官方页面，找到 **Download ChatGPT**。
2. 选择与你电脑对应的 Windows 或 macOS 版本并下载。
3. 按系统提示完成安装，然后打开 ChatGPT 桌面 App。
4. 登录后，如果界面提供 Chat、Work 和 Codex 等选择，进入 **Codex**。

只从 OpenAI 官方页面下载，不要搜索来路不明的“Codex 安装包”。

界面名称和按钮位置可能随版本或账号 rollout 略有变化，以“能够选择 Codex 并打开本地文件夹”为准。

**成功标志：** App 能正常打开，登录后可以进入 Codex。

## 三、用 ChatGPT 账号登录

1. 在 App 里点击登录。
2. 如果系统打开浏览器，就使用前两篇完成注册和订阅的**同一个 ChatGPT 账号**完成登录和授权。
3. 授权结束后回到桌面 App。官方当前流程也是直接[使用 ChatGPT 账号连接 Codex](https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan/)，不需要再注册一个 Codex 账号。

如果登录过程中触发额外验证，回到[账号注册篇]({{< relref "post/codex-tutorial-account.md" >}})第四节处理。

**成功标志：** App 不再显示登录按钮，左下角能看到你的账号头像或名称。

## 四、选择第一个本地项目

进入 Codex 后，主界面左侧的“项目”区域会列出你加入过的文件夹；第一次使用时，先点“新建任务”，再从输入框上方的文件夹入口选择或打开一个本地文件夹。

下图是当前 Codex 主界面：左侧是项目列表，输入框上方依次显示项目名称、运行位置和 Git 分支。

![](https://img.jdy.systems/manual/20260711164847517.webp)

第一次练习，建议新建一个不含隐私资料的测试文件夹，并在里面放一两个你认识的文件。选中这个文件夹后，如果系统询问是否允许访问，点击允许。

选好后，输入框上方会显示三类信息：项目名称、运行位置和当前 Git 分支。例如截图中的 `obsidian · 本地 · main`，表示当前任务使用 obsidian 项目、在本机运行，Git 分支是 main。普通文件夹不是 Git 项目时，可能不会显示分支。

**成功标志：** 左侧项目列表中能看到刚才选择的文件夹；输入框上方同时显示该项目名称和“本地”。

## 五、做一次只读验收

在输入框粘贴下面这句话：

> 请列出这个文件夹里的主要文件，并用一句话说明每个文件是什么。只读取，不要修改任何文件。

发送后，对照 Codex 的回答和文件夹里的真实文件名。

**成功标志：** Codex 说出的文件名与文件夹中的实际内容一致，而且没有新增或修改文件。

## 六、三个常见问题

| 现象 | 先这样处理 |
|---|---|
| 官方页面打不开或下载失败 | 确认梯子和 TUN 模式开启，换一个干净节点后重试 |
| 浏览器显示登录成功，但没有自动回到 App | 保持 App 开着，允许浏览器“打开 ChatGPT”；仍无反应就退出 App 后重开 |
| App 能打开，但加载不出内容 | 先切 Clash Verge 全局模式测试；能恢复说明是分流规则问题 |

## 七、这一篇做完的标志

- [ ] Codex 桌面端已安装并登录
- [ ] 左侧项目列表能看到自己的项目
- [ ] 输入框上方显示项目名称和“本地”
- [ ] Codex 能正确读出其中的文件，且没有修改内容

下一篇先给这个本地项目装上版本记录，再把确认可公开的版本保存到 GitHub。

→ [第 5 篇 · Git 与 GitHub 篇]({{< relref "post/codex-tutorial-git-github.md" >}})

## 官方依据

- [ChatGPT 桌面 App 官方快速入门](https://developers.openai.com/codex/app)
- [Using Codex with your ChatGPT plan](https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan/)
- [ChatGPT Work and Codex](https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex)
