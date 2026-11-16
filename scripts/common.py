"""共用工具：frontmatter 解析与章节切分。只用标准库。"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


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
