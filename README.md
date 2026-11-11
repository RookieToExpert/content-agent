# content-agent

AI 行业开发者账号的内容运营库：**学别人怎么发帖 → 沉淀成有证据的规律 → 用自己的真实经历写稿 → 用发布后的数据修正规律。**
先做小红书，结构对 X / 公众号等通用。

## 闭环

```
 收样本(content-research) ──► 样本卡 + 评论需求 ──► 规律库(带证据和状态)
        ▲                                               │
        │                                               ▼
 数据回流(content-review) ◄── 发布(人工) ◄── 审核 ◄── 写稿(content-draft)
```

| 环节 | 谁来做 | 产物 |
|---|---|---|
| 抓取 | Mac 上的小红书抓取 skill，**小号、低频** | 帖子/评论/数据 JSON |
| 拆解、提炼 | agent + `content-research` | `library/samples/`、`accounts/`、`patterns.md`、`demand.md` |
| 写稿 | agent + `content-draft` | `posts/<日期-slug>/post.md` |
| 审核、发布 | **本人** | 状态改 approved → published |
| 数据、评论、复盘 | agent + `content-review` | d1/d3/d7 数据、回复草稿、`reviews/` |

## 和现成 skill 的关系

调研过的现成 skill（2026-11-11 读过原文）都只覆盖一段，这里借了它们的长处：

| 来源 | 借了什么 |
|---|---|
| [LeeFeee/WriteLikeMaster-Skill](https://github.com/LeeFeee/WriteLikeMaster-Skill) | Content-Judge 的 8 项拆解维度（→ 样本卡 1～9 节）、写前 6 问（→ content-draft 澄清步骤） |
| [Felo-Inc/felo-skills](https://github.com/Felo-Inc/felo-skills) twitter-writer | 「风格 DNA」概念和维度（→ 账号模板）；生成依赖其付费 API，未采用 |
| [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) social | 逆向拆解流程、证据标注、No AI Tells（→ 中文 AI 腔黑名单） |
| [autoclaw-cc/xiaohongshu-skills](https://github.com/autoclaw-cc/xiaohongshu-skills) / [white0dew/XiaohongshuSkills](https://github.com/white0dew/XiaohongshuSkills) | 作为抓取/数据导出的「手脚」，装在 Mac 上，使用前需审读源码 |

## 第一周怎么开始

1. 改 `positioning.md`（定位草案）和 `products.md`（产品真实功能）——这两份不填，agent 写不出真东西
2. 找 5～10 个对标账号，收 20～30 篇高互动样本：`让 agent 用 content-research 拆这篇 <链接/截图>`
3. 样本到 10 篇后让 agent 提炼第一批规律
4. 写 3 篇稿（每个支柱一篇），审核后手动发
5. 每篇记 d1/d3/d7 数据，周末跑 content-review 复盘

## 检查脚本

```bash
python3 scripts/check_draft.py posts/<slug>/post.md   # 红线、长度、AI 腔
python3 scripts/lint_library.py                       # 样本/规律/帖子一致性、规律证据是否够
python3 scripts/report.py --samples                   # 自己帖子表现、规律自测效果、样本排行
python3 -m unittest discover -s tests                 # 脚本自测
```
