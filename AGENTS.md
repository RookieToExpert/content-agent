# content-agent 工作规则（所有 Agent 必读）

本仓库围绕 **「抓对标原帖 → 模仿创作自己的帖子 → 记录真实流量复盘」** 运作。

## 一、两个固定 Skill（按场景调用）

| 场景 | 调用 Skill | 产出位置 |
|---|---|---|
| 在浏览器抓取垂直对标博主与原帖（保存全部内页原图 `p01`～`pNN`、图上原文、正文原文、评论原话） | [`.agents/skills/benchmark-collect/SKILL.md`](.agents/skills/benchmark-collect/SKILL.md) | `benchmarks/<博主名>_<粉丝数>粉/` |
| 挑对标样板、选题、写稿、改稿、回填发布后流量数据 | [`.agents/skills/content-draft/SKILL.md`](.agents/skills/content-draft/SKILL.md) | `posts/<YYYY-MM-DD-slug>/post.md` |

## 二、分工

| 角色 | 职责 |
|---|---|
| **Codex（Mac 本地浏览器）** | 按 `benchmark-collect` SOP 访问小红书，保存对标博主的**全部内页原图、图上原始文字、正文原文、评论原话**到 `benchmarks/` |
| **Claude / Antigravity** | 陪唐睿一起看 `benchmarks/` 原帖，按 `content-draft` + `rules/voice.md` + `rules/xhs-format.md` 选题、写卡片文案与脚本、做脱敏检查 |
| **唐睿** | 拍实拍底图/截图、确认事实、审稿发布、把发布后第 1/3/7 天数据发回归档 |

## 三、硬规则

1. **对标库只放原帖内容，不写主观因果结论。** `benchmarks/` 下的帖子文件 100% 还原原图、图上原文、正文和评论，不用 AI 摘要代替原图文字，也不根据点赞数硬编因果结论。
2. **自己的帖子：故事可以编，技术和数据不能编。** 角色、情节、对话可以虚构（见 [`positioning.md`](positioning.md)）；技术步骤、代码、工具能力必须真实可复现；自己产品的功能和数据只能来自 [`products.md`](products.md) 和用户提供的真实素材。
3. **脱敏是红线。** 稿件里绝不出现公司/客户名、内部域名、IP、主机名、集群名、账号、密钥、未打码截图。写完必跑 `python3 scripts/check_draft.py <稿件>`。
4. **不自动发布、不自动回复。** 所有帖子和评论回复均由唐睿本人审核后发布。
5. 时间一律北京时间，日期格式 `YYYY-MM-DD`。
