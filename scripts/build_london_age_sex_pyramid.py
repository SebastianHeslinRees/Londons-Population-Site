"""Build src/lib/data/londonAgeSexPyramidData.json from the canonical London sex-age totals CSV.

The dashboard's age pyramid is derived exclusively from the London totals CSV supplied at
/Users/user1/Downloads/london_sex_age_totals.csv.

Usage: python3 scripts/build_london_age_sex_pyramid.py /path/to/london_sex_age_totals.csv
"""

import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "src/lib/data/londonAgeSexPyramidData.json"
DEFAULT_INPUT = Path("/Users/user1/Downloads/london_sex_age_totals.csv")
YEARS = range(2011, 2026)
AGE_BAND_WIDTH = 5
MAX_AGE_BAND_START = 90


def age_band(age: int) -> str:
    if age >= MAX_AGE_BAND_START:
        return f"{MAX_AGE_BAND_START}+"
    start = (age // AGE_BAND_WIDTH) * AGE_BAND_WIDTH
    return f"{start}-{start + AGE_BAND_WIDTH - 1}"


def read_source(path: Path) -> pd.DataFrame:
    if path.suffix.lower() != ".csv":
        raise ValueError(f"Only the London totals CSV is supported: {path}")

    df = pd.read_csv(path)
    df["sex"] = df["sex"].astype(str).str.lower()
    df["age"] = pd.to_numeric(df["age"], errors="coerce").fillna(0).astype(int)
    return df[df["sex"].isin(["f", "m"])].copy()


def main() -> None:
    source = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_INPUT
    if not source.exists():
        raise FileNotFoundError(f"Missing source CSV: {source}")

    df = read_source(source)
    df = df[["sex", "age"] + [c for c in df.columns if c.startswith("population_")]].copy()

    df["age"] = pd.to_numeric(df["age"], errors="coerce").fillna(0).astype(int)

    rows = []
    for year in YEARS:
        col = f"population_{year}"
        if col not in df.columns:
            continue

        work = df[["sex", "age", col]].copy()
        work["age_band"] = work["age"].apply(age_band)
        grouped = work.groupby(["age_band", "sex"], as_index=False)[col].sum()
        for age_band_value, sex_value, value in grouped.itertuples(index=False, name=None):
            sex_label = {"f": "Female", "m": "Male"}.get(str(sex_value).lower(), str(sex_value).capitalize())
            rows.append(
                {
                    "dataset": "london_age_sex_pyramid",
                    "xd": age_band_value,
                    "b": f"{year}|{sex_label}",
                    "y": float(value),
                }
            )

    OUT.write_text(json.dumps(rows, indent=1) + "\n")
    print(f"Wrote {len(rows)} rows to {OUT}")


if __name__ == "__main__":
    main()
