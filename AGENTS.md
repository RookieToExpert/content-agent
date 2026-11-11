# content-agent 工作规则（所有 agent 必读）

本仓库是唐睿的内容运营库：学习别人怎么发帖 → 沉淀成有证据的规律 → 用自己的真实经历写稿 → 发布后用数据修正规律。
小红书是第一个渠道，结构对其他平台通用（`platform` 字段区分）。

## 三个 skill，按场景调用

| 场景 | skill |
|---|---|
| 收样本（只收同赛道）、拆解爆款、分析对标账号、整理评论需求 | `.agents/skills/content-research` |
| 选题、写稿、改稿、做配图文案 | `.agents/skills/content-draft` |
| 填发布后数据、周/月复盘、哪些规律真的有效 | `.agents/skills/content-review` |

动手前先读对应 SKILL.md，不凭印象做。

## 硬规则

1. **故事可以编，技术和数据不能编。** 角色、情节、场景可以虚构（见 `positioning.md`「真实性边界」）；技术步骤、代码、工具能力必须真实可复现；自己产品的功能和数据只能来自 `products.md` 和用户提供的素材。
2. **脱敏是红线。** 稿件里不能出现公司/客户名、内部域名、IP、主机名、集群名、账号、密钥、未打码截图。规则见 `rules/redlines.md`，`scripts/check_draft.py` 会拦截一部分，但脚本不能替代人看。
3. **学结构，不抄内容。** 样本卡只摘标题和关键句（单句引用），不整篇搬运原文；永远保留原帖链接和作者。
4. **规律要有证据。** `library/patterns.md` 每条规律必须引用样本 id，状态按证据升降（见 content-review）。只有 1～2 个样本支持的只能叫「假设」。
5. **不自动发布、不自动回复。** 发布和评论回复只给草稿，用户确认后由用户（或经用户明确同意的工具）执行。
6. **抓取要克制。** 用小号、每批 ≤20 篇、批次之间间隔，不绕过平台限制。
7. **改完跑检查：** `python3 scripts/check_draft.py <稿件>`、`python3 scripts/lint_library.py`，有 ERROR 不提交。
8. 时间一律北京时间，日期写 `YYYY-MM-DD`。

## 目录

```
positioning.md        定位、受众、内容支柱、语气（用户确认过的才算数）
products.md           产品真实功能、截图位置、解决的具体问题、转化口令
library/
  samples/<平台>/      一篇样本一张卡（templates/sample.md）
  accounts/            对标账号风格 DNA（templates/account.md）
  patterns.md          规律库，带证据和状态
  demand.md            评论里挖出的真实需求池，带出处
posts/<日期-slug>/     自己的帖子：post.md（稿件+元数据+发布后数据）、assets/
reviews/              周/月复盘（content-review 产出）
series/               系列规划：设定、分集表、终点（对应小红书合集）
rules/                 redlines.md 红线、ai-tells-zh.md 中文 AI 腔黑名单
templates/             样本卡、账号、帖子模板
scripts/               check_draft.py / lint_library.py / report.py（只用标准库）
```
