"""Build every London population dashboard dataset from one source: the London sex-age-component
totals CSV at /Users/user1/Downloads/london_sex_age_totals.csv.

Replaces the old projection (proj2_*) and components-of-change pipelines, which read from
separate parquet exports. This script reads only the single CSV and writes:
  - src/lib/data/londonPopulationTotal.json   total population per year
  - src/lib/data/londonAgeStructure.json      population per single year of age, latest year
  - src/lib/data/londonAgeGroups.json         primary/secondary school age + 65-plus per year
  - src/lib/data/londonComponentsOfChange.json births/deaths/migration per year

Usage: python3 scripts/build_london_from_single_source.py /path/to/london_sex_age_totals.csv
"""

import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "src/lib/data"
DEFAULT_INPUT = Path("/Users/user1/Downloads/london_sex_age_totals.csv")
YEARS = range(2011, 2026)
COMPONENT_YEARS = range(2012, 2026)
LATEST_YEAR = 2025

PRIMARY_SCHOOL_AGE = (5, 10)
SECONDARY_SCHOOL_AGE = (11, 15)
OLDER_AGE = (65, 90)


def read_source(path: Path) -> pd.DataFrame:
    if path.suffix.lower() != ".csv":
        raise ValueError(f"Only the London totals CSV is supported: {path}")

    df = pd.read_csv(path)
    df["sex"] = df["sex"].astype(str).str.lower()
    df["age"] = pd.to_numeric(df["age"], errors="coerce").fillna(0).astype(int)
    return df[df["sex"].isin(["f", "m"])].copy()


def write_json(rows: list[dict], out: Path) -> None:
    out.write_text(json.dumps(rows, indent=1) + "\n")
    print(f"Wrote {len(rows)} rows to {out}")


def build_population_total(df: pd.DataFrame) -> list[dict]:
    rows = []
    for year in YEARS:
        col = f"population_{year}"
        if col not in df.columns:
            continue
        rows.append(
            {
                "dataset": "london_population_total",
                "xd": f"{year}-01-01",
                "b": "London",
                "y": float(df[col].sum()),
            }
        )
    return rows


def build_age_structure(df: pd.DataFrame) -> list[dict]:
    col = f"population_{LATEST_YEAR}"
    grouped = df.groupby("age", as_index=False)[col].sum()
    return [
        {
            "dataset": "london_age_structure",
            "xd": int(age),
            "b": str(LATEST_YEAR),
            "y": float(value),
        }
        for age, value in grouped.itertuples(index=False, name=None)
    ]


def build_age_groups(df: pd.DataFrame) -> list[dict]:
    rows = []
    specs = [
        ("london_primary_school_age", PRIMARY_SCHOOL_AGE),
        ("london_secondary_school_age", SECONDARY_SCHOOL_AGE),
        ("london_population_age_65_plus", OLDER_AGE),
    ]
    for year in YEARS:
        col = f"population_{year}"
        if col not in df.columns:
            continue
        for dataset, (low, high) in specs:
            value = float(df.loc[df["age"].between(low, high), col].sum())
            rows.append({"dataset": dataset, "xd": f"{year}-01-01", "b": "London", "y": value})
    return rows


def build_components_of_change(df: pd.DataFrame) -> list[dict]:
    rows = []
    for year in COMPONENT_YEARS:
        births_col = f"births_{year}"
        deaths_col = f"deaths_{year}"
        internal_net_col = f"internal_net_{year}"
        international_net_col = f"international_net_{year}"
        if births_col not in df.columns:
            continue

        births = float(df[births_col].sum())
        deaths = float(df[deaths_col].sum())
        internal_net = float(df[internal_net_col].sum())
        international_net = float(df[international_net_col].sum())
        xd = f"{year}-01-01"

        rows.append({"dataset": "london_births", "xd": xd, "b": "London", "y": births})
        rows.append({"dataset": "london_deaths", "xd": xd, "b": "London", "y": deaths})
        rows.append({"dataset": "london_natural_change", "xd": xd, "b": "London", "y": births - deaths})
        rows.append({"dataset": "london_domestic_net_migration", "xd": xd, "b": "London", "y": internal_net})
        rows.append(
            {"dataset": "london_international_net_migration", "xd": xd, "b": "London", "y": international_net}
        )
        rows.append(
            {
                "dataset": "london_total_net_migration",
                "xd": xd,
                "b": "London",
                "y": internal_net + international_net,
            }
        )
    return rows


def main() -> None:
    source = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_INPUT
    if not source.exists():
        raise FileNotFoundError(f"Missing source CSV: {source}")

    df = read_source(source)

    write_json(build_population_total(df), DATA_DIR / "londonPopulationTotal.json")
    write_json(build_age_structure(df), DATA_DIR / "londonAgeStructure.json")
    write_json(build_age_groups(df), DATA_DIR / "londonAgeGroups.json")
    write_json(build_components_of_change(df), DATA_DIR / "londonComponentsOfChange.json")


if __name__ == "__main__":
    main()
