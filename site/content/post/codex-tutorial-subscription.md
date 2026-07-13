---
title: "人人都会用 Codex · 第 3 篇 订阅与支付篇"
date: 2026-07-13T13:17:00+08:00
tags: [Codex, 教程]
draft: false
---

> 这一篇解决订阅和支付问题。做完的标志：你的 ChatGPT 账号已经升级为 Plus 或更高付费套餐，并且知道它由哪个平台管理续费。

系列：人人都会用 Codex · 上一篇：[第 2 篇 · 账号注册篇]({{< relref "post/codex-tutorial-account.md" >}})

---

## 一、先立三个预期

第一，**Free 可以使用 Codex，但额度较低**。这套教程还要连续完成安装、本地文件读取、Git 与 GitHub 版本管理和 Obsidian 知识库练习。为避免中途因额度不足停下，本教程把 **Plus 或更高付费套餐** 作为完成主路线的前提。

第二，**Plus 标准价是 `$20/月`**。实际人民币金额会受汇率、税费和应用商店定价影响，付款前以结账页显示的金额为准。不要依赖旧教程里的固定人民币价格。

第三，**订阅跟 ChatGPT 账号走，不跟设备走**。你在安卓手机或 iPhone 上订阅后，用同一个 ChatGPT 账号登录网页、手机和电脑时，套餐状态会跟随账号。

## 二、为什么会被拒付

付款失败不一定是卡里没钱。结账系统还会检查账号地区、当前位置、发卡地区、账单地址、境外订阅权限和 3D Secure 验证。网页、Apple App Store 和 Google Play 的收款规则也不完全相同。

两个“别”：

- **别在网页端连续反复试卡**：先核对地区、账单地址和银行的境外订阅开关，再决定是否重试。
- **别乱试来路不明的虚拟卡**：虚拟卡的发卡方、可用地区和风控可能随时变化，还可能涉及实名信息和资金托管风险。

> **先确认地区支持范围：** 开始下面任何支付路线前，先查看 OpenAI 当前的 [ChatGPT 支持国家和地区列表](https://help.openai.com/en/articles/7947663-chatgpt-supported-countries)。截至本文更新时，中国大陆目前不在列表中。OpenAI 说明，从不支持的国家或地区访问服务，账号可能被封禁或暂停；使用来自支持国家和地区之外的付款方式，将导致你被禁止使用 OpenAI 服务。即使付款成功，也不代表这一风险已经消失。详见 [OpenAI 对不支持地区访问和付款的说明](https://help.openai.com/en/articles/9131992)。

## 三、三条路线怎么选

| 路线 | 一句话原理 | 成本口径 | 主要门槛 |
|---|---|---|---|
| A. Google Play + 双币卡 | Google Play 管理订阅 | `$20/月` 附近，以商店为准 | 能使用 Google Play 的安卓设备和可用付款方式 |
| B. U 卡 | 使用海外虚拟 Visa 卡在网页订阅 | 套餐价格加开卡、充值或手续费 | 实名认证、USDT 与资金风险 |
| C. 外区 Apple ID + 礼品卡 | Apple 管理订阅并扣减礼品卡余额 | 以外区 App Store 实际价格为准 | 外区 Apple ID 和同地区礼品卡 |

如果你有可使用 Google Play 的安卓设备和可用双币卡，可以先看路 A。如果你是 iPhone 用户，且没有可用的双币卡，可以看路 C。路 B 涉及实名认证和加密货币，只适合已经理解相关风险的读者。

### 路 A：Google Play 订阅

**原理：** 通过安卓版 ChatGPT App 订阅时，订阅由 Google Play 管理。某些国内银行发行的双币 Visa/Mastercard 可能可用，但结果以 Google Play 和发卡行的实际验证为准。

**前提：** 一台可以正常使用 Google Play 的安卓设备，以及能够通过发卡行境外订阅验证的付款方式。

**步骤：**

1. 手机连好网络，打开 Google Play，登录准备用于下载和付款的 Google 账号。
2. 下载官方 ChatGPT App，使用第 2 篇注册的 ChatGPT 账号登录。
3. 在 App 内进入设置，选择 `Upgrade to Plus`，确认付款弹窗来自 Google Play。
4. 添加付款方式，核对套餐名称、实际金额和自动续费说明后确认付款。
5. 扣款成功后，返回 ChatGPT 账号设置确认套餐已生效。

**遇到拒付：** 先检查 Google Play 地区、账单地址、发卡行的境外交易权限和验证短信。不要在原因不明时连续更换大量卡片反复测试。

### 路 B：U 卡

**原理：** U 卡通常是使用 USDT 充值的海外虚拟 Visa 卡，可用于尝试在 ChatGPT 网页绑卡订阅。发卡商、可用地区、手续费和平台风控可能变化，不能把某张卡过去成功当成将来也一定成功。

**参考资料：**

- [Plasma One U 卡上手教程（卷柏，2026-06）](https://x.com/GoldenCicada/status/2065355998458675409)
- [Bitget Wallet U 卡完整教程（2026-05）](https://dabaiketang.com/bitget-wallet-card-guide-2026/)
- [Bitget Wallet 官方申请说明](https://web3.bitget.com/zh/helpCenter/235)

第三方教程可能包含邀请码，不使用邀请码也不影响你核对操作步骤。申请前必须自己核对当前的开卡费、年费、消费手续费、实名条件和可用地区。

**风险：** 这条路线需要实名认证、购买或转入 USDT，还会承担发卡方停服、冻结、资金托管和资产损失风险。如果你没有加密货币经验，不建议为了一次订阅盲目开卡。

### 路 C：外区 Apple ID + 礼品卡

**原理：** 使用与 Apple ID 同地区的 App Store 礼品卡充值，再由 Apple 管理 ChatGPT 订阅并扣减余额。

**适合：** iPhone 用户，或者没有可用双币卡、但能合规准备外区 Apple ID 和同区礼品卡的读者。

**步骤：**

1. 单独注册一个外区 Apple ID，不要为了下载一个 App 直接修改主力 Apple ID 地区。注册信息应当真实并符合 Apple 当前规则。可参考：[美区 Apple ID 注册保姆级教程](https://kerrynotes.com/register-american-apple-id/)。
2. 从可信渠道购买与 Apple ID 地区一致的小额礼品卡，先确认区域和币种，再兑换进该 Apple ID。
3. 在 App Store 登录该外区 Apple ID，下载官方 ChatGPT App，然后用第 2 篇注册的 ChatGPT 账号登录。
4. 在 ChatGPT App 内选择 `Upgrade to Plus`，核对 App Store 显示的实际金额、余额和自动续费说明后确认订阅。

**风险：** 礼品卡必须与 Apple ID 地区一致。来路不明的低价礼品卡可能导致余额被撤回或 Apple ID 被冻结。不要按旧教程里的土耳其区固定低价估算成本，当前价格以 App Store 结账页为准。

## 四、三条纪律

1. **自己订，不要购买需要交出账号密码的代充**。你无法确认对方使用的资金和卡片来源，账号也可能因后续拒付或撤销付款受影响。
2. **第一个月按月订阅**。先完成教程，确认自己的真实用量，再决定后续安排。
3. **付款前后保持网络和账号地区一致**。不要在短时间内频繁切换地区、设备和付款方式。

## 五、这一篇做完的标志

- [ ] ChatGPT 账号设置中显示 Plus 或更高付费套餐
- [ ] 登录邮箱与之后使用 Codex 的账号一致
- [ ] 知道订阅是由 ChatGPT 网页、Apple 还是 Google 管理
- [ ] 知道自动续费和取消入口

到这里，订阅和支付已经完成。下一篇安装桌面 App，登录同一个 ChatGPT 账号，再让 Codex 打开你的第一个文件夹。

## 六、下一篇

→ [第 4 篇 · 下载安装与登录篇]({{< relref "post/codex-tutorial-install.md" >}})

## 官方依据

- [OpenAI：Codex 与 ChatGPT 套餐](https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan/)
- [OpenAI：ChatGPT Plus](https://help.openai.com/en/articles/6950777-what-is-chatgpt-plus)
- [OpenAI：银行卡为什么被拒](https://help.openai.com/en/articles/7232916-why-was-my-credit-card-declined)
- [OpenAI：多币种和应用内订阅](https://help.openai.com/en/articles/10421635-multi-currency-billing)
- [OpenAI：ChatGPT 支持的国家和地区](https://help.openai.com/en/articles/7947663-chatgpt-supported-countries)
- [OpenAI：不支持地区的访问与付款风险](https://help.openai.com/en/articles/9131992)
