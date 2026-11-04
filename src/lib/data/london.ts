import type { ChartDataRow } from '@ldn-viz/charts';

import componentsOfChange from '$lib/data/ComponentsOfChangeChartData.json' with { type: 'json' };
import londonAgeSexPyramid from '$lib/data/londonAgeSexPyramidData.json' with { type: 'json' };
import londonPopulationBySex from '$lib/data/londonPopulationBySex.json' with { type: 'json' };
import population from '$lib/data/projectedPopulation2ChartData.json' with { type: 'json' };

type SourceRow = { dataset: string; xd: string | number; b: string; y: number };

/** Latest mid-year estimate; later years in the source files are projections and are not used. */
export const LATEST_YEAR = 2024;

const populationRows = population as SourceRow[];
const componentRows = componentsOfChange as SourceRow[];
const ageSexPyramidRows = londonAgeSexPyramid as SourceRow[];

const yearOf = (xd: string | number) => Number(String(xd).slice(0, 4));

// Estimates are identical across projection variants, so 'Central' is used for all of them.
const estimates = (rows: SourceRow[], dataset: string, label: string): ChartDataRow[] =>
	rows
		.filter((r) => r.dataset === dataset && r.b === 'Central' && yearOf(r.xd) <= LATEST_YEAR)
		.map((r) => ({ dataset, xd: r.xd, b: label, y: r.y }));

const relabel = (rows: ChartDataRow[], dataset: string): ChartDataRow[] =>
	rows.map((r) => ({ ...r, dataset }));

export const datasets: Record<string, ChartDataRow[]> = {
	london_population: estimates(populationRows, 'proj2_total_population', 'London'),
	london_population_by_sex: relabel(
		(londonPopulationBySex as ChartDataRow[]).map((row) => ({
			...row,
			xd: new Date(String(row.xd))
		})),
		'london_population_by_sex'
	),
	london_annual_change: estimates(populationRows, 'proj2_annual_population_change', 'London'),
	london_births_deaths: relabel(
		[
			...estimates(componentRows, 'births', 'Births'),
			...estimates(componentRows, 'deaths', 'Deaths')
		],
		'london_births_deaths'
	),
	london_natural_change: estimates(componentRows, 'natural_change', 'London'),
	london_net_migration: relabel(
		[
			...estimates(componentRows, 'international_net_migration', 'International'),
			...estimates(componentRows, 'domestic_net_migration', 'Domestic'),
			...estimates(componentRows, 'total_net_migration', 'Total')
		],
		'london_net_migration'
	),
	london_age_structure: populationRows
		.filter((r) => r.dataset === 'proj2_age_structure_median_age' && r.b === '2024 structure')
		.map((r) => ({ dataset: 'london_age_structure', xd: r.xd, b: String(LATEST_YEAR), y: r.y })),
	london_age_groups: relabel(
		[
			...estimates(populationRows, 'proj2_primary_school_age_children', 'Primary school'),
			...estimates(populationRows, 'proj2_secondary_school_age_children', 'Secondary school'),
			...estimates(populationRows, 'proj2_population_age_65_plus', '65 and over')
		],
		'london_age_groups'
	)
};

export type AgeSexPyramidRow = { year: number; ageBand: string; sex: 'Female' | 'Male'; value: number };

/** Population by 5-year age band and sex, one row per year/age band/sex (2001-{LATEST_YEAR}). */
export const ageSexPyramidData: AgeSexPyramidRow[] = ageSexPyramidRows.map((r) => {
	const [yearLabel, sex] = r.b.split('|');
	return { year: Number(yearLabel), ageBand: String(r.xd), sex: sex as 'Female' | 'Male', value: r.y };
});

export const ageSexPyramidYears: number[] = [...new Set(ageSexPyramidData.map((r) => r.year))].sort(
	(a, b) => a - b
);

const at = (rows: SourceRow[], dataset: string, year: number) => {
	const row = rows.find(
		(r) => r.dataset === dataset && r.b === 'Central' && yearOf(r.xd) === year
	);
	if (!row) throw new Error(`No ${dataset} value for ${year}`);
	return row.y;
};

const pair = (rows: SourceRow[], dataset: string) => ({
	now: at(rows, dataset, LATEST_YEAR),
	prev: at(rows, dataset, LATEST_YEAR - 1)
});

const extreme = (rows: SourceRow[], dataset: string, pick: 'min' | 'max') => {
	const history = rows.filter(
		(r) => r.dataset === dataset && r.b === 'Central' && yearOf(r.xd) <= LATEST_YEAR
	);
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

const olderNow = at(populationRows, 'proj2_population_age_65_plus', LATEST_YEAR);
const olderThen = at(populationRows, 'proj2_population_age_65_plus', 2001);
const populationNow = at(populationRows, 'proj2_total_population', LATEST_YEAR);
const populationThen = at(populationRows, 'proj2_total_population', 2001);

export const figures = {
	year: LATEST_YEAR,
	population: pair(populationRows, 'proj2_total_population'),
	populationChange: pair(populationRows, 'proj2_annual_population_change'),
	population2001: populationThen,
	population2019: at(populationRows, 'proj2_total_population', 2019),
	population2021: at(populationRows, 'proj2_total_population', 2021),
	change2020: at(populationRows, 'proj2_annual_population_change', 2020),
	change2021: at(populationRows, 'proj2_annual_population_change', 2021),
	change2022: at(populationRows, 'proj2_annual_population_change', 2022),
	births: pair(componentRows, 'births'),
	deaths: pair(componentRows, 'deaths'),
	naturalChange: pair(componentRows, 'natural_change'),
	domestic: pair(componentRows, 'domestic_net_migration'),
	international: pair(componentRows, 'international_net_migration'),
	totalMigration: pair(componentRows, 'total_net_migration'),
	international2021: at(componentRows, 'international_net_migration', 2021),
	international2022: at(componentRows, 'international_net_migration', 2022),
	peakDomesticOutflow: extreme(componentRows, 'domestic_net_migration', 'min'),
	peakInternational: extreme(componentRows, 'international_net_migration', 'max'),
	primarySchoolAge: {
		...pair(populationRows, 'proj2_primary_school_age_children'),
		peak: extreme(populationRows, 'proj2_primary_school_age_children', 'max')
	},
	secondarySchoolAge: {
		...pair(populationRows, 'proj2_secondary_school_age_children'),
		peak: extreme(populationRows, 'proj2_secondary_school_age_children', 'max')
	},
	older: { now: olderNow, then: olderThen },
	olderShare: olderNow / populationNow,
	olderShare2001: olderThen / populationThen,
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
