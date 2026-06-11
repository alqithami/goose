#!/usr/bin/env python3
"""CHMARL MCP server.

This server connects Goose to a local EcoFair-CH-MARL workspace. It reads local
repository files and generated CSV outputs, then exposes structured tools for
experiment discovery, result summarization, comparison, reporting, and
paper-to-code traceability support.

It intentionally does not execute training commands or arbitrary shell code.
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import pandas as pd
from mcp.server.fastmcp import FastMCP


DEFAULT_REPO_DIR = Path.cwd()
DEFAULT_RESULTS_DIR = Path.cwd() / "results"
DEFAULT_REPORT_DIR = Path.cwd() / "reports"

REPO_DIR = DEFAULT_REPO_DIR
RESULTS_DIR = DEFAULT_RESULTS_DIR
REPORT_DIR = DEFAULT_REPORT_DIR

CHMARL_PATTERNS = (
    "results_*.csv",
    "fairness_metrics_*.csv",
    "training_fairness_metrics_*.csv",
    "ppo_only_test_returns.csv",
)

EXPECTED_OUTPUT_GLOBS = (
    "results_*.csv",
    "fairness_metrics_*.csv",
    "training_fairness_metrics_*.csv",
)

METRIC_ALIASES: dict[str, tuple[str, ...]] = {
    "return": ("return", "returns", "average_return", "avg_return", "episode_return"),
    "gini": ("gini", "gini_coefficient"),
    "max_min_ratio": ("max_min_ratio", "max-min", "max_min", "minmax", "min_max_ratio"),
    "fuel": ("fuel", "fuel_usage", "total_fuel", "episode_fuel"),
    "emission": ("emission", "emissions", "global_emissions"),
}

mcp = FastMCP("chmarl")


def _json(payload: Any) -> str:
    """Serialize a payload for MCP clients."""
    return json.dumps(payload, indent=2, default=str, ensure_ascii=False)


def _exists_dir(path: Path) -> bool:
    return path.exists() and path.is_dir()


def _safe_base(path: Path, label: str) -> Path:
    resolved = path.expanduser().resolve()
    if not resolved.exists():
        raise FileNotFoundError(f"{label} does not exist: {resolved}")
    if not resolved.is_dir():
        raise NotADirectoryError(f"{label} is not a directory: {resolved}")
    return resolved


def _safe_repo_dir() -> Path:
    return _safe_base(REPO_DIR, "CHMARL repository directory")


def _safe_results_dir() -> Path:
    return _safe_base(RESULTS_DIR, "CHMARL results directory")


def _safe_report_dir() -> Path:
    resolved = REPORT_DIR.expanduser().resolve()
    resolved.mkdir(parents=True, exist_ok=True)
    return resolved


def _safe_child(base: Path, user_path: str) -> Path:
    """Resolve a user-provided relative path inside base."""
    base = base.expanduser().resolve()
    candidate = (base / user_path).expanduser().resolve()
    if candidate != base and base not in candidate.parents:
        raise ValueError(f"Path escapes configured base directory: {user_path}")
    return candidate


def _iter_result_files(root: Path | None = None) -> Iterable[Path]:
    base = _safe_results_dir() if root is None else root.expanduser().resolve()
    for pattern in CHMARL_PATTERNS:
        yield from base.rglob(pattern)


def _all_result_files(root: Path | None = None) -> list[Path]:
    return sorted(set(path for path in _iter_result_files(root) if path.is_file()))


def _relative_to_results(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(_safe_results_dir()))
    except Exception:
        return str(path)


def _read_csv(path: Path) -> pd.DataFrame:
    try:
        return pd.read_csv(path)
    except Exception as exc:
        raise ValueError(f"Failed to read CSV {path}: {exc}") from exc


def _numeric_summary(df: pd.DataFrame) -> dict[str, dict[str, float | int | None]]:
    numeric = df.select_dtypes(include="number")
    summary: dict[str, dict[str, float | int | None]] = {}
    for column in numeric.columns:
        series = numeric[column].dropna()
        if series.empty:
            summary[column] = {
                "count": 0,
                "mean": None,
                "median": None,
                "std": None,
                "min": None,
                "max": None,
                "first": None,
                "last": None,
                "delta": None,
            }
            continue
        first = float(series.iloc[0])
        last = float(series.iloc[-1])
        summary[column] = {
            "count": int(series.count()),
            "mean": float(series.mean()),
            "median": float(series.median()),
            "std": None if pd.isna(series.std()) else float(series.std()),
            "min": float(series.min()),
            "max": float(series.max()),
            "first": first,
            "last": last,
            "delta": last - first,
        }
    return summary


def _file_kind(path: Path) -> str:
    name = path.name
    if name.startswith("training_fairness_metrics_"):
        return "training_fairness"
    if name.startswith("fairness_metrics_"):
        return "evaluation_fairness"
    if name.startswith("results_"):
        return "evaluation_returns"
    if name == "ppo_only_test_returns.csv":
        return "legacy_ppo_returns"
    return "unknown"


def _algorithm_from_filename(path: Path) -> str | None:
    name = path.name
    match = re.match(r"(?:results|fairness_metrics|training_fairness_metrics)_([a-zA-Z0-9_-]+)\.csv$", name)
    if match:
        return match.group(1)
    if name == "ppo_only_test_returns.csv":
        return "ppo"
    return None


def _experiment_key(path: Path) -> str:
    results_dir = _safe_results_dir()
    try:
        parent = path.parent.resolve().relative_to(results_dir)
    except ValueError:
        return "."
    return "." if str(parent) == "." else str(parent)


def _summarize_file(path: Path) -> dict[str, Any]:
    df = _read_csv(path)
    return {
        "file": _relative_to_results(path),
        "kind": _file_kind(path),
        "algorithm": _algorithm_from_filename(path),
        "experiment": _experiment_key(path),
        "rows": int(len(df)),
        "columns": list(df.columns),
        "numeric_columns": list(df.select_dtypes(include="number").columns),
        "numeric_summary": _numeric_summary(df),
    }


def _metric_columns(df: pd.DataFrame, metric: str) -> list[str]:
    metric_key = metric.strip().lower()
    aliases = METRIC_ALIASES.get(metric_key, (metric_key,))
    numeric_columns = list(df.select_dtypes(include="number").columns)
    matches: list[str] = []
    for column in numeric_columns:
        normalized = column.lower().replace(" ", "_")
        if any(alias in normalized for alias in aliases):
            matches.append(column)
    return matches


def _reduce_series(series: pd.Series, reducer: str) -> float | None:
    clean = series.dropna()
    if clean.empty:
        return None
    reducer = reducer.lower()
    if reducer == "mean":
        return float(clean.mean())
    if reducer == "median":
        return float(clean.median())
    if reducer == "min":
        return float(clean.min())
    if reducer == "max":
        return float(clean.max())
    if reducer == "last":
        return float(clean.iloc[-1])
    if reducer == "first":
        return float(clean.iloc[0])
    raise ValueError(f"Unsupported reducer: {reducer}")


def _experiment_files(experiment: str | None = None) -> list[Path]:
    files = _all_result_files()
    if not experiment or experiment in {".", "all", "*"}:
        return files
    normalized = experiment.strip().strip("/")
    return [path for path in files if _experiment_key(path).startswith(normalized)]


@mcp.tool()
def chmarl_healthcheck() -> str:
    """Return configured CHMARL paths and basic availability."""
    payload = {
        "server": "chmarl",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "repo_dir": str(REPO_DIR.expanduser().resolve()),
        "repo_dir_exists": _exists_dir(REPO_DIR.expanduser().resolve()),
        "results_dir": str(RESULTS_DIR.expanduser().resolve()),
        "results_dir_exists": _exists_dir(RESULTS_DIR.expanduser().resolve()),
        "report_dir": str(REPORT_DIR.expanduser().resolve()),
        "report_dir_exists": _exists_dir(REPORT_DIR.expanduser().resolve()),
    }
    return _json(payload)


@mcp.tool()
def inspect_chmarl_repo() -> str:
    """Inspect the configured EcoFair-CH-MARL repository for expected files."""
    repo = _safe_repo_dir()
    expected = {
        "main_script": repo / "EcoFairCHMARL.py",
        "readme": repo / "README.md",
        "requirements": repo / "requirements.txt",
        "pyproject": repo / "pyproject.toml",
        "tests_dir": repo / "tests",
        "results_dir": repo / "results",
    }
    payload = {
        "repo_dir": str(repo),
        "exists": {name: path.exists() for name, path in expected.items()},
        "python_files_top_level": sorted(path.name for path in repo.glob("*.py")),
        "result_file_count": len(_all_result_files(RESULTS_DIR if RESULTS_DIR.exists() else repo / "results"))
        if (RESULTS_DIR.exists() or (repo / "results").exists())
        else 0,
        "recommendations": [],
    }
    if not expected["requirements"].exists() and not expected["pyproject"].exists():
        payload["recommendations"].append("Add requirements.txt or pyproject.toml for reproducible installs.")
    if not expected["tests_dir"].exists():
        payload["recommendations"].append("Add tests for metrics, environment reset/step, and CLI behavior.")
    if expected["main_script"].exists():
        payload["recommendations"].append("Consider splitting EcoFairCHMARL.py into env, metrics, train, baselines, and cli modules.")
    return _json(payload)


@mcp.tool()
def list_chmarl_result_files() -> str:
    """List detected CHMARL CSV result files under the configured results directory."""
    results = _safe_results_dir()
    files = _all_result_files(results)
    payload = {
        "results_dir": str(results),
        "file_count": len(files),
        "files": [
            {
                "file": _relative_to_results(path),
                "kind": _file_kind(path),
                "algorithm": _algorithm_from_filename(path),
                "experiment": _experiment_key(path),
                "bytes": path.stat().st_size,
            }
            for path in files
        ],
    }
    return _json(payload)


@mcp.tool()
def list_chmarl_experiments() -> str:
    """Group detected result files by experiment directory."""
    experiments: dict[str, list[dict[str, Any]]] = {}
    for path in _all_result_files():
        key = _experiment_key(path)
        experiments.setdefault(key, []).append(
            {
                "file": path.name,
                "kind": _file_kind(path),
                "algorithm": _algorithm_from_filename(path),
                "bytes": path.stat().st_size,
            }
        )
    payload = {
        "results_dir": str(_safe_results_dir()),
        "experiment_count": len(experiments),
        "experiments": [
            {"experiment": key, "file_count": len(value), "files": value}
            for key, value in sorted(experiments.items())
        ],
    }
    return _json(payload)


@mcp.tool()
def inspect_chmarl_schema(filename: str) -> str:
    """Return row count, columns, and numeric columns for a selected result CSV."""
    path = _safe_child(_safe_results_dir(), filename)
    if not path.exists():
        raise FileNotFoundError(f"Result file not found: {filename}")
    df = _read_csv(path)
    payload = {
        "file": _relative_to_results(path),
        "rows": int(len(df)),
        "columns": list(df.columns),
        "numeric_columns": list(df.select_dtypes(include="number").columns),
        "non_numeric_columns": list(df.select_dtypes(exclude="number").columns),
    }
    return _json(payload)


@mcp.tool()
def summarize_chmarl_file(filename: str) -> str:
    """Summarize a single CHMARL result CSV by relative filename."""
    path = _safe_child(_safe_results_dir(), filename)
    if not path.exists():
        raise FileNotFoundError(f"Result file not found: {filename}")
    return _json(_summarize_file(path))


@mcp.tool()
def summarize_chmarl_results(experiment: str = "all") -> str:
    """Summarize all detected result files, optionally under one experiment directory."""
    files = _experiment_files(experiment)
    payload = {
        "results_dir": str(_safe_results_dir()),
        "experiment_filter": experiment,
        "file_count": len(files),
        "summaries": [_summarize_file(path) for path in files],
    }
    return _json(payload)


@mcp.tool()
def compare_chmarl_experiments(metric: str = "return", reducer: str = "mean") -> str:
    """Compare experiments using a metric such as return, gini, or max_min_ratio."""
    rows: list[dict[str, Any]] = []
    for path in _all_result_files():
        df = _read_csv(path)
        columns = _metric_columns(df, metric)
        for column in columns:
            value = _reduce_series(df[column], reducer)
            rows.append(
                {
                    "experiment": _experiment_key(path),
                    "file": _relative_to_results(path),
                    "kind": _file_kind(path),
                    "algorithm": _algorithm_from_filename(path),
                    "metric": metric,
                    "matched_column": column,
                    "reducer": reducer,
                    "value": value,
                }
            )
    payload = {
        "metric": metric,
        "reducer": reducer,
        "comparison_count": len(rows),
        "comparisons": sorted(rows, key=lambda item: (item["experiment"], item["file"], item["matched_column"])),
        "note": "Fuel-related columns should be treated as emissions proxies unless direct emissions columns exist.",
    }
    return _json(payload)


@mcp.tool()
def rank_chmarl_runs(metric: str = "gini", reducer: str = "mean", ascending: bool = True) -> str:
    """Rank result files by a selected metric."""
    rows = json.loads(compare_chmarl_experiments(metric=metric, reducer=reducer))["comparisons"]
    rows = [row for row in rows if row.get("value") is not None]
    rows.sort(key=lambda row: row["value"], reverse=not ascending)
    payload = {
        "metric": metric,
        "reducer": reducer,
        "ascending": ascending,
        "ranked_count": len(rows),
        "ranked": rows,
    }
    return _json(payload)


@mcp.tool()
def detect_missing_chmarl_outputs(expected_experiments: str = "baseline,emission_cap,fairness,emission_fairness,soto,fen") -> str:
    """Check expected experiment directories and expected output file patterns."""
    results = _safe_results_dir()
    expected = [item.strip() for item in expected_experiments.split(",") if item.strip()]
    checks: list[dict[str, Any]] = []
    for experiment in expected:
        exp_dir = results / experiment
        missing_patterns = []
        found_files = []
        for pattern in EXPECTED_OUTPUT_GLOBS:
            matches = sorted(exp_dir.glob(pattern)) if exp_dir.exists() else []
            if not matches:
                missing_patterns.append(pattern)
            found_files.extend(match.name for match in matches)
        checks.append(
            {
                "experiment": experiment,
                "directory": str(exp_dir),
                "directory_exists": exp_dir.exists(),
                "found_files": sorted(found_files),
                "missing_patterns": missing_patterns,
                "complete": exp_dir.exists() and not missing_patterns,
            }
        )
    payload = {
        "results_dir": str(results),
        "expected_experiments": expected,
        "checks": checks,
    }
    return _json(payload)


@mcp.tool()
def create_chmarl_ablation_plan(episodes: int = 2000, output_root: str = "results/chmarl_ablation") -> str:
    """Create a shell command plan for a standard CHMARL ablation matrix."""
    cases = [
        ("baseline", ""),
        ("emission_cap", "--emission_cap"),
        ("fairness", "--fairness"),
        ("emission_fairness", "--emission_cap --fairness"),
        ("soto", "--algo SOTO"),
        ("fen", "--algo FEN"),
    ]
    commands = []
    for name, flags in cases:
        command = f"python EcoFairCHMARL.py --episodes {episodes} --outdir {output_root}/{name}"
        if flags:
            command += f" {flags}"
        commands.append({"case": name, "command": command})
    payload = {
        "episodes": episodes,
        "output_root": output_root,
        "commands": commands,
        "notes": [
            "Run these from the EcoFairCHAMRL repository root.",
            "Add explicit seed support in EcoFairCHAMRL.py before publishing multi-seed claims.",
            "QMIX and MAPPO should only be included when verified implementations and outputs exist.",
        ],
    }
    return _json(payload)


@mcp.tool()
def generate_chmarl_markdown_report(report_name: str = "chmarl_experiment_report.md", metric: str = "return") -> str:
    """Generate a markdown report summarizing detected CHMARL result files."""
    report_dir = _safe_report_dir()
    safe_name = re.sub(r"[^a-zA-Z0-9_.-]", "_", Path(report_name).name)
    report_path = report_dir / safe_name

    experiments = json.loads(list_chmarl_experiments())
    comparison = json.loads(compare_chmarl_experiments(metric=metric, reducer="mean"))
    missing = json.loads(detect_missing_chmarl_outputs())

    lines = [
        "# CHMARL experiment report",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        f"Results directory: `{_safe_results_dir()}`",
        "",
        "## Experiments detected",
        "",
    ]
    for item in experiments["experiments"]:
        lines.append(f"- `{item['experiment']}`: {item['file_count']} result file(s)")
    lines.extend(["", f"## Metric comparison: `{metric}`", ""])
    for row in comparison["comparisons"]:
        lines.append(
            f"- `{row['experiment']}` / `{row['file']}` / `{row['matched_column']}`: {row['value']} ({row['reducer']})"
        )
    lines.extend(["", "## Missing-output check", ""])
    for item in missing["checks"]:
        status = "complete" if item["complete"] else "missing outputs"
        lines.append(f"- `{item['experiment']}`: {status}; missing={item['missing_patterns']}")
    lines.extend(
        [
            "",
            "## Caveats",
            "",
            "- Fuel-related columns should be treated as emissions proxies unless direct emissions columns are present.",
            "- Placeholder or fallback algorithms should not be described as fully implemented baselines.",
            "- Multi-seed claims require explicit seed handling and stored metadata.",
        ]
    )

    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    payload = {"report_path": str(report_path), "bytes": report_path.stat().st_size}
    return _json(payload)


@mcp.tool()
def paper_to_code_traceability_stub() -> str:
    """Return a starter paper-to-code traceability matrix for CHMARL."""
    rows = [
        {
            "claim": "Constrained hierarchical MARL framework",
            "expected_code": "EcoFairCHMARL.py or future chmarl/env.py and chmarl/train.py",
            "status": "partially implemented / needs verification",
            "next_check": "Verify explicit high-level and low-level policy separation.",
        },
        {
            "claim": "Real-time emission budget",
            "expected_code": "environment reward logic: emission_cap_enabled, emission_cap_value, gamma_emis",
            "status": "partially implemented",
            "next_check": "Add tests for cap violation and penalty scaling.",
        },
        {
            "claim": "Fairness-aware reward shaping",
            "expected_code": "compute_gini, compute_minmax_ratio, SOTO/FEN wrappers",
            "status": "partially implemented",
            "next_check": "Map wrappers to paper equations and add tests.",
        },
        {
            "claim": "QMIX and MAPPO baselines",
            "expected_code": "optional baseline discovery and outputs",
            "status": "placeholder/fallback unless verified outputs exist",
            "next_check": "Do not publish full-baseline claims without true implementations and result files.",
        },
        {
            "claim": "Maritime digital twin scale",
            "expected_code": "num_ports, num_vessels, queueing, weather, fuel curves",
            "status": "simplified prototype / needs benchmarking",
            "next_check": "Add scale experiments and runtime notes.",
        },
    ]
    return _json({"rows": rows})


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="CHMARL MCP server")
    parser.add_argument("--repo-dir", default=str(DEFAULT_REPO_DIR), help="Path to the EcoFairCHAMRL repository.")
    parser.add_argument("--results-dir", default=str(DEFAULT_RESULTS_DIR), help="Path to CHMARL results directory.")
    parser.add_argument("--report-dir", default=str(DEFAULT_REPORT_DIR), help="Directory for generated reports.")
    return parser.parse_args()


def main() -> None:
    global REPO_DIR, RESULTS_DIR, REPORT_DIR
    args = _parse_args()
    REPO_DIR = Path(args.repo_dir).expanduser().resolve()
    RESULTS_DIR = Path(args.results_dir).expanduser().resolve()
    REPORT_DIR = Path(args.report_dir).expanduser().resolve()
    mcp.run()


if __name__ == "__main__":
    main()
