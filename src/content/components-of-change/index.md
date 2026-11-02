---
title: Components of change
description: Births, deaths and migration
section: Demography
navLabel: Components of change
---

<script>
import Chart from "$lib/components/charts/Chart.svelte";
import { figures, compare, formatNumber, formatRounded, formatSigned } from "$lib/data/london";

const { year, births, deaths, naturalChange, domestic, international } = figures;
const absCompare = (now, prev) => compare(Math.abs(now), Math.abs(prev));
</script>

## Components of Change

Births, deaths and migration form the components of population change.

The {year} MYE value for births was {compare(births.now, births.prev)} than that in {year - 1}, and for deaths {compare(deaths.now, deaths.prev)}. The consequent value for natural change (births - deaths) was {compare(naturalChange.now, naturalChange.prev)} than in {year - 1}.

<Chart
 title="Births and deaths, London"
 subtitle="Annual births and deaths (persons)"
 dataset="london_births_deaths"
 byline="GLA City Intelligence"
 />

<Chart
 title="Natural change, London"
 subtitle="Births minus deaths (persons)"
 dataset="london_natural_change"
 byline="GLA City Intelligence"
 />

At {formatSigned(domestic.now)}, the net outflow of domestic migration (migration within the UK) was {absCompare(domestic.now, domestic.prev)} than the {year - 1} value, and still significantly lower than the peak net outflow of {formatNumber(Math.abs(figures.peakDomesticOutflow.value))} in {figures.peakDomesticOutflow.year}, during the COVID-19 pandemic. An outflow of domestic migrants from London is normal and this has been the case each year for the last two decades. This flow is partly because many international in-migrants initially settle in London before moving out to other parts of the UK. The second move in this sequence is counted as a domestic migration.

There has been a marked change in immigration since 2021. This can be attributed to the end of free movement for EU nationals, easing of travel restrictions following the COVID-19 pandemic, and the war in Ukraine. At {formatRounded(international.now)}, the {year} MYE value for London's net international migration was {compare(international.now, international.prev)} than {year - 1}, after reaching a peak of {formatRounded(figures.peakInternational.value)} in {figures.peakInternational.year}. It remains well above the {formatRounded(figures.international2021)} recorded in 2021.

<Chart
 title="Net migration, London"
 subtitle="Net international, domestic and total migration (persons)"
 dataset="london_net_migration"
 byline="GLA City Intelligence"
 />
