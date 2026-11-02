---
title: Population Change
description: London's current population and how it changed over the latest year
section: Demography
navLabel: Population Change
---

<script>
import Chart from "$lib/components/charts/Chart.svelte";
import { figures, formatNumber, formatSigned } from "$lib/data/london";
</script>

## Population Change

London's {figures.year} population was {formatNumber(figures.population.now)}. The first chart below shows the {figures.year} MYE in the context of previous estimates. The annual change in population fell to {formatSigned(figures.change2020)} in 2020 and {formatSigned(figures.change2021)} in 2021, and then recovered. We attribute this temporary decrease in population to the COVID-19 pandemic.

<Chart
 title="Population, London"
 subtitle="Mid-year population estimates (persons)"
 dataset="london_population"
 byline="GLA City Intelligence"
 />

<Chart
 title="Annual population change, London"
 subtitle="Year-on-year population change (persons)"
 dataset="london_annual_change"
 byline="GLA City Intelligence"
 />

## Comparison to previous MYE data

[Do we want a comparsion key card and chart here]

<Chart
 title="Population by Sex, London"
 subtitle="Mid-year population estimates (persons)"
 dataset="london_population_by_sex"
 byline="GLA City Intelligence"
 />
