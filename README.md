# content-agent

AI 时代「普通人也能给自己造工具」的内容运营工作台：
**1. 收对标原帖（`benchmarks/`） ──► 2. 照着原帖写我们自己的图文/视频（`posts/`） ──► 3. 发布后记录流量复盘。**

---

## 一、核心目录（一眼看懂）

| 目录 / 文件 | 作用 |
|---|---|
| 📊 **[`benchmarks/`（对标原帖库）](benchmarks/README.md)** | 按博主中文名归档的同赛道原帖（**100% 原图 + 图上原文 + 正文原文**），写稿时直接挑一篇照着写 |
| ✍️ **[`posts/`（我们的帖子）](posts/)** | 我们自己写的每一篇帖子（含逐页卡片文案、配图与发布后 d1/d3/d7 流量数据） |
| 🎬 **[`series/`（合集规划）](series/ai-database.md)** | 小红书合集分集表，如 [《被AI包养的第X天》](series/ai-database.md) |
| 🎯 **[`positioning.md`（账号定位）](positioning.md)** | 赛道定位、4 个系列（小白造工具 / 热点 / AI管我 / 给自己造工具）、真实性边界 |
| 📦 **[`products.md`（产品素材库）](products.md)** | 我们自己的两个产品（`todoulist`、`网站监控`）真实功能与截图位置 |
| 📏 **[`rules/`（写作与脱敏规则）](rules/)** | [怎么写得有意思(`voice.md`)](rules/voice.md) · [小红书卡片版式(`xhs-format.md`)](rules/xhs-format.md) · [脱敏红线(`redlines.md`)](rules/redlines.md) · [去AI腔(`ai-tells-zh.md`)](rules/ai-tells-zh.md) |
| 🛠️ **[`.agents/skills/`（两个固定 Skill）](.agents/skills/)** | [`benchmark-collect`](.agents/skills/benchmark-collect/SKILL.md)（抓对标原帖） · [`content-draft`](.agents/skills/content-draft/SKILL.md)（写稿与记数据） |

---

## 二、我们的发帖与进度看板

| 序号 / 目录 | 标题 | 所属系列 | 对标参考原帖 | 状态 | d7 浏览 / 赞 / 藏 / 评 / 涨粉 |
|---|---|---|---|---|---|
| [2026-11-11-ai-coach-database](posts/2026-11-11-ai-coach-database/post.md) | 我把自己存进了数据库，然后被AI包养了 | AI管我（第1集） | [林熙乐·10页文字卡](benchmarks/林熙乐_350粉/01_1794赞_github搞钱最快的方式.md) | `review`（待做图发布） | 待发布后记录 |

---

## 三、发布前自动检查

```bash
python3 scripts/check_draft.py posts/<目录>/post.md   # 检查脱敏红线（IP/主机名/公司名/密钥）、字数上限、AI腔
python3 -m unittest discover -s tests                 # 脚本自测
```
