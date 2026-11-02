from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd


LONDON_GSS_CODE = 'E12000007'

SOURCE_ROOT = Path('/Users/user1/Downloads/20260825_explorer_tool')
DATA_DIR = Path('src/lib/data')
HOUSING_OUTPUT = DATA_DIR / 'housingLedProjectedPopulation.json'
COMPARISON_OUTPUT = DATA_DIR / 'housingLedVsTrendProjectionData.json'
TREND_INPUT = DATA_DIR / 'projectedPopulation2ChartData.json'

VARIANT_SPECS = [
    ('variant=central_ward', 'Central'),
    ('variant=high_ward', 'High'),
    ('variant=low_ward', 'Low'),
]


def read_year_frame(year_path: Path) -> pd.DataFrame:
    parquet_file = next(year_path.glob('*.parquet'))
    return pd.read_parquet(parquet_file)


def london_only_frame(frame: pd.DataFrame) -> pd.DataFrame:
    london_frame = frame.loc[frame['gss_code'] == LONDON_GSS_CODE].copy()
    if london_frame.empty:
        raise RuntimeError(f'No London rows found in {frame}')
    return london_frame


def build_housing_rows() -> tuple[list[dict], list[dict]]:
    rows_by_dataset = {
        'housing_led_projected_population': [],
        'housing_led_total_population': [],
        'housing_led_annual_population_change': [],
        'housing_led_age_structure_median_age': [],
        'housing_led_working_age_population': [],
        'housing_led_primary_school_age_children': [],
        'housing_led_secondary_school_age_children': [],
        'housing_led_population_age_65_plus': [],
    }
    report_rows: list[dict] = []

    for variant_dir_name, variant_label in VARIANT_SPECS:
        component_root = SOURCE_ROOT / variant_dir_name / 'geography=region' / 'component=population'
        year_dirs = sorted(component_root.glob('year=*'))
        if not year_dirs:
            raise RuntimeError(f'No year folders found under {component_root}')

        yearly_totals: list[tuple[int, float]] = []

        for year_dir in year_dirs:
            year = int(year_dir.name.split('=')[1])
            frame = read_year_frame(year_dir)
            london_frame = london_only_frame(frame)

            london_total = float(london_frame['value'].sum())
            all_total = float(frame['value'].sum())
            yearly_totals.append((year, london_total))
            report_rows.append(
                {
                    'variant': variant_label,
                    'year': year,
                    'london_total': london_total,
                    'all_regions_total': all_total,
                    'inflation_factor': all_total / london_total if london_total else None,
                }
            )

            for dataset_name in ['housing_led_projected_population', 'housing_led_total_population']:
                rows_by_dataset[dataset_name].append(
                    {
                        'dataset': dataset_name,
                        'xd': f'{year:04d}-01-01',
                        'b': variant_label,
                        'y': london_total,
                    }
                )

            def sum_age_group(age_min: int, age_max: int) -> float:
                mask = london_frame['age'].between(age_min, age_max, inclusive='both')
                return float(london_frame.loc[mask, 'value'].sum())

            rows_by_dataset['housing_led_working_age_population'].append(
                {
                    'dataset': 'housing_led_working_age_population',
                    'xd': f'{year:04d}-01-01',
                    'b': variant_label,
                    'y': sum_age_group(16, 64),
                }
            )
            rows_by_dataset['housing_led_primary_school_age_children'].append(
                {
                    'dataset': 'housing_led_primary_school_age_children',
                    'xd': f'{year:04d}-01-01',
                    'b': variant_label,
                    'y': sum_age_group(5, 10),
                }
            )
            rows_by_dataset['housing_led_secondary_school_age_children'].append(
                {
                    'dataset': 'housing_led_secondary_school_age_children',
                    'xd': f'{year:04d}-01-01',
                    'b': variant_label,
                    'y': sum_age_group(11, 15),
                }
            )
            rows_by_dataset['housing_led_population_age_65_plus'].append(
                {
                    'dataset': 'housing_led_population_age_65_plus',
                    'xd': f'{year:04d}-01-01',
                    'b': variant_label,
                    'y': sum_age_group(65, 90),
                }
            )

        age_structure_year = 2046
        age_structure_dir = component_root / f'year={age_structure_year}'
        if not age_structure_dir.exists():
            raise RuntimeError(f'No housing-led age structure data found for year {age_structure_year}')

        age_frame = london_only_frame(read_year_frame(age_structure_dir))

        for age in sorted(age_frame['age'].unique()):
            age_total = float(age_frame.loc[age_frame['age'] == age, 'value'].sum())
            rows_by_dataset['housing_led_age_structure_median_age'].append(
                {
                    'dataset': 'housing_led_age_structure_median_age',
                    'xd': int(age),
                    'b': variant_label,
                    'y': age_total,
                }
            )

        for index, (year, total) in enumerate(sorted(yearly_totals)):
            previous_total = yearly_totals[index - 1][1] if index else total
            rows_by_dataset['housing_led_annual_population_change'].append(
                {
                    'dataset': 'housing_led_annual_population_change',
                    'xd': f'{year:04d}-01-01',
                    'b': variant_label,
                    'y': total - previous_total,
                }
            )

        report_rows.append(
            {
                'variant': variant_label,
                'year': age_structure_year,
                'london_total': yearly_totals[-1][1],
                'note': 'latest_year',
            }
        )

    baseline_year = 2024
    baseline_variant_dir = SOURCE_ROOT / VARIANT_SPECS[0][0] / 'geography=region' / 'component=population' / f'year={baseline_year}'
    if not baseline_variant_dir.exists():
        raise RuntimeError(f'No housing-led baseline age structure data found for year {baseline_year}')

    baseline_frame = london_only_frame(read_year_frame(baseline_variant_dir))
    for age in sorted(baseline_frame['age'].unique()):
        rows_by_dataset['housing_led_age_structure_median_age'].append(
            {
                'dataset': 'housing_led_age_structure_median_age',
                'xd': int(age),
                'b': '2024 structure',
                'y': float(baseline_frame.loc[baseline_frame['age'] == age, 'value'].sum()),
            }
        )

    combined_rows: list[dict] = []
    for dataset_rows in rows_by_dataset.values():
        combined_rows.extend(dataset_rows)

    return combined_rows, report_rows


def build_comparison_rows(trend_rows: list[dict], housing_rows: list[dict]) -> list[dict]:
    trend_dataset_map = {
        'proj2_total_population': 'housing_led_vs_trend_total_population',
        'proj2_annual_population_change': 'housing_led_vs_trend_annual_population_change',
        'proj2_age_structure_median_age': 'housing_led_vs_trend_age_structure',
        'proj2_working_age_population': 'housing_led_vs_trend_working_age_population',
        'proj2_primary_school_age_children': 'housing_led_vs_trend_primary_school_age_children',
        'proj2_secondary_school_age_children': 'housing_led_vs_trend_secondary_school_age_children',
        'proj2_population_age_65_plus': 'housing_led_vs_trend_population_age_65_plus',
    }

    housing_dataset_map = {
        'housing_led_total_population': 'housing_led_vs_trend_total_population',
        'housing_led_annual_population_change': 'housing_led_vs_trend_annual_population_change',
        'housing_led_age_structure_median_age': 'housing_led_vs_trend_age_structure',
        'housing_led_working_age_population': 'housing_led_vs_trend_working_age_population',
        'housing_led_primary_school_age_children': 'housing_led_vs_trend_primary_school_age_children',
        'housing_led_secondary_school_age_children': 'housing_led_vs_trend_secondary_school_age_children',
        'housing_led_population_age_65_plus': 'housing_led_vs_trend_population_age_65_plus',
    }

    combined_rows: list[dict] = []

    for row in trend_rows:
        dataset = trend_dataset_map.get(row.get('dataset', ''))
        if dataset:
            combined_rows.append({**row, 'dataset': dataset, 'b': f"Trend - {row['b']}"})

    for row in housing_rows:
        dataset = housing_dataset_map.get(row.get('dataset', ''))
        if dataset:
            combined_rows.append({**row, 'dataset': dataset, 'b': f"Housing-led - {row['b']}"})

    return combined_rows


def main() -> None:
    parser = argparse.ArgumentParser(description='Investigate and rebuild the housing-led projection data.')
    parser.add_argument('--report-only', action='store_true', help='Print the investigation report without writing files.')
    args = parser.parse_args()

    housing_rows, report_rows = build_housing_rows()
    trend_rows = json.loads(TREND_INPUT.read_text())
    comparison_rows = build_comparison_rows(trend_rows, housing_rows)

    print('Housing-led investigation report')
    print('London geography filter:', LONDON_GSS_CODE)
    for row in report_rows:
        if 'year' in row and 'london_total' in row and 'all_regions_total' in row:
            print(
                f"{row['variant']:<16} {row['year']} london={row['london_total']:.1f} "
                f"all_regions={row['all_regions_total']:.1f} inflation={row['inflation_factor']:.2f}"
            )

    if args.report_only:
        return

    HOUSING_OUTPUT.write_text(json.dumps(housing_rows, indent=2))
    COMPARISON_OUTPUT.write_text(json.dumps(comparison_rows, indent=2))
    print(f'wrote {HOUSING_OUTPUT} ({len(housing_rows)} rows)')
    print(f'wrote {COMPARISON_OUTPUT} ({len(comparison_rows)} rows)')


if __name__ == '__main__':
    main()