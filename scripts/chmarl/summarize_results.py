#!/usr/bin/env python3
"""Summarize EcoFair-CH-MARL CSV result outputs.

This helper is intentionally independent from Goose runtime code. It scans a
results directory for CHMARL-style CSV files and writes a compact aggregate CSV
that can be reviewed directly or used by Goose as context.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

import pandas as pd

CHMARL_PATTERNS = (
    "results_*.csv",
    "fairness_metrics_*.csv",
    "training_fairness_metrics_*.csv",
    "ppo_only_test_returns.csv",
)


def iter_csv_files(results_root: Path) -> Iterable[Path]:
    """Yield CHMARL-style CSV files under a results root."""
    for pattern in CHMARL_PATTERNS:
        yield from results_root.rglob(pattern)


def summarize_csv(path: Path, root: Path) -> list[dict[str, object]]:
    """Return per-column numeric summaries for a CSV file."""
    try:
        df = pd.read_csv(path)
    except Exception as exc:  # pragma: no cover - defensive for corrupted outputs
        return [
            {
                "file": str(path.relative_to(root)),
                "column": "__read_error__",
                "rows": 0,
                "count": 0,
                "mean": None,
                "std": None,
                "min": None,
                "max": None,
                "last": None,
                "error": str(exc),
            }
        ]

    rows: list[dict[str, object]] = []
    numeric = df.select_dtypes(include="number")

    if numeric.empty:
        rows.append(
            {
                "file": str(path.relative_to(root)),
                "column": "__no_numeric_columns__",
                "rows": len(df),
                "count": 0,
                "mean": None,
                "std": None,
                "min": None,
                "max": None,
                "last": None,
                "error": None,
            }
        )
        return rows

    for column in numeric.columns:
        series = numeric[column].dropna()
        rows.append(
            {
                "file": str(path.relative_to(root)),
                "column": column,
                "rows": len(df),
                "count": int(series.count()),
                "mean": None if series.empty else float(series.mean()),
                "std": None if series.empty or pd.isna(series.std()) else float(series.std()),
                "min": None if series.empty else float(series.min()),
                "max": None if series.empty else float(series.max()),
                "last": None if series.empty else float(series.iloc[-1]),
                "error": None,
            }
        )
    return rows


def build_summary(results_root: Path) -> pd.DataFrame:
    """Build an aggregate DataFrame for all detected CHMARL CSV files."""
    root = results_root.expanduser().resolve()
    if not root.exists():
        raise FileNotFoundError(f"Results root does not exist: {root}")
    if not root.is_dir():
        raise NotADirectoryError(f"Results root is not a directory: {root}")

    rows: list[dict[str, object]] = []
    for path in sorted(set(iter_csv_files(root))):
        rows.extend(summarize_csv(path, root))

    return pd.DataFrame(
        rows,
        columns=["file", "column", "rows", "count", "mean", "std", "min", "max", "last", "error"],
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Summarize EcoFair-CH-MARL CSV result files.")
    parser.add_argument(
        "--results-root",
        required=True,
        help="Root directory containing CHMARL result CSV files.",
    )
    parser.add_argument(
        "--out",
        default="chmarl_results_summary.csv",
        help="Path to write the aggregate summary CSV.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary = build_summary(Path(args.results_root))
    out = Path(args.out).expanduser().resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(out, index=False)
    print(f"Wrote {len(summary)} summary rows to {out}")


if __name__ == "__main__":
    main()
