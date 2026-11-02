<script lang="ts">
	import PageContainer from '$lib/components/PageContainer.svelte';
	import PageHead from '$lib/components/PageHead.svelte';

	import { resolve } from '$app/paths';

	import { afterNavigate, beforeNavigate } from '$app/navigation';
	import { Bars3, XMark } from '@steeze-ui/heroicons';
	import { Icon } from '@steeze-ui/svelte-icon';

	import { sidebarState } from '$lib/state.svelte';
	import {
		AnalyticsAndCookieConsent,
		Button,
		CookieControlSettings,
		Footer,
		Header,
		PrivacyPolicyLink,
		Theme,
		ThemeSwitcher
	} from '@ldn-viz/ui';
	import '../app.postcss';

	let breakPoint: number = $state(0);

	$effect(() => {
		sidebarState.state.isOpen = breakPoint >= 1280;
	});

	beforeNavigate(() => {
		document.documentElement.classList.add('disable-smooth-scroll');
	});

	afterNavigate(() => {
		requestAnimationFrame(() => {
			document.documentElement.classList.remove('disable-smooth-scroll');
		});
	});

	afterNavigate(() => (sidebarState.state.isOpen = breakPoint >= 1280));

	let { data, children } = $props();
	const tocItems = $derived(data.metadata.toc);
</script>

<Theme />

<svelte:window bind:innerWidth={breakPoint} />
<!--
<PageMetadata
	title="The State of London report"
	description="The State of London report brings together an array of data about how London is performing across its economy, society and environment. Published annually by the GLA’s City Intelligence unit, it provides an up‑to‑date, data‑led picture of life in the capital, drawing on a wide range of official and administrative sources."
	url="https://apps.london.gov.uk/state-of-london"
	image="https://apps.london.gov.uk/state-of-london/preview.jpg"
	imageAlt="Screenshot of the State of London report"
	imageWidth={1200}
	imageHeight={630}
/>
-->
<svelte:head>
	<script>
		window.ldnVizCivicApiKey = 'b08bca6362c188d40519ea5501ffd4a94d8003dc';
		window.ldnVizCivicAppName = 'state-of-london';
	</script>
</svelte:head>

<AnalyticsAndCookieConsent />

<div class="flex min-h-dvh flex-col">
	<div class="sticky top-0 z-50">
		<Header>
			<Button
				variant="square"
				size="sm"
				emphasis="secondary"
				class="-ml-3 mr-1 !bg-transparent text-color-text no-underline hover:!text-color-text-muted xl:hidden"
				onclick={() => (sidebarState.state.isOpen = !sidebarState.state.isOpen)}
			>
				{#if !sidebarState.state.isOpen}
					<Icon src={Bars3} class="h-5 w-5"></Icon>
				{:else}
					<Icon src={XMark} class="h-5 w-5"></Icon>
				{/if}
			</Button>
			<a href={resolve('/')}>
				<span class="product body font-semibold"> London's Population </span>
			</a>
		</Header>
	</div>

	<PageHead
		title={data.metadata.title}
		subTitle={data.metadata.description}
		image={data.metadata.heroImage}
		intro={data.metadata.intro}
	></PageHead>

	<PageContainer {tocItems}>
		{@render children()}
	</PageContainer>

	<Footer showCiuLogo>
		<div class="product body-sm pb-4 lg:w-1/6">
			<nav>
				<h3 class="mb-1 font-semibold">Links</h3>
				<ul class="text-color-text-muted">
					<li>
						<a href="https://data.london.gov.uk/demography" target="_blank" class="hover:underline">
							London Data Store
						</a>
					</li>
				</ul>
			</nav>
		</div>

		<div class="product body-sm pb-4 lg:w-1/6">
			<nav>
				<h3 class="mb-1 font-semibold">Contact</h3>
				<ul class="text-color-text-muted">
					<li>
						<a href="mailto:demography@london.gov.uk?subject=London's Population"
							>demography@london.gov.uk</a
						>
					</li>
				</ul>
			</nav>
		</div>

		{#snippet footerCookieMenu()}
			<div class="flex justify-between">
				<ul class="label-sm-tight flex space-x-2">
					<li><CookieControlSettings /></li>
					<li><PrivacyPolicyLink /></li>
				</ul>
				<ThemeSwitcher size="xs" />
			</div>
		{/snippet}
	</Footer>
</div>
