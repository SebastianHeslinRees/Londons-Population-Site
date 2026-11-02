"""Build src/lib/data/londonPopulationBySex.json (London population by sex, 2001-2024).

Male/female shares come from the GLA 2024-based projections CSV (London region, all ages).
They are applied to the dashboard's total population series so the two sexes sum to the
total shown elsewhere; the CSV's own totals differ slightly from that series after 2001.

Usage: python3 scripts/build_london_population_by_sex.py path/to/2024_based_population_projections.zip
"""

import collections
import csv
import io
import json
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOTALS = ROOT / "src/lib/data/projectedPopulation2ChartData.json"
OUT = ROOT / "src/lib/data/londonPopulationBySex.json"
LONDON_REGION = "E12000007"
YEARS = range(2001, 2025)

with zipfile.ZipFile(sys.argv[1]) as z:
    name = next(n for n in z.namelist() if n.endswith("2024_ppt_10yr.csv"))
    reader = csv.DictReader(io.TextIOWrapper(z.open(name), encoding="utf-8"))
    by_sex = collections.defaultdict(float)
    for row in reader:
        if (
            row["gss_code"] == LONDON_REGION
            and row["residence_type"] == "total"
            and row["sex"] in ("female", "male")
            and row["age_group"] != "total"
        ):
            for year in YEARS:
                by_sex[(row["sex"], year)] += float(row[str(year)])

totals = {
    int(r["xd"][:4]): r["y"]
    for r in json.loads(TOTALS.read_text())
    if r["dataset"] == "proj2_total_population" and r["b"] == "Central"
}

rows = []
for year in YEARS:
    female_share = by_sex[("female", year)] / (by_sex[("female", year)] + by_sex[("male", year)])
    female = round(totals[year] * female_share)
    for label, value in (("Female", female), ("Male", totals[year] - female)):
        rows.append(
            {"dataset": "london_population_by_sex", "xd": f"{year}-01-01", "b": label, "y": value}
        )

OUT.write_text(json.dumps(rows, indent=1) + "\n")
print(f"Wrote {len(rows)} rows to {OUT}")
