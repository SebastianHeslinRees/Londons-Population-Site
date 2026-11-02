---
title: Age structure of the population
description: London's population by age
section: Demography
navLabel: Age structure of the population
---

<script>
import Chart from "$lib/components/charts/Chart.svelte";
import PopulationPyramid from "$lib/components/charts/PopulationPyramid.svelte";
import { figures, formatPercent, formatRounded } from "$lib/data/london";

const { year, primarySchoolAge, secondarySchoolAge, older } = figures;
</script>

## Age structure of the population

The first chart below shows London's population by single year of age in mid-{year}. The median age was {figures.medianAge}.

- {formatRounded(figures.under18)} people were aged under 18
- {formatRounded(figures.aged18to64)} people were aged 18 to 64
- {formatRounded(older.now)} people were aged 65 and over, {formatPercent(figures.olderShare)} of the population (compared with {formatPercent(figures.olderShare2001)} in 2001)

<Chart
 title="Age structure, London"
 subtitle="Population by single year of age (persons), mid-{year}"
 dataset="london_age_structure"
 byline="GLA City Intelligence"
 />

The population pyramid below shows the same population broken down into 5-year age bands and split by sex. Use the slider to see how the structure has changed since 2001.

<PopulationPyramid
 title="Age structure, London"
 subtitle="Population by 5-year age band and sex (persons)"
 byline="GLA City Intelligence"
 />


The second chart shows how the numbers of primary school age children (5 to 10), secondary school age children (11 to 15) and people aged 65 and over have changed since 2001. The number of primary school age children peaked at {formatRounded(primarySchoolAge.peak.value)} in {primarySchoolAge.peak.year} and the number of secondary school age children peaked at {formatRounded(secondarySchoolAge.peak.value)} in {secondarySchoolAge.peak.year}.

<Chart
 title="Population by age group, London"
 subtitle="Primary school age, secondary school age and aged 65 and over (persons)"
 dataset="london_age_groups"
 byline="GLA City Intelligence"
 />

## Future Updates

ONS publishes new mid-year estimates each year.

The full ONS mid-year population estimates release and back series can be found on the ONS website: [https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates](https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates).

For information relating to London's population see the demography pages of the London Datastore: [https://data.london.gov.uk/demography/](https://data.london.gov.uk/demography) or email [demography@london.gov.uk](mailto:demography@london.gov.uk).

An in-depth review of the available evidence for population change in London since the start of the coronavirus pandemic has been produced by GLA Demography: [https://data.london.gov.uk/dataset/population-change-in-london-during-the-pandemic](https://data.london.gov.uk/dataset/population-change-in-london-during-the-pandemic).
