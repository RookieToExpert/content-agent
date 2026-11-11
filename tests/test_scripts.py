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
import lint_library  # noqa: E402
import report  # noqa: E402


def sample(nid: str, author: str, likes="100", collects="200", comments="30", followers="5000", url=None) -> str:
    url = url or f"https://www.xiaohongshu.com/explore/{nid}"
    return textwrap.dedent(f"""\
        ---
        id: S-xhs-{nid}
        platform: xhs
        url: {url}
        author: {author}
        author_url: https://www.xiaohongshu.com/user/profile/{author}
        author_followers: {followers}
        published: unknown
        collected: 2026-11-11
        format: 图文
        pillar: 硬核干货
        hook_type: 实用清单
        likes: {likes}
        collects: {collects}
        comments: {comments}
        shares: -1
        reuse: 是
        ---

        ## 8. 评论里的真实需求

        - 想要排查清单：「有没有完整的 checklist」

        ## 9. 复用判断
        """)


def post(pid: str, status="published", patterns="P-001", d7=("50", "80", "10"), title="GPU 掉卡我先看这三处",
         body="正文内容，讲一个具体的排查判断。", extra="") -> str:
    likes, collects, comments = d7
    return textwrap.dedent(f"""\
        ---
        id: {pid}
        title: {title}
        status: {status}
        platform: xhs
        pillar: AI热点上手
        role: 引流
        patterns: {patterns}
        inspired_by: none
        product: none
        cta_code: none
        url: https://www.xiaohongshu.com/explore/{pid}
        published_at: 2026-11-12
        d7_views: 1000
        d7_likes: {likes}
        d7_collects: {collects}
        d7_comments: {comments}
        d7_follows: 5
        leads: 1
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


PATTERNS_HEAD = "# 规律库\n\n```\n### P-999 示例\n- 状态: 乱写\n```\n\n---\n\n"


def pattern(pid: str, status: str, samples: str, tests: str = "无") -> str:
    return textwrap.dedent(f"""\
        ### {pid} 数字反差标题
        - 类型: 标题
        - 状态: {status}
        - 描述: 标题里放一个具体数字和反常识结果
        - 模板: [数字][对象]，我只看了[少数几处]
        - 样本: {samples}
        - 自测: {tests}
        - 备注: 无

        """)


class RepoFixture(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        shutil.copytree(REPO / "rules", self.tmp / "rules")
        (self.tmp / "library" / "samples" / "xhs").mkdir(parents=True)
        (self.tmp / "library" / "accounts").mkdir(parents=True)
        (self.tmp / "posts").mkdir()
        (self.tmp / "library" / "demand.md").write_text("| id |\n|---|\n", encoding="utf-8")
        (self.tmp / "library" / "patterns.md").write_text(PATTERNS_HEAD, encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def add_sample(self, nid, author, **kw):
        (self.tmp / "library" / "samples" / "xhs" / f"{nid}.md").write_text(sample(nid, author, **kw), encoding="utf-8")

    def add_post(self, pid, **kw):
        d = self.tmp / "posts" / pid
        d.mkdir()
        (d / "post.md").write_text(post(pid, **kw), encoding="utf-8")
        return d / "post.md"

    def set_patterns(self, *blocks):
        (self.tmp / "library" / "patterns.md").write_text(PATTERNS_HEAD + "".join(blocks), encoding="utf-8")


class TestCommon(unittest.TestCase):
    def test_to_int_units_and_missing(self):
        self.assertEqual(common.to_int("1.2万"), 12000)
        self.assertEqual(common.to_int("3k"), 3000)
        self.assertEqual(common.to_int("1,234"), 1234)
        self.assertEqual(common.to_int("10万+"), 100000)
        self.assertIsNone(common.to_int(""))
        self.assertIsNone(common.to_int("<数字>"))
        self.assertIsNone(common.to_int("unknown"))
        self.assertEqual(common.to_int("-1"), None)  # 负号不是合法计数，按缺失处理

    def test_engagement_requires_core_metrics(self):
        self.assertEqual(common.engagement({"likes": "1", "collects": "2", "comments": "3", "shares": "-1"}), 6)
        self.assertEqual(common.engagement({"likes": "1", "collects": "2", "comments": "3", "shares": "4"}), 10)
        self.assertIsNone(common.engagement({"likes": "1", "collects": "", "comments": "3"}))

    def test_frontmatter_missing(self):
        meta, body = common.parse_frontmatter("没有 frontmatter")
        self.assertEqual(meta, {})
        self.assertEqual(body, "没有 frontmatter")

    def test_split_ids(self):
        self.assertEqual(common.split_ids("P-001, P-002，P-003"), ["P-001", "P-002", "P-003"])
        self.assertEqual(common.split_ids("none"), [])
        self.assertEqual(common.split_ids("无"), [])


class TestCheckDraft(RepoFixture):
    def test_clean_post_passes(self):
        p = self.add_post("2026-11-12-ok")
        errors, warns = check_draft.check(p, self.tmp)
        self.assertEqual(errors, [])

    def test_review_notes_not_scanned(self):
        # 审核记录里的 IP 不应触发
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


class TestLint(RepoFixture):
    def test_empty_repo_ok(self):
        errors, _ = lint_library.lint(self.tmp)
        self.assertEqual(errors, [])

    def test_code_block_example_ignored(self):
        # PATTERNS_HEAD 里代码块中的 P-999 不应被当成规律
        self.assertNotIn("P-999", common.load_patterns(self.tmp))

    def test_sample_id_and_dup_url(self):
        self.add_sample("aaa", "甲")
        (self.tmp / "library" / "samples" / "xhs" / "bbb.md").write_text(
            sample("aaa", "乙").replace("id: S-xhs-aaa", "id: S-xhs-aaa2"), encoding="utf-8")
        errors, _ = lint_library.lint(self.tmp)
        joined = "\n".join(errors)
        self.assertIn("id 应为 S-xhs-bbb", joined)
        self.assertIn("url 重复", joined)

    def test_sample_placeholder_fields(self):
        (self.tmp / "library" / "samples" / "xhs" / "ccc.md").write_text(
            (REPO / "templates" / "sample.md").read_text(encoding="utf-8"), encoding="utf-8")
        errors, _ = lint_library.lint(self.tmp)
        self.assertTrue(any("占位符" in e for e in errors))

    def test_pattern_evidence_rules(self):
        self.add_sample("a1", "甲")
        self.add_sample("a2", "甲")
        self.add_sample("a3", "甲")
        self.set_patterns(
            pattern("P-001", "样本支持", "S-xhs-a1, S-xhs-a2, S-xhs-a3"),  # 只有 1 个账号
            pattern("P-002", "假设", "S-xhs-nope"),  # 样本不存在
            pattern("P-003", "自测有效", "S-xhs-a1", "2026-11-12-x"),  # 自测不足且帖子不存在
            pattern("P-004", "瞎写", "S-xhs-a1"),
        )
        errors, _ = lint_library.lint(self.tmp)
        joined = "\n".join(errors)
        self.assertIn("P-001", joined)
        self.assertIn("≥2 个账号", joined)
        self.assertIn("不存在的样本", joined)
        self.assertIn("不存在的帖子", joined)
        self.assertIn("≥2 篇自测", joined)
        self.assertIn("P-004", joined)

    def test_pattern_supported_ok(self):
        self.add_sample("a1", "甲")
        self.add_sample("a2", "乙")
        self.add_sample("a3", "甲")
        self.set_patterns(pattern("P-001", "样本支持", "S-xhs-a1, S-xhs-a2, S-xhs-a3"))
        errors, _ = lint_library.lint(self.tmp)
        self.assertEqual(errors, [])

    def test_offtrack_samples_not_evidence(self):
        self.add_sample("a1", "甲")
        self.add_sample("a2", "乙")
        p = self.tmp / "library" / "samples" / "xhs" / "a3.md"
        p.write_text(sample("a3", "丙").replace("pillar: 硬核干货", "pillar: 其他"), encoding="utf-8")
        self.set_patterns(pattern("P-001", "样本支持", "S-xhs-a1, S-xhs-a2, S-xhs-a3"))
        errors, warns = lint_library.lint(self.tmp)
        self.assertTrue(any("圈外参考" in w for w in warns))
        self.assertTrue(any("现在 2 样本" in e for e in errors), errors)

    def test_post_refs_and_published_fields(self):
        p = self.add_post("2026-11-12-p", patterns="P-404")
        text = p.read_text(encoding="utf-8").replace("url: https://www.xiaohongshu.com/explore/2026-11-12-p", "url:")
        p.write_text(text, encoding="utf-8")
        errors, _ = lint_library.lint(self.tmp)
        joined = "\n".join(errors)
        self.assertIn("P-404", joined)
        self.assertIn("缺 url", joined)

    def test_series_file_required(self):
        p = self.add_post("2026-11-12-s")
        text = p.read_text(encoding="utf-8").replace("role: 引流\n", "role: 引流\nseries: ghost\n")
        p.write_text(text, encoding="utf-8")
        errors, warns = lint_library.lint(self.tmp)
        self.assertTrue(any("series/ghost.md" in e for e in errors))
        self.assertTrue(any("episode" in w for w in warns))
        (self.tmp / "series").mkdir()
        (self.tmp / "series" / "ghost.md").write_text("# ghost\n", encoding="utf-8")
        errors, _ = lint_library.lint(self.tmp)
        self.assertFalse(any("series/ghost.md" in e for e in errors))

    def test_demand_dup(self):
        (self.tmp / "library" / "demand.md").write_text("| D-001 | a |\n| D-001 | b |\n", encoding="utf-8")
        errors, _ = lint_library.lint(self.tmp)
        self.assertTrue(any("编号重复" in e for e in errors))


class TestReport(RepoFixture):
    def run_report(self, samples=False):
        sys.argv = ["report.py", "--root", str(self.tmp)] + (["--samples"] if samples else [])
        buf = io.StringIO()
        with redirect_stdout(buf):
            report.main()
        return buf.getvalue()

    def test_no_data(self):
        out = self.run_report(samples=True)
        self.assertIn("还没有可用数据", out)
        self.assertIn("样本库：0 篇", out)

    def test_pattern_suggestion(self):
        self.add_sample("a1", "甲")
        self.set_patterns(pattern("P-001", "假设", "S-xhs-a1"), pattern("P-002", "假设", "S-xhs-a1"))
        self.add_post("2026-11-01-a", patterns="P-001", d7=("100", "100", "10"))
        self.add_post("2026-11-02-b", patterns="P-001", d7=("90", "90", "10"))
        self.add_post("2026-11-03-c", patterns="P-002", d7=("5", "5", "1"))
        self.add_post("2026-11-04-d", patterns="P-002", d7=("6", "6", "1"))
        self.add_post("2026-11-05-e", status="draft", patterns="P-002", d7=("999", "999", "999"))  # 草稿不计
        out = self.run_report()
        self.assertIn("基数只有 4 篇", out)
        p1 = next(ln for ln in out.splitlines() if ln.startswith("| P-001"))
        p2 = next(ln for ln in out.splitlines() if ln.startswith("| P-002"))
        self.assertIn("自测有效", p1)
        self.assertIn("自测无效", p2)
        self.assertIn("⚠ 是", p1)
        role = next(ln for ln in out.splitlines() if ln.startswith("| 引流"))
        self.assertIn("| 引流 | 4 | 1000 | 5 |", role)
        self.assertTrue(role.rstrip(" |").endswith("4"), role)  # 线索合计 4（每篇 1）

    def test_series_section_sorted_by_episode(self):
        for pid, ep in (("2026-11-20-b", "2"), ("2026-11-13-a", "1"), ("2026-11-27-c", "10")):
            p = self.add_post(pid)
            p.write_text(p.read_text(encoding="utf-8").replace("role: 引流\n", f"role: 引流\nseries: s1\nepisode: {ep}\n"),
                         encoding="utf-8")
        self.add_post("2026-11-14-solo")  # 不属于系列，不应出现在系列表
        out = self.run_report()
        rows = [ln for ln in out.splitlines() if ln.startswith("| s1 |")]
        self.assertEqual([r.split("|")[2].strip() for r in rows], ["1", "2", "10"])
        self.assertNotIn("2026-11-14-solo |", "\n".join(rows))

    def test_missing_metrics_skipped(self):
        self.add_post("2026-11-01-a", d7=("", "", ""))
        out = self.run_report()
        self.assertIn("有 d7 数据 0 篇", out)

    def test_sample_ranking_handles_unknown_followers(self):
        self.add_sample("a1", "甲", followers="-1", likes="1.2万", collects="3k", comments="100")
        out = self.run_report(samples=True)
        self.assertIn("| S-xhs-a1 | 甲 |", out)
        self.assertIn("15100", out)


if __name__ == "__main__":
    unittest.main()
