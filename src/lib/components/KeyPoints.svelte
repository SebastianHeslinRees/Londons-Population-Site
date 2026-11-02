<script lang="ts">
	import {
		figures,
		formatMillions,
		formatPercent,
		formatRounded,
		formatSigned
	} from '$lib/data/london';

	const headline = [
		{
			label: `Mid-${figures.year} population`,
			value: formatMillions(figures.population.now),
			note: 'Estimated usual residents of London'
		},
		{
			label: 'Change on previous mid-year',
			value: formatSigned(figures.populationChange.now),
			note: 'Persons'
		}
	];

	const components = [
		{
			label: 'Births',
			value: formatRounded(figures.births.now),
			note: 'Births in the year'
		},
		{
			label: 'Deaths',
			value: formatRounded(figures.deaths.now),
			note: 'Deaths in the year'
		},
		{
			label: 'Natural change',
			value: formatSigned(figures.naturalChange.now),
			note: 'Births minus deaths'
		},
		{
			label: 'Net domestic migration',
			value: formatSigned(figures.domestic.now),
			note:
				figures.domestic.now < 0
					? 'Outflow to the rest of the UK'
					: 'Inflow from the rest of the UK'
		},
		{
			label: 'Net international migration',
			value: formatSigned(figures.international.now),
			note: figures.international.now < 0 ? 'Outflow overseas' : 'Inflow from overseas'
		},
		{
			label: 'Dependency ratio',
			value: formatPercent(figures.dependencyRatio),
			note: 'Children (<18) and older residents (<65) per 100 working-age adults'
		}
	];
</script>

<div class="not-prose my-6 space-y-6">
	<div class="grid gap-4 sm:grid-cols-2">
		{#each headline as card (card.label)}
			<div
				class="bg-color-container-level-0 border-l-[6px] border-color-surface-accent p-5 shadow-sm ring-1 ring-color-border-muted"
			>
				<p class="product label-sm text-color-text-muted">{card.label}</p>
				<p class="product mt-1 text-4xl font-bold tabular-nums text-color-text">{card.value}</p>
				<p class="product caption mt-1 text-color-text-muted">{card.note}</p>
			</div>
		{/each}
	</div>

	<div>
		<p class="product label-sm mb-2 font-semibold text-color-text">Components of change</p>
		<div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
			{#each components as card (card.label)}
				<div class="bg-color-container-level-0 p-4 shadow-sm ring-1 ring-color-border-muted">
					<p class="product label-sm text-color-text-muted">{card.label}</p>
					<p class="product mt-1 text-2xl font-bold tabular-nums text-color-text">{card.value}</p>
					<p class="product caption mt-1 text-color-text-muted">{card.note}</p>
				</div>
			{/each}
		</div>
	</div>
</div>
