---
name: content-draft
description: 选题、参照 benchmarks/ 原帖写自己的图文卡片或视频脚本、改稿、以及回填发布后流量数据时使用。触发语：「写一篇」「出个选题」「改一下这篇」「填数据」「复盘这篇」。抓别人的原帖用 benchmark-collect。
---

# content-draft：参照对标原帖写我们自己的内容 & 记录流量

核心原则：**从 `benchmarks/` 挑一篇对标原帖看样式 → 用我们自己的真实技术/生活素材套进去（故事角色可编，技术与数据必真） → 跑 `check_draft.py` 脱敏 → 发布后回填流量。**

## 开始前必读

1. `AGENTS.md`、`positioning.md`（赛道与 4 个系列）
2. `rules/voice.md`（怎么写得有意思）、`rules/xhs-format.md`（小红书卡片长什么样）、`rules/redlines.md`、`rules/ai-tells-zh.md`
3. `benchmarks/README.md`：挑一篇与本次题材最搭的对标原帖，打开看它的卡片页数、每页字数和节奏
4. 写系列帖必读 `series/<系列>.md`；写产品露出必读 `products.md`

---

## 流程

### 1. 选题与挑对标样板
- 给 3 个候选选题，每个写清：**标题候选 / 普通人为什么前 3 秒会停下来 / 参照 `benchmarks/` 里的哪一篇原帖格式 / 用我们自己的什么真实素材**。
- 由用户挑定后再动笔。

### 2. 定核心与设定（写正文前先跟用户对齐）
- **一句话核心**：这篇只讲哪一件事？
- **戏精设定**：用什么视角讲（如「被 AI 包养的第 X 天」「零基础女朋友做 App」）？
- **开头画面（P1 封面 + P2 首滑页）**：封面大字写什么、标题写什么（两者分工，不重复）、P2 怎么防划走？
- **翻车/笑点 + 结尾画面**：中后段放哪个具体的小翻车？结尾落在哪句对话或画面上？

### 3. 生成 `posts/<YYYY-MM-DD-slug>/post.md`

按以下固定模板创建 `post.md`：

```markdown
---
id: <YYYY-MM-DD-slug>
title: <最终笔记标题，≤20 字>
status: draft
platform: xhs
pillar: <小白造工具 | 热点 | AI管我 | 给自己造工具>
role: <引流 | 信任 | 转化>
series: <系列名 或 none>
episode: <集数 或留空>
benchmark_ref: <参照的 benchmarks/ 原帖路径>
product: <todoulist | website-monitor | none>
cta_code: <口令 或 none>
url:
published_at:
d1_views:
d1_likes:
d1_collects:
d1_comments:
d1_follows:
d7_views:
d7_likes:
d7_collects:
d7_comments:
d7_follows:
leads:
---

## 选题卡

- 参照对标原帖：
- 读者是谁 & 为什么会停下来：
- 一句话核心：
- 真实技术/数据素材出处：

## 标题候选（≤20 字，标出选中项）

1. **...**
2. ...
3. ...

## 卡片（图片内容，按页；小红书内容主要在这里）

1. 封面：...
2. 第2页：...
...

## 正文

（3～6 句话补充，≤1000 字）

## 配图与素材清单

- 哪几页是文字卡片、哪几页需要用户拍实拍图或截真实界面

## 话题

#话题1 #话题2 ...

## 审核与发布后复盘记录

- check_draft 结果：
- 发布后表现与复盘（对比对标原帖，哪里好、下一篇改什么）：
```

### 4. 自检与交审
1. 运行 `python3 scripts/check_draft.py posts/<slug>/post.md`，确保 `0 ERROR`。
2. 对照 `rules/voice.md` 检查：有没有背景式无聊开头？有没有把封面字和标题写成同一句话？
3. 更新顶层 `README.md` 的「二、我们的发帖与进度看板」。

### 5. 发布后回填数据
- 用户发来第 1 / 3 / 7 天数据截图或数字时，填入 `post.md` 的 frontmatter 及文末复盘区，并同步更新顶层 `README.md` 进度表。
