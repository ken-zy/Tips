---
title: "人人都会用 Codex · 第 3 篇 订阅与支付篇"
date: 2026-07-13T13:17:00+08:00
tags: [Codex, 教程]
draft: false
---

> Codex 当前已经包含在 ChatGPT Free 套餐中，Free 可以用来短暂试用。但这套教程还要连续完成安装、本地文件读取、版本管理和知识库练习；为避免中途因额度不足停下，进入第 4 篇前必须升级 Plus，或确认账号已有更高付费套餐。

系列：人人都会用 Codex · 上一篇：[第 2 篇 · 账号注册篇]({{< relref "post/codex-tutorial-account.md" >}})

---

## 一、为什么这套教程要求付费套餐

OpenAI 当前说明：Codex 包含在 ChatGPT Free 中，但不同套餐的使用额度不同。Free 适合先打开 Codex、完成一次简短试用；这套教程还要连续完成桌面端安装、本地文件读取、Git 与 GitHub 版本管理、Obsidian 知识库练习，因此把 **Plus 或更高付费套餐** 作为完成主路线的前提。

这不是说 Free 技术上不能使用 Codex，也不是给 Free 编造一个固定额度。这里区分的是两件事：

- **产品可用性**：Free 当前可以试用 Codex。
- **教程完成条件**：为了减少中途因额度不足而停下，本教程要求 Plus 或更高付费套餐。

如果账号已经是 Pro 或其他更高付费套餐，不需要重复购买 Plus；确认账户设置中的套餐状态后，继续执行本篇验收即可。

## 二、Plus 能得到什么

OpenAI 当前对 ChatGPT Plus 的官方说明是：

- 价格为 `$20/月`，按月计费。
- 相比 Free，提供更高的模型和功能使用额度。
- Plus 仍然可能有使用上限，不等于无限使用。
- API 用量不包含在 Plus 里，本教程也不使用 API。

实际本币金额、税费和应用商店价格以你结账时看到的页面为准，不要按旧教程里的固定人民币价格做决定。

## 三、订阅入口与原文实操

### 路线 A：在 ChatGPT 网页升级

1. 登录 `chatgpt.com`。
2. 点击头像或账户菜单，选择升级套餐。
3. 选择 Plus，确认页面显示的价格和续费周期。
4. 填写付款方式并完成银行要求的验证。

OpenAI 官方要求：购买发生在支持地区，并且银行卡由支持地区的银行发行。中国大陆不在当前支持地区列表中，因此大陆银行发行的卡通常不符合这项官方要求。

**你要检查：** 付款前核对登录账号、套餐名称、每月价格和自动续费说明，不要只看“立即支付”按钮。

### 路线 B：在 ChatGPT 手机 App 内升级

在 iOS 或 Android 的官方 ChatGPT App 内订阅时，账单由 Apple App Store 或 Google Play 管理，并以应用商店显示的本币价格结算。

1. 从 Apple App Store 或 Google Play 下载官方 ChatGPT App。
2. 登录第 2 篇注册的同一个 ChatGPT 账号。
3. 在 App 设置中选择升级 Plus。
4. 按应用商店显示的付款方式完成订阅。

可用银行卡、余额或礼品卡取决于你的应用商店地区和平台规则。不要把某张卡在别人账号上成功，当成自己一定成功的保证。

**你要检查：** App 中的登录邮箱必须与准备使用 Codex 的账号一致；付款弹窗的收款平台应当是 Apple 或 Google 官方系统。

### Git 历史中的大陆用户实操原文

> 以下按 Git 历史原文恢复，用于保留原教程的实操信息，不代表当前一定可用。
>
> 不过大陆用户想要使用这个产品，是需要走一些弯路的，目前的正规订阅方式如下：
>
> - iOS 平台
> 	- 准备一个美区的 iOS 账号，下载 ChatGPT。
> 	- 用 gift card 充值，在 App 里面用 Apple 账户订阅
> - 安卓平台
> 	- 注册美区的 Google 账号，下载 ChatGPT。
> 	- 用该账号登录 ChatGPT，用 Google Play 订阅（可直接使用国内 visa 信用卡）
> - 网页端
> 	- 如果有海外银行卡，可以直接使用银行卡订阅。

## 四、付款失败时怎么处理

按这个顺序排查：

1. 核对卡号、有效期、安全码和账单地址。
2. 确认账户地区、当前位置和发卡地区符合平台规则。
3. 查看银行是否拦截了境外、订阅或 3D Secure 验证。
4. 如果通过手机 App 订阅，去 Apple 或 Google 的订阅页面检查订单状态。
5. 仍然失败，停止反复尝试，联系发卡行或 OpenAI 支持。

不要为了绕过一次失败，连续测试大量银行卡。频繁失败只会让原因更难判断。

## 五、原项目页中的支付路线

> 以下按 Git 历史原文恢复，不作为当前付款成功的保证。
>
> - 为什么国内卡直接拒付（OpenAI 风控拉黑虚拟卡 BIN 段）
> - 三条可行路：安卓 Google Play + 国内 Visa／苹果礼品卡（土耳其区约 ¥80/月）／U 卡（bybit·bitget）
> - 明确告知：桌面 App 必须 Plus 及以上订阅，没有免费档

当前 Free 可以使用 Codex，但本教程的完整主路线仍要求 Plus 或更高付费套餐。固定价格和卡片可用性以实际结账页面为准。第三方代充、共享账号、来源不明的虚拟卡，以及需要先购买加密货币才能充值的 U 卡，都存在额外的账号与资金风险。

## 六、这一篇做完的标志

- [ ] ChatGPT 账户设置中显示 Plus 或更高付费套餐
- [ ] 登录邮箱与 Codex 使用的账号一致
- [ ] 知道套餐按月自动续费，并知道在哪里取消

下一步安装桌面 App。Free 和付费套餐使用同一套 ChatGPT 登录流程；本教程后续默认你已满足上面的付费套餐前提。

→ [第 4 篇 · 下载安装与登录篇]({{< relref "post/codex-tutorial-install.md" >}})

## 官方依据

- [OpenAI：Codex 与 ChatGPT 套餐](https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan/)
- [OpenAI：ChatGPT Plus](https://help.openai.com/en/articles/6950777-what-is-chatgpt-plus)
- [OpenAI：银行卡为什么被拒](https://help.openai.com/en/articles/7232916-why-was-my-credit-card-declined)
- [OpenAI：多币种和应用内订阅](https://help.openai.com/en/articles/10421635-multi-currency-billing)
