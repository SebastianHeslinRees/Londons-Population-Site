<script lang="ts">
	import PageNav from '$lib/components/pageNav/PageNav.svelte';
	import type { PageProps } from './$types';

	let { data }: PageProps = $props();

	const PageComponent = $derived(data.component);
</script>

<svelte:head>
	<title>London's Population - {data.metadata.title}</title>
</svelte:head>

<PageComponent />

<PageNav />
