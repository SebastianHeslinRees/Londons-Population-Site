#!/usr/bin/env python3
import json
from pathlib import Path

import pandas as pd

SOURCE_ROOT = Path('/Users/user1/Downloads/20260825_explorer_tool/variant=central_ward/geography=ward22/component=population')
OUTPUT_FILE = Path('src/lib/data/housingLedWardPopulationData.json')


def main() -> None:
    rows: list[dict[str, object]] = []
    for year_dir in sorted(SOURCE_ROOT.glob('year=*')):
        parquet_file = next(year_dir.glob('*.parquet'), None)
        if parquet_file is None:
            continue

        frame = pd.read_parquet(parquet_file)
        if 'area_code' not in frame.columns:
            raise ValueError(f'Missing area_code in {parquet_file}')

        totals = frame.groupby('area_code', as_index=False)['value'].sum()
        year = year_dir.name.split('=')[-1]

        for row in totals.itertuples(index=False):
            rows.append({
                'dataset': 'housing_led_ward_population',
                'xd': row.area_code,
                'b': str(year),
                'y': float(row.value),
            })

    OUTPUT_FILE.write_text(json.dumps(rows, indent=2))
    print(f'Wrote {len(rows)} records to {OUTPUT_FILE}')


if __name__ == '__main__':
    main()
