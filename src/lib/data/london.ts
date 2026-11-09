import type { ChartDataRow } from '@ldn-viz/charts';

import londonAgeGroups from '$lib/data/londonAgeGroups.json' with { type: 'json' };
import londonAgeSexPyramid from '$lib/data/londonAgeSexPyramidData.json' with { type: 'json' };
import londonAgeStructure from '$lib/data/londonAgeStructure.json' with { type: 'json' };
import londonComponentsOfChange from '$lib/data/londonComponentsOfChange.json' with { type: 'json' };
import londonPopulationBySex from '$lib/data/londonPopulationBySex.json' with { type: 'json' };
import londonPopulationTotal from '$lib/data/londonPopulationTotal.json' with { type: 'json' };

type SourceRow = { dataset: string; xd: string | number; b: string; y: number };

/** All datasets are derived from the London sex-age-component totals CSV, up to this year. */
export const LATEST_YEAR = 2025;

const populationTotalRows = londonPopulationTotal as SourceRow[];
const ageGroupRows = londonAgeGroups as SourceRow[];
const componentRows = londonComponentsOfChange as SourceRow[];
const ageSexPyramidRows = londonAgeSexPyramid as SourceRow[];

const yearOf = (xd: string | number) => Number(String(xd).slice(0, 4));

const series = (rows: SourceRow[], dataset: string, label: string): ChartDataRow[] =>
	rows
		.filter((r) => r.dataset === dataset && yearOf(r.xd) <= LATEST_YEAR)
		.map((r) => ({ dataset, xd: r.xd, b: label, y: r.y }));

const relabel = (rows: ChartDataRow[], dataset: string): ChartDataRow[] =>
	rows.map((r) => ({ ...r, dataset }));

/** Year-over-year change in total population, derived from the population totals series. */
const annualChangeRows: SourceRow[] = populationTotalRows
	.filter((r) => r.dataset === 'london_population_total')
	.slice()
	.sort((a, b) => yearOf(a.xd) - yearOf(b.xd))
	.map((r, index, arr) =>
		index === 0
			? null
			: { dataset: 'london_annual_change', xd: r.xd, b: 'London', y: r.y - arr[index - 1].y }
	)
	.filter((r): r is SourceRow => r !== null);

export const datasets: Record<string, ChartDataRow[]> = {
	london_population: series(populationTotalRows, 'london_population_total', 'London'),
	london_annual_change: series(annualChangeRows, 'london_annual_change', 'London'),
	london_population_by_sex: relabel(
		(londonPopulationBySex as ChartDataRow[]).map((row) => ({
			...row,
			xd: new Date(String(row.xd))
		})),
		'london_population_by_sex'
	),
	london_births_deaths: relabel(
		[
			...series(componentRows, 'london_births', 'Births'),
			...series(componentRows, 'london_deaths', 'Deaths')
		],
		'london_births_deaths'
	),
	london_natural_change: series(componentRows, 'london_natural_change', 'London'),
	london_net_migration: relabel(
		[
			...series(componentRows, 'london_international_net_migration', 'International'),
			...series(componentRows, 'london_domestic_net_migration', 'Domestic'),
			...series(componentRows, 'london_total_net_migration', 'Total')
		],
		'london_net_migration'
	),
	london_age_structure: (londonAgeStructure as SourceRow[]).map((r) => ({
		dataset: 'london_age_structure',
		xd: r.xd,
		b: String(LATEST_YEAR),
		y: r.y
	})),
	london_age_groups: relabel(
		[
			...series(ageGroupRows, 'london_primary_school_age', 'Primary school'),
			...series(ageGroupRows, 'london_secondary_school_age', 'Secondary school'),
			...series(ageGroupRows, 'london_population_age_65_plus', '65 and over')
		],
		'london_age_groups'
	)
};

export type AgeSexPyramidRow = { year: number; ageBand: string; sex: 'Female' | 'Male'; value: number };

/** Population by 5-year age band and sex, one row per year/age band/sex (2001-{LATEST_YEAR}). */
export const ageSexPyramidData: AgeSexPyramidRow[] = ageSexPyramidRows.map((r) => {
	const [yearLabel, rawSex] = r.b.split('|');
	const sex =
		rawSex === 'F' || rawSex === 'Female'
			? 'Female'
			: rawSex === 'M' || rawSex === 'Male'
				? 'Male'
				: (rawSex as 'Female' | 'Male');
	return { year: Number(yearLabel), ageBand: String(r.xd), sex, value: r.y };
});

export const ageSexPyramidYears: number[] = [...new Set(ageSexPyramidData.map((r) => r.year))].sort(
	(a, b) => a - b
);

/** Earliest year available in the source CSV; used in place of the old 2001 baseline. */
export const EARLIEST_YEAR = 2011;

const at = (rows: SourceRow[], dataset: string, year: number) => {
	const row = rows.find((r) => r.dataset === dataset && yearOf(r.xd) === year);
	if (!row) throw new Error(`No ${dataset} value for ${year}`);
	return row.y;
};

const pair = (rows: SourceRow[], dataset: string) => ({
	now: at(rows, dataset, LATEST_YEAR),
	prev: at(rows, dataset, LATEST_YEAR - 1)
});

const extreme = (rows: SourceRow[], dataset: string, pick: 'min' | 'max') => {
	const history = rows.filter((r) => r.dataset === dataset && yearOf(r.xd) <= LATEST_YEAR);
	const best = history.reduce((a, b) => ((pick === 'min' ? b.y < a.y : b.y > a.y) ? b : a));
	return { year: yearOf(best.xd), value: best.y };
};

const ageRows = datasets.london_age_structure.map((r) => ({ age: r.xd as number, y: r.y }));
const totalByAge = (test: (age: number) => boolean) =>
	ageRows.filter((r) => test(r.age)).reduce((sum, r) => sum + r.y, 0);

const medianAge = (() => {
	const total = totalByAge(() => true);
	let cumulative = 0;
	for (const r of ageRows) {
		cumulative += r.y;
		if (cumulative >= total / 2) return r.age;
	}
	return NaN;
})();

const olderNow = at(ageGroupRows, 'london_population_age_65_plus', LATEST_YEAR);
const olderThen = at(ageGroupRows, 'london_population_age_65_plus', EARLIEST_YEAR);
const populationNow = at(populationTotalRows, 'london_population_total', LATEST_YEAR);
const populationThen = at(populationTotalRows, 'london_population_total', EARLIEST_YEAR);

export const figures = {
	year: LATEST_YEAR,
	population: pair(populationTotalRows, 'london_population_total'),
	populationChange: pair(annualChangeRows, 'london_annual_change'),
	populationEarliestYear: populationThen,
	population2019: at(populationTotalRows, 'london_population_total', 2019),
	population2021: at(populationTotalRows, 'london_population_total', 2021),
	change2020: at(annualChangeRows, 'london_annual_change', 2020),
	change2021: at(annualChangeRows, 'london_annual_change', 2021),
	change2022: at(annualChangeRows, 'london_annual_change', 2022),
	births: pair(componentRows, 'london_births'),
	deaths: pair(componentRows, 'london_deaths'),
	naturalChange: pair(componentRows, 'london_natural_change'),
	domestic: pair(componentRows, 'london_domestic_net_migration'),
	international: pair(componentRows, 'london_international_net_migration'),
	totalMigration: pair(componentRows, 'london_total_net_migration'),
	international2021: at(componentRows, 'london_international_net_migration', 2021),
	international2022: at(componentRows, 'london_international_net_migration', 2022),
	peakDomesticOutflow: extreme(componentRows, 'london_domestic_net_migration', 'min'),
	peakInternational: extreme(componentRows, 'london_international_net_migration', 'max'),
	primarySchoolAge: {
		...pair(ageGroupRows, 'london_primary_school_age'),
		peak: extreme(ageGroupRows, 'london_primary_school_age', 'max')
	},
	secondarySchoolAge: {
		...pair(ageGroupRows, 'london_secondary_school_age'),
		peak: extreme(ageGroupRows, 'london_secondary_school_age', 'max')
	},
	older: { now: olderNow, then: olderThen },
	olderShare: olderNow / populationNow,
	olderShareEarliestYear: olderThen / populationThen,
	under18: totalByAge((age) => age < 18),
	aged18to64: totalByAge((age) => age >= 18 && age < 65),
	dependencyRatio: (totalByAge((age) => age < 18) + olderNow) / totalByAge((age) => age >= 18 && age < 65),
	medianAge
};

/** 1234567 -> "1,234,567" */
export const formatNumber = (value: number) => Math.round(value).toLocaleString('en-GB');

/** Rounds to the nearest hundred, as used in the headline figures. */
export const formatRounded = (value: number) => formatNumber(Math.round(value / 100) * 100);

export const formatMillions = (value: number) => `${(value / 1_000_000).toFixed(3)} million`;

export const formatPercent = (fraction: number) => `${(Math.abs(fraction) * 100).toFixed(1)}%`;

/** "+55,100" / "-128,200" */
export const formatSigned = (value: number) =>
	`${value < 0 ? '-' : '+'}${formatRounded(Math.abs(value))}`;

/** Size of the change from `prev` to `now`, e.g. "6.9% higher". */
export const compare = (now: number, prev: number) =>
	`${formatPercent((now - prev) / Math.abs(prev))} ${now > prev ? 'higher' : 'lower'}`;
