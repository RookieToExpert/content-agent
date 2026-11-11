#!/usr/bin/env python3
"""检查一篇帖子稿件：红线（脱敏/引流/密钥）、平台长度、AI 腔。

用法: python3 scripts/check_draft.py posts/2026-11-12-xxx/post.md [--root 仓库根]
有 ERROR 时退出码 1。脚本只能兜底，不能替代人审（截图打码、案例可定位性要人看）。
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, parse_frontmatter, sections  # noqa: E402

TITLE_MAX = 20
BODY_MAX = 1000

IP_RE = re.compile(r"(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])")
HOST_RE = re.compile(r"\b(?:host|node|gpu|npu|master|worker|vc)-\d+(?:[-.]\d+)+\b", re.I)
SECRET_ASSIGN_RE = re.compile(r"(?i)\b(?:secret|token|passwd|password|access[_-]?key|secret[_-]?key|ak|sk)\s*[:=]\s*\S{6,}")
LONG_TOKEN_RE = re.compile(r"(?<![A-Za-z0-9/_.-])[A-Za-z0-9+/_-]{32,}(?![A-Za-z0-9/_-])")
OUTBOUND_RE = re.compile(r"(?i)(微信号|加\s*v|\bvx\b|\bwx\b|v信|二维码|扫码|https?://|www\.)")
ABSOLUTE_RE = re.compile(r"(最好|最强|第一|100%|百分百|绝对|唯一|永久)")
NOT_BUT_RE = re.compile(r"不是[^。！？\n]{1,30}?而是")
EMOJI_LEAD_RE = re.compile(r"^\s*[☀-➿\U0001F300-\U0001FAFF]")


def load_terms(path: Path, markers: bool = False) -> list[str]:
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    if markers:
        m = re.search(r"<!-- BEGIN TERMS -->(.*?)<!-- END TERMS -->", text, re.S)
        text = m.group(1) if m else ""
    return [ln.strip() for ln in text.splitlines() if ln.strip() and not ln.strip().startswith("#")]


def check(path: Path, root: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warns: list[str] = []
    text = path.read_text(encoding="utf-8")
    meta, body = parse_frontmatter(text)
    secs = sections(body)
    body_no_comments = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    # 审核记录是内部备注，不参与内容扫描
    scan_text = re.split(r"^##\s+审核记录", body_no_comments, maxsplit=1, flags=re.M)[0]
    publish_text = "\n".join([meta.get("title", ""), secs.get("封面文案", ""), secs.get("正文", ""), secs.get("话题", "")])

    # --- 长度 ---
    title = meta.get("title", "")
    if not title or title.startswith("<"):
        errors.append("frontmatter 缺少 title（最终标题）")
    elif len(title) > TITLE_MAX:
        errors.append(f"标题 {len(title)} 字，超过 {TITLE_MAX} 字：{title}")
    content = secs.get("正文", "")
    if not content:
        errors.append("缺少「## 正文」或正文为空")
    elif len(content) > BODY_MAX:
        errors.append(f"正文 {len(content)} 字，超过 {BODY_MAX} 字")
    topics = re.findall(r"#[^\s#]+", secs.get("话题", ""))
    if not topics:
        warns.append("没有话题标签")
    elif len(topics) > 10:
        warns.append(f"话题 {len(topics)} 个，偏多")

    # --- 红线：脱敏 ---
    lowered = scan_text.lower() + "\n" + title.lower()
    for term in load_terms(root / "rules" / "redline_terms.txt"):
        if term.lower() in lowered:
            errors.append(f"命中敏感词：{term}")
    for ip in sorted(set(IP_RE.findall(scan_text + title))):
        errors.append(f"出现 IP 地址：{ip}")
    for h in sorted(set(HOST_RE.findall(scan_text))):
        errors.append(f"出现主机/节点名样式字符串：{h}")
    for s in SECRET_ASSIGN_RE.findall(scan_text):
        errors.append(f"疑似密钥/凭据：{s[:20]}…")
    for tok in sorted(set(LONG_TOKEN_RE.findall(scan_text))):
        warns.append(f"长随机串，确认不是密钥：{tok[:12]}…")

    # --- 红线：站外引流（只查会发出去的部分）---
    for m in sorted(set(OUTBOUND_RE.findall(publish_text))):
        errors.append(f"站外引流/外链：{m}")

    # --- 产品稿的绝对化用语 ---
    product = meta.get("product", "none").strip().lower()
    if product and product not in ("none", "无") and not product.startswith("<"):
        for m in sorted(set(ABSOLUTE_RE.findall(publish_text))):
            warns.append(f"产品稿出现绝对化用语：{m}")

    # --- AI 腔 ---
    for term in load_terms(root / "rules" / "ai-tells-zh.md", markers=True):
        try:
            hits = re.findall(term, publish_text)
        except re.error:
            hits = [term] if term in publish_text else []
        if hits:
            warns.append(f"AI 腔：{term} ×{len(hits)}")
    nb = NOT_BUT_RE.findall(publish_text)
    if len(nb) > 1:
        warns.append(f"「不是…而是」出现 {len(nb)} 次，最多 1 次")
    emoji_lines = [ln for ln in content.splitlines() if EMOJI_LEAD_RE.match(ln)]
    if len(emoji_lines) >= 3:
        warns.append(f"{len(emoji_lines)} 行以 emoji 开头，像 AI 的项目符号")
    lines = [ln for ln in content.splitlines() if ln.strip()]
    if len(lines) >= 8 and sum(len(ln) <= 15 for ln in lines) / len(lines) > 0.8:
        warns.append("八成以上的行都是短句单独成行（诗体），按自然停顿分段")

    # --- 元数据 ---
    if meta.get("status") in ("approved", "published") and not meta.get("cta_code"):
        warns.append("cta_code 为空：没有口令就无法归因转化（无产品露出可填 none）")
    return errors, warns


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+", type=Path)
    ap.add_argument("--root", type=Path, default=ROOT)
    args = ap.parse_args()
    failed = False
    for f in args.files:
        errors, warns = check(f, args.root)
        print(f"== {f}")
        for e in errors:
            print(f"  ERROR {e}")
        for w in warns:
            print(f"  WARN  {w}")
        if not errors and not warns:
            print("  OK")
        print(f"  结果：{len(errors)} ERROR / {len(warns)} WARN（脚本通过≠可以发布，截图打码和可定位性仍需人审）")
        failed = failed or bool(errors)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
