"""Tests for skills/build/token_meter.py, on a made-up project folder with known numbers."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills" / "build"))
import token_meter as tm  # noqa: E402

SECRET = "sk-ant-THIS-MUST-NEVER-APPEAR"


def reply(mid, model, inp, out, cw=0, cr=0, ts="2026-11-28T10:00:00Z", text=SECRET):
    return {
        "type": "assistant",
        "timestamp": ts,
        "message": {
            "id": mid,
            "model": model,
            "content": [{"type": "text", "text": text}],
            "usage": {
                "input_tokens": inp,
                "output_tokens": out,
                "cache_creation_input_tokens": cw,
                "cache_read_input_tokens": cr,
            },
        },
    }


def write(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")


def project(tmp: Path) -> Path:
    proj = tmp / "proj"
    sid = "s1"
    write(proj / f"{sid}.jsonl", [
        {"type": "user", "message": {"content": SECRET}},
        reply("m1", "claude-opus-5-5", 10, 100, cw=1000, cr=0),
        reply("m1", "claude-opus-5-5", 10, 100, cw=1000, cr=0),  # the same reply written twice: count once
        reply("m2", "claude-opus-5-5", 5, 50, cw=0, cr=2000, ts="2026-11-29T10:00:00Z"),
        "not json at all",
    ])
    sub = proj / sid / "subagents"
    write(sub / "agent-a1.jsonl", [reply("x1", "claude-sonnet-5-5", 100, 400, cw=500, cr=3000)])
    (sub / "agent-a1.meta.json").write_text(json.dumps({"description": "Build T1 test harness", "model": "sonnet"}))
    write(sub / "agent-a2.jsonl", [reply("x2", "claude-sonnet-5-5", 50, 200, cw=0, cr=1000)])
    (sub / "agent-a2.meta.json").write_text(json.dumps({"description": "Combined check T2 and T3"}))
    write(sub / "agent-a3.jsonl", [reply("x3", "claude-sonnet-5-5", 1, 1)])  # no meta file
    return proj


class TokenMeter(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.proj = project(Path(self._tmp.name))
        self.runs = tm.scan(self.proj)

    def tearDown(self):
        self._tmp.cleanup()

    def by(self, agent):
        return next(r for r in self.runs if r.agent == agent)

    def test_totals_dedupe_and_skip_bad_lines(self):  # T-R1
        main = self.by("main")
        self.assertEqual((main.input, main.output, main.cache_write, main.cache_read), (15, 150, 1000, 2000))
        self.assertEqual(main.replies, 2)
        self.assertEqual(main.models, {"claude-opus-5-5"})
        self.assertEqual(main.first_day, "2026-11-28")
        self.assertEqual(self.by("a1").total, 100 + 400 + 500 + 3000)
        self.assertEqual(len(self.runs), 4)

    def test_tasks_and_roles_from_descriptions(self):  # T-R2
        a1, a2, a3 = self.by("a1"), self.by("a2"), self.by("a3")
        self.assertEqual((a1.tasks, a1.role), (["T1"], "builder"))
        self.assertEqual((a2.tasks, a2.role), (["T2", "T3"], "check"))
        self.assertEqual((a3.tasks, a3.role), ([], "other"))
        self.assertEqual(self.by("main").role, "supervisor")

    def test_fresh_tokens_leave_out_cache_reads(self):  # T-R3, T-R5
        a1 = self.by("a1")
        self.assertEqual(a1.fresh, 100 + 400 + 500)
        self.assertEqual(tm.per_task(self.runs)["T1"], a1.fresh)  # budgets use fresh tokens by default

    def test_synthetic_replies_are_not_a_model(self):  # T-R1
        log = self.proj / "s2.jsonl"
        write(log, [reply("z1", "<synthetic>", 0, 0), reply("z2", "claude-opus-5-5", 1, 2)])
        run = tm.read_run(log, "main")
        self.assertEqual(run.models, {"claude-opus-5-5"})
        self.assertEqual(run.replies, 1)

    def test_per_task_splits_shared_runs(self):  # T-R2
        per = tm.per_task(self.runs, measure="total")
        self.assertEqual(per["T1"], self.by("a1").total)
        self.assertEqual(per["T2"], self.by("a2").total / 2)
        self.assertEqual(per["T3"], self.by("a2").total / 2)

    def test_cache_savings_need_no_prices(self):  # T-R3, T-R4
        s = tm.summary(self.runs)
        self.assertEqual(s["cache_read"], 2000 + 3000 + 1000)
        self.assertIsNone(s["cost"])  # no prices file: tokens only
        self.assertIn("tokens only", tm.report(self.runs))

    def test_cost_with_a_prices_file(self):  # T-R4
        prices = {"as_of": "2026-11-28", "per_million": {
            "claude-opus-5-5": {"input": 10, "output": 50, "cache_write": 12.5, "cache_read": 1},
            "claude-sonnet-5-5": {"input": 2, "output": 10, "cache_write": 2.5, "cache_read": 0.2}}}
        s = tm.summary(self.runs, prices)
        opus = (15 * 10 + 150 * 50 + 1000 * 12.5 + 2000 * 1) / 1e6
        self.assertAlmostEqual(s["by_model_cost"]["claude-opus-5-5"], opus)
        # Saved by the cache: what cache reads would have cost as plain input, minus what they did cost.
        saved_opus = 2000 * (10 - 1) / 1e6
        self.assertAlmostEqual(s["cache_saved_cost"]["claude-opus-5-5"], saved_opus)
        self.assertIn("2026-11-28", tm.report(self.runs, prices))

    def test_lean_savings_against_a_measured_baseline(self):  # T-R3
        sizes = {"T1": "M", "T2": "S", "T3": "S"}
        lean = tm.lean_savings(tm.per_task(self.runs), sizes, baseline={"S": 10000, "M": 10000})
        self.assertEqual(lean["T2"], 10000 - self.by("a2").fresh / 2)
        self.assertNotIn("T9", lean)

    def test_budget_warnings(self):  # T-R5
        per = {"T1": 130000, "T2": 30000, "T3": 70000}
        flags = tm.budget_flags(per, {"T1": "M", "T2": "S", "T3": "S"}, {"S": 60000, "M": 150000})
        self.assertEqual(flags, {"T1": "warning: 87% of 150,000", "T3": "over: 117% of 60,000"})

    def test_private_output(self):  # T-R6
        out = tm.report(self.runs) + tm.ledger_rows(self.runs) + json.dumps(tm.summary(self.runs))
        self.assertNotIn(SECRET, out)
        self.assertNotIn(str(self.proj), out)

    def test_ledger_rows_are_markdown(self):  # T-R2
        rows = tm.ledger_rows(self.runs)
        self.assertIn("| 2026-11-28 | T1 | builder | claude-sonnet-5-5 | 4,000 |", rows)


if __name__ == "__main__":
    unittest.main()
