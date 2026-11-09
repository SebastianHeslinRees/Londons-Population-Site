"""Build src/lib/data/londonPopulationBySex.json from the canonical London sex-age totals CSV.

The dashboard's London sex split is derived exclusively from the London totals CSV supplied at
/Users/user1/Downloads/london_sex_age_totals.csv.

Usage: python3 scripts/build_london_population_by_sex.py /path/to/london_sex_age_totals.csv
"""

import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "src/lib/data/londonPopulationBySex.json"
DEFAULT_INPUT = Path("/Users/user1/Downloads/london_sex_age_totals.csv")
YEARS = range(2011, 2026)


def read_source(path: Path) -> pd.DataFrame:
    if path.suffix.lower() != ".csv":
        raise ValueError(f"Only the London totals CSV is supported: {path}")

    df = pd.read_csv(path)
    if "sex" in df.columns:
        df["sex"] = df["sex"].astype(str).str.lower()
    if "age" in df.columns:
        df["age"] = pd.to_numeric(df["age"], errors="coerce").fillna(0).astype(int)
    return df[df["sex"].isin(["f", "m"])].copy()


def main() -> None:
    source = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_INPUT
    if not source.exists():
        raise FileNotFoundError(f"Missing source CSV: {source}")

    df = read_source(source)

    rows = []
    for year in YEARS:
        col = f"population_{year}"
        if col not in df.columns:
            continue

        grouped = df.groupby("sex", as_index=False)[col].sum()
        total = int(grouped[col].sum())
        female = int(grouped.loc[grouped["sex"] == "f", col].sum())
        male = total - female

        for label, value in (("Female", female), ("Male", male)):
            rows.append(
                {"dataset": "london_population_by_sex", "xd": f"{year}-01-01", "b": label, "y": value}
            )

    OUT.write_text(json.dumps(rows, indent=1) + "\n")
    print(f"Wrote {len(rows)} rows to {OUT}")


if __name__ == "__main__":
    main()
