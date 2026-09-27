---
verticale: trasversale
language: en
last_updated: '2026-05-08'
title: Extra sources - curated list of additional public datasets
---

# Extra sources - public datasets and references

Curated list of additional **publicly accessible** sources beyond what is bundled in `data/bocconi/` and `data/openmilano/`. Some of these are NOT included as scraped/parsed content - if you want to use them, you must fetch and parse them yourself.

The intent: give you pointers to differentiate your AI Buddy with extra ground-truth knowledge.

## Already bundled (snapshot 2026-05-08)

These external sources are NOW shipped as parsed markdown inside the dataset:

- **Farnesina / Unita' di Crisi MAECI - Schede paese viaggiaresicuri.it**: 18 country advisories bundled in `study_abroad/viaggiaresicuri-it-scheda-paese-*.md`. Includes major Bocconi exchange destinations (China, Japan, Singapore, South Korea, India, Hong Kong, Thailand, Indonesia, Israel, Pakistan) and high-risk countries (Afghanistan, Myanmar, Yemen, Iran, North Korea, Syria, Russia, Ukraine). Source: `https://www.viaggiaresicuri.it/schede_paese/{CODICE3}.json` (JSON API). For other countries fetch additional schede paese yourself.
- **AlmaLaurea - Sintesi Condizione Occupazionale dei Laureati 2023 e 2024**: national synthesis reports bundled in `career_readiness/almalaurea-it-sintesi-condizione-occupazionale-laureati-202{3,4}.md`. National-level figures only (not Bocconi-specific). For per-ateneo statistics, see the AlmaLaurea statistical portal below.

## Open data Milano (additional datasets)

The full Comune di Milano open data portal: https://dati.comune.milano.it/

Specific datasets worth exploring:

- **Public transport (ATM)**:
  - GTFS feed (always-current schedule): https://dati.comune.milano.it/gtfs.zip
  - ATM surface line routes: https://dati.comune.milano.it/dataset/ds538_atm-percorsi-linee-di-superficie-urbane
  - AMAT GTFS publishing: https://www.amat-mi.it/it/servizi/pubblicazione-orari-trasporto-pubblico-locale-formato-gtfs/
  - All transport datasets: https://dati.comune.milano.it/callgroup/32bbfe8c-ca16-4ec3-bd6f-c12380ca3a11
- **Neighborhoods (NIL - Nuclei di Identità Locale)**:
  - Demographic and territorial characteristics: https://dati.comune.milano.it/it/dataset/ds205-sociale-caratteristiche-demografiche-territoriali-quartiere
  - Population by NIL: search "popolazione anagrafe" on the portal
- **University students in Milan**:
  - https://dati.comune.milano.it/dataset/ds752_iscritti-nelle-universita-milanesi-anno-accademico-2017-avanti
- **Cultural events and spaces**:
  - https://www.comune.milano.it/en/servizi/cultura/spazi-culturali-per-eventi-e-iniziative

## City of Milan (institutional)

- Statistics: https://www.comune.milano.it/en/aree-tematiche/dati-statistici
- Geoportale SIT (geographical data): https://geoportale.comune.milano.it/sit/open-data/
- Città Metropolitana (extended scope beyond city): https://www.cittametropolitana.mi.it/open_data/

## National datasets - Italy

- **ISTAT** (national statistics): https://www.istat.it/en/
- **dati.gov.it** (national open data portal): https://www.dati.gov.it/

## Education and university rankings

- **QS World University Rankings**: https://www.topuniversities.com/
- **Times Higher Education**: https://www.timeshighereducation.com/world-university-rankings
- **Fondazione Agnelli** (Italian schools data): https://www.fondazioneagnelli.it/
- **AlmaLaurea** (Italian graduate-survey consortium - Bocconi profile, ateneo code 70032):
  - Bocconi profile statistics: https://www2.almalaurea.it/cgi-php/universita/statistiche/framescheda.php?anno=2023&corstipo=L&ateneo=70032&LANG=it
  - Main portal: https://www.almalaurea.it/

## Cost of living (Milan)

- **Numbeo - Cost of Living in Milan** (community-sourced prices: rent, groceries, transport, salaries): https://www.numbeo.com/cost-of-living/in/Milan

## Travel safety / advisories

- **Farnesina - Viaggiare Sicuri** (official Italian Foreign Ministry country advisories - MAECI Unita' di Crisi): https://www.viaggiaresicuri.it/  Public JSON endpoint per country: `https://www.viaggiaresicuri.it/schede_paese/{ISO-3-CODE}.json`. 18 schede are already bundled in `study_abroad/viaggiaresicuri-it-scheda-paese-*.md`; fetch other countries from the same endpoint if needed.

## International student mobility

- **UNESCO Institute for Statistics**: http://uis.unesco.org/
- **Eurostat - Education and training**: https://ec.europa.eu/eurostat/web/education-and-training

## Geo / OpenStreetMap

- **OpenStreetMap**: https://www.openstreetmap.org/
- **Overpass API** (query OSM data): https://overpass-api.de/

## Bocconi extended (already partially bundled)

- **Tra i Leoni** (independent student newspaper): https://traileoni.it/
- **Via Sarfatti 25** (official news magazine): https://viasarfatti25.unibocconi.eu/
- **B4i** (Bocconi for innovation - startups): https://www.b4i.unibocconi.it/
- **Bocconi Sport Center**: https://www.bocconisport.eu/
- **Bocconi Alumni Community**: https://www.bocconialumni.it/

## Notes on usage

1. Always rate-limit your requests when fetching from these sources
2. Cache results - don't re-fetch on every query
3. Respect the data licenses (most CC-BY-SA / IODL-compatible)
4. If a source is paywalled, you don't need it for the hackathon
