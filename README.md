# London’s population site

This repository contains the static web app for London’s demographic reporting and population analysis. It is built with SvelteKit and produces a publication-style site covering London population totals, age structure, change over time, and related demographic datasets.

## Project overview

The app reads locally generated JSON datasets in `src/lib/data` and renders them into markdown-driven pages and chart components. Content is organised under `src/content`, with page metadata and chart config driving the report structure.

Key areas of the project:

- `src/content` — page content and report sections
- `src/lib/components` — reusable UI and chart components
- `src/lib/data` — generated demographic datasets used by the site
- `scripts` — data preparation scripts for population and age-structure datasets
- `public` and `static` — static assets and exported files

## Local setup

Install dependencies:

```bash
npm install
```

Run the site locally:

```bash
npm run dev
```

Build the production site:

```bash
npm run build
```

Run type checks:

```bash
npm run check
```

## Data pipeline

The project uses generated JSON files derived from source data. The main source-building script is:

```bash
python3 scripts/build_london_from_single_source.py /path/to/london_sex_age_totals.csv
```

This script creates the data files used by the site, including:

- `src/lib/data/londonPopulationTotal.json`
- `src/lib/data/londonAgeStructure.json`
- `src/lib/data/londonAgeGroups.json`
- `src/lib/data/londonComponentsOfChange.json`

The site uses these generated files to populate the charts and summary figures displayed on the pages.

## Content workflow

The report pages are authored as markdown in `src/content` and rendered through the SvelteKit + mdsvex pipeline.

Common commands:

```bash
npm run build:content
npm run dev
npm run build
```

`npm run build:content` regenerates content from the structured markdown setup and refreshes the content index used by the app.

## Repository conventions

- `*.csv` source files are ignored in `.gitignore` so local data inputs are not committed.
- Generated content and build artefacts stay out of source control.
- The app is configured around a publication-style data report rather than a generic app shell.

## Notes

This project is primarily a demographic analysis and reporting site for London, with the data pipeline and chart components designed around population estimates, age structure, and change over time.
