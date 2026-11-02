import { base } from '$app/paths';

export const navigation = [
	{
		title: 'Highlights',
		id: 'highlights',
		href: base || '/',
		children: []
	},
	{
		title: 'Population Change',
		id: 'key-points',
		href: `${base}/key-points`,
		children: []
	},
	{
		title: 'Components of change',
		id: 'components-of-change',
		href: `${base}/components-of-change`,
		children: []
	},
	{
		title: 'Age structure of the population',
		id: 'age-structure',
		href: `${base}/age-structure`,
		children: []
	}
];
