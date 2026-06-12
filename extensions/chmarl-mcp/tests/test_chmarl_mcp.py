from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest


MODULE_PATH = Path(__file__).resolve().parents[1] / "chmarl_mcp.py"
SAMPLE_RESULTS = Path(__file__).resolve().parents[1] / "examples" / "sample_results"


def load_module():
    spec = importlib.util.spec_from_file_location("chmarl_mcp", MODULE_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture()
def chmarl(tmp_path: Path):
    module = load_module()
    repo_dir = tmp_path / "EcoFairCHAMRL"
    repo_dir.mkdir()
    (repo_dir / "EcoFairCHMARL.py").write_text("print('sample chmarl repo')\n", encoding="utf-8")
    (repo_dir / "README.md").write_text("# Sample EcoFairCHAMRL\n", encoding="utf-8")

    module.REPO_DIR = repo_dir
    module.RESULTS_DIR = SAMPLE_RESULTS
    module.REPORT_DIR = tmp_path / "reports"
    return module


def parse(payload: str):
    return json.loads(payload)


def test_healthcheck_reports_configured_paths(chmarl):
    payload = parse(chmarl.chmarl_healthcheck())
    assert payload["server"] == "chmarl"
    assert payload["repo_dir_exists"] is True
    assert payload["results_dir_exists"] is True


def test_inspect_repo_finds_expected_files_and_recommendations(chmarl):
    payload = parse(chmarl.inspect_chmarl_repo())
    assert payload["exists"]["main_script"] is True
    assert payload["exists"]["readme"] is True
    assert "EcoFairCHMARL.py" in payload["python_files_top_level"]
    assert payload["recommendations"]


def test_list_result_files_and_experiments(chmarl):
    files = parse(chmarl.list_chmarl_result_files())
    assert files["file_count"] == 6
    assert {item["experiment"] for item in files["files"]} == {"baseline", "fairness"}

    experiments = parse(chmarl.list_chmarl_experiments())
    assert experiments["experiment_count"] == 2
    assert {item["experiment"] for item in experiments["experiments"]} == {"baseline", "fairness"}


def test_schema_and_file_summary(chmarl):
    schema = parse(chmarl.inspect_chmarl_schema("baseline/results_ppo.csv"))
    assert schema["rows"] == 3
    assert schema["numeric_columns"] == ["episode", "return"]

    summary = parse(chmarl.summarize_chmarl_file("baseline/results_ppo.csv"))
    assert summary["numeric_summary"]["return"]["mean"] == pytest.approx(105.0)
    assert summary["numeric_summary"]["return"]["delta"] == pytest.approx(5.0)


def test_summarize_all_results(chmarl):
    payload = parse(chmarl.summarize_chmarl_results())
    assert payload["file_count"] == 6
    assert len(payload["summaries"]) == 6


def test_compare_and_rank_metrics(chmarl):
    comparison = parse(chmarl.compare_chmarl_experiments(metric="return", reducer="mean"))
    values = {(row["experiment"], row["file"]): row["value"] for row in comparison["comparisons"]}
    assert values[("baseline", "baseline/results_ppo.csv")] == pytest.approx(105.0)
    assert values[("fairness", "fairness/results_ppo.csv")] == pytest.approx(95.3333333333)

    ranked = parse(chmarl.rank_chmarl_runs(metric="gini", reducer="mean", ascending=True))
    assert ranked["ranked_count"] >= 2
    assert ranked["ranked"][0]["value"] <= ranked["ranked"][-1]["value"]


def test_detect_missing_outputs(chmarl):
    payload = parse(chmarl.detect_missing_chmarl_outputs("baseline,fairness,emission_cap"))
    checks = {item["experiment"]: item for item in payload["checks"]}
    assert checks["baseline"]["complete"] is True
    assert checks["fairness"]["complete"] is True
    assert checks["emission_cap"]["complete"] is False
    assert checks["emission_cap"]["missing_patterns"]


def test_ablation_plan_and_traceability_stub(chmarl):
    plan = parse(chmarl.create_chmarl_ablation_plan(episodes=10, output_root="results/test"))
    assert len(plan["commands"]) == 6
    assert plan["commands"][0]["command"].startswith("python EcoFairCHMARL.py --episodes 10")

    traceability = parse(chmarl.paper_to_code_traceability_stub())
    assert len(traceability["rows"]) >= 5
    assert any("emission" in row["claim"].lower() for row in traceability["rows"])


def test_generate_markdown_report(chmarl):
    payload = parse(chmarl.generate_chmarl_markdown_report("report.md", metric="return"))
    report_path = Path(payload["report_path"])
    assert report_path.exists()
    text = report_path.read_text(encoding="utf-8")
    assert "# CHMARL experiment report" in text
    assert "baseline" in text
    assert "fairness" in text
