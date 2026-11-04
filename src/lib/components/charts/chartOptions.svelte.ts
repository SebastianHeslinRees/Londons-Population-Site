import type { ChartOptions } from '@ldn-viz/charts';
import { theme } from '@ldn-viz/ui';

const colorsBirthsDeaths = $derived({
	colorScale: {
		domain: ['Births', 'Deaths'],
		range: [
			theme.tokenNameToValue('palette.blue.500'),
			theme.tokenNameToValue('palette.darkpink.500')
		]
	}
});

const colorsMigration = $derived({
	colorScale: {
		domain: ['International', 'Domestic', 'Total'],
		range: [
			theme.tokenNameToValue('palette.blue.500'),
			theme.tokenNameToValue('palette.darkpink.500'),
			theme.tokenNameToValue('data.context')
		]
	}
});

const colorsAgeGroups = $derived({
	colorScale: {
		domain: ['Primary school', 'Secondary school', '65 and over'],
		range: [
			theme.tokenNameToValue('palette.blue.300'),
			theme.tokenNameToValue('palette.blue.700'),
			theme.tokenNameToValue('palette.darkpink.500')
		]
	}
});

const colorsSex = $derived({
	colorScale: {
		domain: ['Female', 'Male'],
		range: [
			theme.tokenNameToValue('palette.darkpink.500'),
			theme.tokenNameToValue('palette.blue.500')
		]
	}
});

class ChartOptionsClass {
	options: Record<string, ChartOptions> = $derived({
		london_population: {
			chartType: 'lineChartWithForecast',
			type: 'date',
			ytickformat: '.2s',
			tooltipFormatValue: ',.0f',
			timeperiod_type: 'Annual',
			yDomain: [7000000, 9500000]
		},

		london_population_by_sex: {
			chartType: 'lineChartWithForecast',
			type: 'date',
			ytickformat: '.2s',
			tooltipFormatValue: ',.0f',
			timeperiod_type: 'Annual',
			autoDodgeLabels: true,
			...colorsSex
		},

		london_annual_change: {
			chartType: 'lineChartWithForecast',
			type: 'date',
			ytickformat: '.2s',
			tooltipFormatValue: ',.0f',
			timeperiod_type: 'Annual',
			includeZeroLine: true,
			numTicks: 4
		},

		london_births_deaths: {
			chartType: 'lineChartWithForecast',
			type: 'date',
			ytickformat: '.2s',
			tooltipFormatValue: ',.0f',
			timeperiod_type: 'Annual',
			yDomain: [40000, 140000],
			...colorsBirthsDeaths
		},

		london_natural_change: {
			chartType: 'lineChartWithForecast',
			type: 'date',
			ytickformat: '.2s',
			tooltipFormatValue: ',.0f',
			timeperiod_type: 'Annual',
			includeZero: true
		},

		london_net_migration: {
			chartType: 'lineChartWithForecast',
			type: 'date',
			ytickformat: '.2s',
			tooltipFormatValue: ',.0f',
			timeperiod_type: 'Annual',
			includeZeroLine: true,
			autoDodgeLabels: true,
			...colorsMigration
		},

		london_age_structure: {
			chartType: 'lineChartWithForecast',
			type: 'integer',
			ytickformat: '.2s',
			tooltipFormatValue: ',.0f',
			timeperiod_type: 'year',
			includeZero: true,
			xAxisLabel: 'Age'
		},

		london_age_groups: {
			chartType: 'lineChartWithForecast',
			type: 'date',
			ytickformat: '.2s',
			tooltipFormatValue: ',.0f',
			timeperiod_type: 'Annual',
			includeZero: true,
			autoDodgeLabels: true,
			...colorsAgeGroups
		}
	});
}

export const chartOptions = new ChartOptionsClass();
