"""共用工具：frontmatter 解析、章节切分、读取样本/帖子/规律。只用标准库。"""
from __future__ import annotations

import re
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SAMPLE_REQUIRED = [
    "id", "platform", "url", "author", "author_url", "author_followers", "published",
    "collected", "format", "pillar", "hook_type", "likes", "collects", "comments", "shares", "reuse",
]
POST_REQUIRED = [
    "id", "title", "status", "platform", "pillar", "role", "patterns", "inspired_by", "product", "cta_code",
]
POST_STATUSES = ["idea", "draft", "review", "approved", "published", "archived"]
PATTERN_STATUSES = ["假设", "样本支持", "自测有效", "自测无效", "废弃"]
PATTERN_FIELDS = ["类型", "状态", "描述", "模板", "样本", "自测", "备注"]


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    """解析扁平的 `key: value` frontmatter。没有 frontmatter 时返回空 dict 和原文。"""
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text
    meta: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        meta[key.strip()] = value.strip()
    body_start = text.find("\n", end + 4)
    body = text[body_start + 1:] if body_start != -1 else ""
    return meta, body


def sections(body: str) -> dict[str, str]:
    """按 `## 标题` 切分正文，返回 {标题: 内容}，去掉 HTML 注释。"""
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    out: dict[str, str] = {}
    current = None
    buf: list[str] = []
    for line in body.splitlines():
        m = re.match(r"^##\s+(.+?)\s*$", line)
        if m and not line.startswith("###"):
            if current is not None:
                out[current] = "\n".join(buf).strip()
            current = m.group(1)
            buf = []
        elif current is not None:
            buf.append(line)
    if current is not None:
        out[current] = "\n".join(buf).strip()
    return out


def to_int(value: str | None) -> int | None:
    """把指标字段转成整数；空、-1、unknown、占位符都视为缺失。支持 1.2万 / 3k。"""
    if value is None:
        return None
    v = value.strip().replace(",", "").replace("，", "")
    if not v or v.startswith("<"):
        return None
    m = re.fullmatch(r"(\d+(?:\.\d+)?)\s*(万|w|W|k|K|千)?\+?", v)
    if not m:
        return None
    num = float(m.group(1))
    unit = m.group(2)
    if unit in ("万", "w", "W"):
        num *= 10000
    elif unit in ("k", "K", "千"):
        num *= 1000
    n = int(round(num))
    return n


def split_ids(value: str | None) -> list[str]:
    if not value:
        return []
    parts = [p.strip() for p in re.split(r"[,，\s]+", value) if p.strip()]
    return [p for p in parts if p.lower() not in ("none", "无", "-")]


def load_samples(root: Path = ROOT) -> dict[str, tuple[Path, dict[str, str]]]:
    out = {}
    for path in sorted((root / "library" / "samples").rglob("*.md")):
        meta, _ = parse_frontmatter(path.read_text(encoding="utf-8"))
        sid = meta.get("id") or f"<无id:{path.name}>"
        out[sid] = (path, meta)
    return out


def load_posts(root: Path = ROOT) -> dict[str, tuple[Path, dict[str, str], str]]:
    out = {}
    for path in sorted((root / "posts").glob("*/post.md")):
        meta, body = parse_frontmatter(path.read_text(encoding="utf-8"))
        pid = meta.get("id") or f"<无id:{path.parent.name}>"
        out[pid] = (path, meta, body)
    return out


def load_patterns(root: Path = ROOT) -> dict[str, dict[str, str]]:
    """解析 patterns.md 里的 `### P-xxx 名称` 小节。"""
    path = root / "library" / "patterns.md"
    if not path.exists():
        return {}
    text = re.sub(r"```.*?```", "", path.read_text(encoding="utf-8"), flags=re.S)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    out: dict[str, dict[str, str]] = {}
    current = None
    for line in text.splitlines():
        m = re.match(r"^###\s+(P-\d{3,})\s*(.*)$", line)
        if m:
            current = m.group(1)
            out[current] = {"名称": m.group(2).strip()}
            continue
        if line.startswith("## ") or line.startswith("### "):
            current = None
            continue
        if current:
            fm = re.match(r"^-\s*([^:：]+)[:：]\s*(.*)$", line)
            if fm:
                out[current][fm.group(1).strip()] = fm.group(2).strip()
    return out


def engagement(meta: dict[str, str], prefix: str = "") -> int | None:
    """互动 = 赞 + 藏 + 评（+ 转发，若有）。缺赞藏评任一则返回 None。"""
    vals = [to_int(meta.get(prefix + k)) for k in ("likes", "collects", "comments")]
    if any(v is None or v < 0 for v in vals):
        return None
    total = sum(vals)  # type: ignore[arg-type]
    shares = to_int(meta.get(prefix + "shares"))
    if shares is not None and shares > 0:
        total += shares
    return total


def median(values: list[int]) -> float | None:
    return statistics.median(values) if values else None
