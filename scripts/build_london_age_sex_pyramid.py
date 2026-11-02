"""Build src/lib/data/londonAgeSexPyramidData.json (London population by 5-year age band and sex, 2001-2024).

Reads the central-variant region population parquet files (single year of age, by sex)
and aggregates into 5-year age bands for each mid-year estimate up to LATEST_YEAR.
Later years in the source are projections and are not included.

Usage: python3 scripts/build_london_age_sex_pyramid.py
"""

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
SOURCE_ROOT = Path('/Users/user1/Downloads/trend_core_outputs_parquet_24august-2/variant=central/geography=region/component=population')
OUT = ROOT / 'src/lib/data/londonAgeSexPyramidData.json'
LONDON_GSS_CODE = 'E12000007'
LATEST_YEAR = 2024
YEARS = range(2001, LATEST_YEAR + 1)

AGE_BAND_WIDTH = 5
MAX_AGE_BAND_START = 90  # bands: 0-4, 5-9, ..., 85-89, 90+


def age_band(age: float) -> str:
    age = int(age)
    if age >= MAX_AGE_BAND_START:
        return f'{MAX_AGE_BAND_START}+'
    start = (age // AGE_BAND_WIDTH) * AGE_BAND_WIDTH
    return f'{start}-{start + AGE_BAND_WIDTH - 1}'


def main() -> None:
    rows = []
    for year in YEARS:
        year_dir = SOURCE_ROOT / f'year={year}'
        parquet_file = next(year_dir.glob('*.parquet'))
        frame = pd.read_parquet(parquet_file)
        london = frame[frame['gss_code'] == LONDON_GSS_CODE].copy()
        if london.empty:
            raise RuntimeError(f'No London rows found for {year}')

        london['age_band'] = london['age'].apply(age_band)
        grouped = london.groupby(['age_band', 'sex'], as_index=False)['value'].sum()

        for row in grouped.itertuples(index=False):
            rows.append(
                {
                    'dataset': 'london_age_sex_pyramid',
                    'xd': row.age_band,
                    'b': f'{year}|{row.sex.capitalize()}',
                    'y': float(row.value),
                }
            )

    OUT.write_text(json.dumps(rows, indent=1) + '\n')
    print(f'Wrote {len(rows)} rows to {OUT}')


if __name__ == '__main__':
    main()
