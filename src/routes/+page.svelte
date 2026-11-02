<script lang="ts">
	import PageNav from '$lib/components/pageNav/PageNav.svelte';

	let { data } = $props();

	const PageComponent = $derived(data.component);
</script>

<svelte:head>
	<title>London's Population</title>
</svelte:head>

<PageComponent />

<PageNav />
