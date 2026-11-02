import type { ChartDataOptions, ChartDataRow } from '@ldn-viz/charts';

import { datasets } from '$lib/data/london';

export function loadChartData(dataset: string, options: ChartDataOptions): Promise<ChartDataRow[]> {
	const rows = datasets[dataset];

	if (!rows) {
		return Promise.reject(new Error(`Unknown dataset: ${dataset}`));
	}

	const convertVal = (val: string | number | Date): string | number | Date => {
		if (options.type === 'integer') return +val;
		if (options.type === 'date') return new Date(val as string);
		return val;
	};

	const data = rows.map((d) => ({ ...d, xd: convertVal(d.xd) }));

	if (options.type === 'date') {
		data.sort((a, b) => (a.xd as Date).getTime() - (b.xd as Date).getTime());
	}

	return Promise.resolve(data);
}
