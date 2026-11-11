#!/usr/bin/env python3
"""校验内容库的一致性：样本卡字段、规律证据、帖子元数据、需求池编号。

用法: python3 scripts/lint_library.py [--root 仓库根]
有 ERROR 时退出码 1。
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (  # noqa: E402
    PATTERN_FIELDS, PATTERN_STATUSES, POST_REQUIRED, POST_STATUSES, ROOT, SAMPLE_REQUIRED,
    load_patterns, load_posts, load_samples, parse_frontmatter, split_ids, to_int,
)

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def lint(root: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warns: list[str] = []
    samples = load_samples(root)
    posts = load_posts(root)
    patterns = load_patterns(root)

    # --- 样本卡 ---
    seen_urls: dict[str, str] = {}
    for sid, (path, meta) in samples.items():
        rel = path.relative_to(root)
        missing = [k for k in SAMPLE_REQUIRED if not meta.get(k) or meta[k].startswith("<")]
        if missing:
            errors.append(f"{rel}: 缺字段或仍是占位符 {missing}")
            continue
        expect = f"S-{meta['platform']}-{path.stem}"
        if sid != expect:
            errors.append(f"{rel}: id 应为 {expect}（与平台和文件名一致），现为 {sid}")
        if not meta["url"].startswith("http"):
            errors.append(f"{rel}: url 不是链接，必须保留原帖出处")
        if meta["url"] in seen_urls:
            errors.append(f"{rel}: 与 {seen_urls[meta['url']]} 是同一篇（url 重复）")
        seen_urls[meta["url"]] = str(rel)
        if not DATE_RE.match(meta["collected"]):
            errors.append(f"{rel}: collected 日期格式应为 YYYY-MM-DD")
        for k in ("likes", "collects", "comments"):
            if to_int(meta[k]) is None:
                errors.append(f"{rel}: {k} 不是数字：{meta[k]}")
        if meta["reuse"] not in ("是", "部分", "否"):
            errors.append(f"{rel}: reuse 只能是 是/部分/否")
        body = path.read_text(encoding="utf-8")
        if "## 8. 评论里的真实需求" in body:
            part = body.split("## 8. 评论里的真实需求", 1)[1].split("## 9.", 1)[0]
            part = re.sub(r"<!--.*?-->|<[^>]*>", "", part, flags=re.S).strip(" -\n")
            if not part:
                warns.append(f"{rel}: 评论需求为空（没看评论就少了一半价值）")

    # --- 账号 ---
    for path in sorted((root / "library" / "accounts").glob("*.md")):
        meta, _ = parse_frontmatter(path.read_text(encoding="utf-8"))
        miss = [k for k in ("id", "platform", "name", "url", "checked") if not meta.get(k) or meta[k].startswith("<")]
        if miss:
            errors.append(f"{path.relative_to(root)}: 缺字段 {miss}")

    # --- 规律 ---
    post_ids = set(posts)
    for pid, p in patterns.items():
        miss = [f for f in PATTERN_FIELDS if f not in p]
        if miss:
            errors.append(f"patterns.md {pid}: 缺字段 {miss}")
            continue
        status = p["状态"]
        if status not in PATTERN_STATUSES:
            errors.append(f"patterns.md {pid}: 状态「{status}」不在 {PATTERN_STATUSES}")
        refs = split_ids(p["样本"])
        bad = [r for r in refs if r not in samples]
        if bad:
            errors.append(f"patterns.md {pid}: 引用了不存在的样本 {bad}")
        if not refs:
            errors.append(f"patterns.md {pid}: 没有样本证据")
        offtrack = [r for r in refs if r in samples and samples[r][1].get("pillar") == "其他"]
        if offtrack:
            warns.append(f"patterns.md {pid}: 引用了圈外参考样本 {offtrack}，不计入证据")
        valid = [r for r in refs if r in samples and r not in offtrack]
        authors = {samples[r][1].get("author") for r in valid}
        if status == "样本支持" and (len(valid) < 3 or len(authors) < 2):
            errors.append(f"patterns.md {pid}: 「样本支持」需要 ≥3 个同赛道样本且 ≥2 个账号，现在 {len(valid)} 样本 / {len(authors)} 账号")
        tests = split_ids(p["自测"])
        bad_t = [t for t in tests if t not in post_ids]
        if bad_t:
            errors.append(f"patterns.md {pid}: 自测引用了不存在的帖子 {bad_t}")
        if status in ("自测有效", "自测无效") and len(tests) < 2:
            errors.append(f"patterns.md {pid}: 「{status}」需要 ≥2 篇自测帖子，现在 {len(tests)}")

    # --- 帖子 ---
    for pid, (path, meta, _) in posts.items():
        rel = path.relative_to(root)
        miss = [k for k in POST_REQUIRED if not meta.get(k) or meta[k].startswith("<")]
        if miss and meta.get("status") not in ("idea",):
            errors.append(f"{rel}: 缺字段或仍是占位符 {miss}")
        if pid != path.parent.name:
            errors.append(f"{rel}: id 应与目录名一致（{path.parent.name}）")
        if meta.get("status") not in POST_STATUSES:
            errors.append(f"{rel}: status「{meta.get('status')}」不在 {POST_STATUSES}")
        for ref in split_ids(meta.get("patterns")):
            if ref not in patterns:
                errors.append(f"{rel}: 用到的规律 {ref} 不在 patterns.md")
        for ref in split_ids(meta.get("inspired_by")):
            if ref not in samples:
                errors.append(f"{rel}: 参考样本 {ref} 不存在")
        if meta.get("status") == "published":
            if not meta.get("url") or not meta.get("published_at"):
                errors.append(f"{rel}: 已发布但缺 url 或 published_at")
            if to_int(meta.get("d7_likes")) is None:
                warns.append(f"{rel}: 已发布但还没有 d7 数据")

    # --- 需求池 ---
    demand = root / "library" / "demand.md"
    if demand.exists():
        ids = re.findall(r"^\|\s*(D-\d{3,})\s*\|", demand.read_text(encoding="utf-8"), re.M)
        dup = sorted({i for i in ids if ids.count(i) > 1})
        if dup:
            errors.append(f"demand.md: 编号重复 {dup}")
    return errors, warns


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", type=Path, default=ROOT)
    args = ap.parse_args()
    errors, warns = lint(args.root)
    for e in errors:
        print(f"ERROR {e}")
    for w in warns:
        print(f"WARN  {w}")
    samples = load_samples(args.root)
    print(f"样本 {len(samples)} / 规律 {len(load_patterns(args.root))} / 帖子 {len(load_posts(args.root))}"
          f" —— {len(errors)} ERROR / {len(warns)} WARN")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
