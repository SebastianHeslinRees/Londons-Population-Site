<script lang="ts">
	import { ageSexPyramidData, ageSexPyramidYears, type AgeSexPyramidRow } from '$lib/data/london';

	type Props = {
		title?: string;
		subtitle?: string;
		byline?: string;
	};

	let { title, subtitle, byline }: Props = $props();

	const ageBandOrder = [
		'90+',
		'85-89',
		'80-84',
		'75-79',
		'70-74',
		'65-69',
		'60-64',
		'55-59',
		'50-54',
		'45-49',
		'40-44',
		'35-39',
		'30-34',
		'25-29',
		'20-24',
		'15-19',
		'10-14',
		'5-9',
		'0-4'
	];

	const minYear = ageSexPyramidYears[0];
	const maxYear = ageSexPyramidYears[ageSexPyramidYears.length - 1];

	let selectedYear = $state(maxYear);

	const rowsForYear = $derived(
		ageSexPyramidData.filter((r: AgeSexPyramidRow) => r.year === selectedYear)
	);

	const byAgeBand = $derived(
		ageBandOrder.map((band) => ({
			ageBand: band,
			female: rowsForYear.find((r) => r.ageBand === band && r.sex === 'Female')?.value ?? 0,
			male: rowsForYear.find((r) => r.ageBand === band && r.sex === 'Male')?.value ?? 0
		}))
	);

	const maxValue = $derived(Math.max(1, ...byAgeBand.flatMap((row) => [row.female, row.male])));

	const maleColor = '#00AEEF';
	const femaleColor = '#00577D';

	const formatValue = (value: number) => Math.round(value).toLocaleString('en-GB');

	const width = 640;
	const barAreaWidth = 260;
	const centerGap = 40;
	const rowHeight = 22;
	const chartHeight = ageBandOrder.length * rowHeight;
	const labelWidth = width - 2 * barAreaWidth - centerGap;

	const barWidth = (value: number) => (value / maxValue) * barAreaWidth;

	let tooltip = $state<{ label: string; x: number; y: number } | null>(null);

	const showTooltip = (event: MouseEvent, label: string) => {
		tooltip = {
			label,
			x: event.clientX + 14,
			y: event.clientY - 16
		};
	};

	const hideTooltip = () => {
		tooltip = null;
	};
</script>

<style>
	.pyramid-tooltip {
		position: fixed;
		z-index: 50;
		pointer-events: none;
		transform: translate(0, -100%);
		border: 1px solid rgba(255, 255, 255, 0.15);
		border-radius: 0;
		background: rgba(10, 14, 22, 0.96);
		box-shadow: 0 12px 24px rgba(0, 0, 0, 0.28);
		padding: 0.5rem 0.75rem;
		color: rgb(255 255 255);
		font-size: 0.75rem;
		font-weight: 600;
		line-height: 1.3;
		white-space: nowrap;
	}

	.pyramid-tooltip::after {
		content: '';
		position: absolute;
		left: 50%;
		bottom: -8px;
		transform: translateX(-50%);
		border-width: 8px 8px 0 8px;
		border-style: solid;
		border-color: rgba(10, 14, 22, 0.96) transparent transparent transparent;
	}
</style>

<div class="not-prose my-6 space-y-3">
	{#if title}
		<p class="label-lg product font-semibold text-color-text">{title}</p>
	{/if}
	{#if subtitle}
		<p class="product caption text-color-text-muted">{subtitle}</p>
	{/if}

	<div class="flex items-center gap-3">
		<label for="pyramid-year" class="product label-sm whitespace-nowrap text-color-text-muted">
			Year: <span class="font-semibold text-color-text">{selectedYear}</span>
		</label>
		<input
			id="pyramid-year"
			type="range"
			min={minYear}
			max={maxYear}
			step="1"
			bind:value={selectedYear}
			class="w-full accent-color-surface-accent"
		/>
	</div>

	<svg viewBox="0 0 {width} {chartHeight + 20}" class="w-full">
		<!-- Male (left) -->
		<g>
			{#each byAgeBand as row, i (row.ageBand)}
				<rect
					x={barAreaWidth - barWidth(row.male)}
					y={i * rowHeight}
					width={barWidth(row.male)}
					height={rowHeight - 2}
					fill={maleColor}
					pointer-events="all"
					aria-label={`Year: ${selectedYear}, Male, ${row.ageBand}: ${formatValue(row.male)}`}
					onmouseenter={(event) =>
						showTooltip(event, `Year: ${selectedYear} • Male • ${row.ageBand}: ${formatValue(row.male)}`)}
					onmouseleave={hideTooltip}
					onmousemove={(event) =>
						showTooltip(event, `Year: ${selectedYear} • Male • ${row.ageBand}: ${formatValue(row.male)}`)}
				/>

			{/each}
		</g>

		<!-- Female (right) -->
		<g>
			{#each byAgeBand as row, i (row.ageBand)}
				<rect
					x={barAreaWidth + centerGap}
					y={i * rowHeight}
					width={barWidth(row.female)}
					height={rowHeight - 2}
					fill={femaleColor}
					pointer-events="all"
					aria-label={`Year: ${selectedYear}, Female, ${row.ageBand}: ${formatValue(row.female)}`}
					onmouseenter={(event) =>
						showTooltip(event, `Year: ${selectedYear} • Female • ${row.ageBand}: ${formatValue(row.female)}`)}
					onmouseleave={hideTooltip}
					onmousemove={(event) =>
						showTooltip(event, `Year: ${selectedYear} • Female • ${row.ageBand}: ${formatValue(row.female)}`)}
				/>

			{/each}
		</g>

		<!-- Age band labels -->
		<g>
			{#each ageBandOrder as band, i (band)}
				<text
					x={barAreaWidth + centerGap / 2}
					y={i * rowHeight + (rowHeight - 2) / 2}
					dominant-baseline="middle"
					text-anchor="middle"
					class="fill-color-text-muted text-[10px]"
				>
					{band}
				</text>
			{/each}
		</g>
	</svg>

	{#if tooltip}
		<div
			class="pyramid-tooltip"
			style="left: {tooltip.x}px; top: {tooltip.y}px;"
		>
			{tooltip.label}
		</div>
	{/if}

	<div class="flex items-center justify-center gap-6">
		<span class="product caption flex items-center gap-2 text-color-text-muted">
			<span class="inline-block h-3 w-3" style="background-color: {maleColor}"></span>
			Male
		</span>
		<span class="product caption flex items-center gap-2 text-color-text-muted">
			<span class="inline-block h-3 w-3" style="background-color: {femaleColor}"></span>
			Female
		</span>
	</div>

	{#if byline}
		<p class="product caption text-color-text-muted">{byline}</p>
	{/if}
</div>
