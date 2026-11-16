"""脚本自测：python3 -m unittest discover -s tests -v"""
from __future__ import annotations

import io
import shutil
import sys
import tempfile
import textwrap
import unittest
from contextlib import redirect_stdout
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

import check_draft  # noqa: E402
import common  # noqa: E402


def post(pid: str, status="published", title="GPU 掉卡我先看这三处",
         body="正文内容，讲一个具体的排查判断。", extra="") -> str:
    return textwrap.dedent(f"""\
        ---
        id: {pid}
        title: {title}
        status: {status}
        platform: xhs
        pillar: 热点
        role: 引流
        product: none
        cta_code: none
        ---

        ## 封面文案

        掉卡别急着重启

        ## 正文

        {body}

        ## 话题

        #AI基础设施 #GPU

        ## 审核记录

        - check_draft：内部备注可以写 10.0.0.1 不应被扫描
        {extra}
        """)


class TestCommon(unittest.TestCase):
    def test_frontmatter_missing(self):
        meta, body = common.parse_frontmatter("没有 frontmatter")
        self.assertEqual(meta, {})
        self.assertEqual(body, "没有 frontmatter")


class TestCheckDraft(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        shutil.copytree(REPO / "rules", self.tmp / "rules")
        (self.tmp / "posts").mkdir()

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def add_post(self, pid, **kw):
        d = self.tmp / "posts" / pid
        d.mkdir()
        (d / "post.md").write_text(post(pid, **kw), encoding="utf-8")
        return d / "post.md"

    def test_clean_post_passes(self):
        p = self.add_post("2026-11-12-ok")
        errors, warns = check_draft.check(p, self.tmp)
        self.assertEqual(errors, [])

    def test_review_notes_not_scanned(self):
        p = self.add_post("2026-11-12-notes")
        errors, _ = check_draft.check(p, self.tmp)
        self.assertFalse(any("IP" in e for e in errors))

    def test_redlines(self):
        body = "那天 10.140.1.2 上的 host-10-140-220-33 挂了，pjlab 的同事说 token: abcdefgh12345 有问题。加v聊 https://x.com"
        p = self.add_post("2026-11-12-bad", body=body)
        errors, _ = check_draft.check(p, self.tmp)
        joined = "\n".join(errors)
        for needle in ("IP 地址", "主机/节点名", "敏感词：pjlab", "密钥", "站外引流"):
            self.assertIn(needle, joined)

    def test_version_number_is_not_ip(self):
        p = self.add_post("2026-11-12-ver", body="todoulist 1.8.3 版本修了一个问题，CUDA 12.4.1 也能用。")
        errors, _ = check_draft.check(p, self.tmp)
        self.assertFalse(any("IP" in e for e in errors))

    def test_title_and_body_length(self):
        p = self.add_post("2026-11-12-long", title="这是一个特别特别特别特别特别特别长的标题超过二十字", body="字" * 1001)
        errors, _ = check_draft.check(p, self.tmp)
        self.assertTrue(any("标题" in e for e in errors))
        self.assertTrue(any("正文" in e for e in errors))

    def test_missing_title(self):
        p = self.add_post("2026-11-12-notitle", title="<最终标题，≤20 字>")
        errors, _ = check_draft.check(p, self.tmp)
        self.assertTrue(any("title" in e for e in errors))

    def test_ai_tells(self):
        body = "家人们，这不是运气，而是方法。也不是天赋，而是积累。希望对你有帮助"
        p = self.add_post("2026-11-12-ai", body=body)
        _, warns = check_draft.check(p, self.tmp)
        joined = "\n".join(warns)
        self.assertIn("家人们", joined)
        self.assertIn("不是…而是", joined)
        self.assertIn("希望对你有帮助", joined)

    def test_cli_exit_code(self):
        p = self.add_post("2026-11-12-cli", body="pjlab")
        sys.argv = ["check_draft.py", str(p), "--root", str(self.tmp)]
        with redirect_stdout(io.StringIO()):
            self.assertEqual(check_draft.main(), 1)


if __name__ == "__main__":
    unittest.main()
