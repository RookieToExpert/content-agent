#!/usr/bin/env python3
"""数据复盘：自己帖子的表现、每条规律的自测效果、样本库概况。

用法:
  python3 scripts/report.py            # 自己帖子 + 规律效果
  python3 scripts/report.py --samples  # 再加样本库排行

互动 = 赞 + 藏 + 评（+ 转发）。帖子用 d7 数据。数字都由代码算，复盘结论引用这里的输出。
"""
from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, engagement, load_patterns, load_posts, load_samples, median, split_ids, to_int  # noqa: E402

SMALL_BASE = 10


def fmt(v: float | None) -> str:
    if v is None:
        return "-"
    return f"{v:.0f}" if float(v).is_integer() else f"{v:.1f}"


def post_report(root: Path) -> None:
    posts = load_posts(root)
    patterns = load_patterns(root)
    rows = []
    for pid, (_, meta, _) in posts.items():
        if meta.get("status") != "published":
            continue
        rows.append((pid, meta, engagement(meta, "d7_")))
    with_data = [r for r in rows if r[2] is not None]
    print(f"## 自己的帖子：已发布 {len(rows)} 篇，有 d7 数据 {len(with_data)} 篇")
    if not with_data:
        print("（还没有可用数据）\n")
        return
    if len(with_data) < SMALL_BASE:
        print(f"⚠ 基数只有 {len(with_data)} 篇（<{SMALL_BASE}），以下对比只能当参考，不能据此定论。")
    overall = median([r[2] for r in with_data])
    print(f"d7 互动中位数：{fmt(overall)}\n")
    print("| 帖子 | 支柱 | d7浏览 | d7互动 | 收藏/赞 | 涨粉 | 线索 | 口令 |")
    print("|---|---|---|---|---|---|---|---|")
    for pid, meta, eng in sorted(with_data, key=lambda r: -r[2]):
        likes = to_int(meta.get("d7_likes")) or 0
        collects = to_int(meta.get("d7_collects")) or 0
        ratio = f"{collects / likes:.2f}" if likes else "-"
        print(f"| {pid} | {meta.get('pillar', '')} | {fmt(to_int(meta.get('d7_views')))} | {eng} | {ratio} "
              f"| {fmt(to_int(meta.get('d7_follows')))} | {fmt(to_int(meta.get('leads')))} | {meta.get('cta_code', '')} |")

    by_pillar: dict[str, list[int]] = defaultdict(list)
    for _, meta, eng in with_data:
        by_pillar[meta.get("pillar", "?")].append(eng)
    print("\n## 按支柱\n\n| 支柱 | 篇数 | 互动中位数 |\n|---|---|---|")
    for k, v in sorted(by_pillar.items(), key=lambda kv: -(median(kv[1]) or 0)):
        print(f"| {k} | {len(v)} | {fmt(median(v))} |")

    print("\n## 规律自测效果（d7 互动中位数 vs 全部帖子中位数）\n")
    print("| 规律 | 当前状态 | 使用篇数 | 使用帖中位数 | 建议状态 | 是否需改 |\n|---|---|---|---|---|---|")
    uses: dict[str, list[int]] = defaultdict(list)
    for _, meta, eng in with_data:
        for ref in split_ids(meta.get("patterns")):
            uses[ref].append(eng)
    for ref in sorted(set(patterns) | set(uses)):
        cur = patterns.get(ref, {}).get("状态", "（不在规律库）")
        vals = uses.get(ref, [])
        m = median(vals)
        if len(vals) >= 2 and m is not None and overall is not None:
            suggest = "自测有效" if m > overall else "自测无效"
        else:
            suggest = cur
        change = "⚠ 是" if suggest != cur and cur not in ("废弃",) else ""
        print(f"| {ref} | {cur} | {len(vals)} | {fmt(m)} | {suggest} | {change} |")
    total_leads = sum(to_int(r[1].get("leads")) or 0 for r in with_data)
    total_follows = sum(to_int(r[1].get("d7_follows")) or 0 for r in with_data)
    print(f"\n合计：d7 涨粉 {total_follows}，线索 {total_leads}\n")


def sample_report(root: Path) -> None:
    samples = load_samples(root)
    print(f"## 样本库：{len(samples)} 篇")
    if not samples:
        return
    rows = []
    for sid, (_, meta) in samples.items():
        eng = engagement(meta)
        fol = to_int(meta.get("author_followers"))
        rel = eng / fol if eng is not None and fol and fol > 0 else None
        likes = to_int(meta.get("likes")) or 0
        collects = to_int(meta.get("collects")) or 0
        rows.append((sid, meta, eng, rel, collects / likes if likes else None))
    authors = {r[1].get("author") for r in rows}
    print(f"覆盖账号 {len(authors)} 个\n")
    print("| 样本 | 作者 | 支柱 | 互动 | 互动/粉丝 | 收藏/赞 | 复用 |\n|---|---|---|---|---|---|---|")
    for sid, meta, eng, rel, ratio in sorted(rows, key=lambda r: -(r[2] or 0))[:30]:
        print(f"| {sid} | {meta.get('author')} | {meta.get('pillar')} | {fmt(eng)} | "
              f"{'-' if rel is None else f'{rel:.2f}'} | {'-' if ratio is None else f'{ratio:.2f}'} | {meta.get('reuse')} |")
    print("\n收藏/赞 >1 通常说明是「干货型」，读者想留着用；互动/粉丝高说明内容本身带量，而不是靠账号粉丝基数。\n")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", type=Path, default=ROOT)
    ap.add_argument("--samples", action="store_true")
    args = ap.parse_args()
    post_report(args.root)
    if args.samples:
        sample_report(args.root)
    return 0


if __name__ == "__main__":
    sys.exit(main())
