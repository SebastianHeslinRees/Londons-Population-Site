#!/usr/bin/env python3
"""Create chart-ready JSON for the housing-led components page.

Reads the three housing-led variants from the 2026 explorer export:
- central_ward
- high_ward
- low_ward
and emits Low/Central/High series using the same dataset names as the page.
"""

import json
from pathlib import Path

import pandas as pd

BASE_DIR = Path('/Users/user1/Downloads/20260825_explorer_tool')
OUTPUT_FILE = Path('src/lib/data/HousingLedComponentsData.json')
LONDON_GSS_CODE = 'E12000007'

VARIANT_MAPPING = {
    'variant=central_ward': 'Central',
    'variant=high_ward': 'High',
    'variant=low_ward': 'Low',
}

COMPONENTS = [
    'births',
    'deaths',
    'in_migration',
    'out_migration',
    'net_migration',
    'population',
    'tfr',
    'asfr',
    'births_by_mothers_age',
]


def read_london_total(variant_dir: Path, component: str, year: str) -> float | None:
    component_dir = variant_dir / 'geography=region' / f'component={component}' / f'year={year}'
    parquet_file = next(component_dir.glob('*.parquet'), None)
    if parquet_file is None:
        return None

    frame = pd.read_parquet(parquet_file)
    if 'gss_code' in frame.columns:
        london_rows = frame[frame['gss_code'] == LONDON_GSS_CODE]
    else:
        london_rows = frame

    if london_rows.empty:
        return None

    if component == 'asfr':
        return float(london_rows['value'].mean())

    return float(london_rows['value'].sum())


def add_rows(rows: list[dict[str, object]], dataset: str, year: str, variant_label: str, value: float) -> None:
    rows.append({
        'dataset': dataset,
        'xd': f'{year}-01-01',
        'b': variant_label,
        'y': value,
    })


def main() -> None:
    rows: list[dict[str, object]] = []

    for variant_dir_name, variant_label in VARIANT_MAPPING.items():
        variant_dir = BASE_DIR / variant_dir_name
        if not variant_dir.exists():
            continue

        for component in COMPONENTS:
            component_dir = variant_dir / 'geography=region' / f'component={component}'
            if not component_dir.exists():
                continue

            for year_dir in sorted(component_dir.glob('year=*')):
                year = year_dir.name.split('=')[-1]
                value = read_london_total(variant_dir, component, year)
                if value is None:
                    continue

                dataset_name = f'housing_led_{component}'
                add_rows(rows, dataset_name, year, variant_label, value)

    births_by_variant: dict[str, dict[str, float]] = {
        'Low': {},
        'Central': {},
        'High': {},
    }
    deaths_by_variant: dict[str, dict[str, float]] = {
        'Low': {},
        'Central': {},
        'High': {},
    }

    for row in rows:
        dataset = row['dataset']
        if dataset == 'housing_led_births':
            births_by_variant[str(row['b'])][str(row['xd'])] = float(row['y'])
        elif dataset == 'housing_led_deaths':
            deaths_by_variant[str(row['b'])][str(row['xd'])] = float(row['y'])

    for variant_label in ['Low', 'Central', 'High']:
        for year_key, birth_value in births_by_variant[variant_label].items():
            death_value = deaths_by_variant[variant_label].get(year_key)
            if death_value is not None:
                add_rows(rows, 'housing_led_natural_change', year_key[:4], variant_label, birth_value - death_value)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps(rows, indent=2))
    print(f'Wrote {len(rows)} rows to {OUTPUT_FILE}')


if __name__ == '__main__':
    main()
