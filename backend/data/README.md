# Knowledge base

Pre-cleaned data for the RAG knowledge base. Use these files - do not fetch external data at runtime.

## Layout

```
data/
├── manifest.json             # Index of all files with metadata (generated)
├── extra-sources.md          # Curated list of additional public sources (some bundled, some pointers only)
├── relocation/               # ~119 files, ~236k tokens
├── life_on_campus/           # ~473 files, ~508k tokens
├── study_abroad/             # ~132 files, ~349k tokens (incl. 18 Farnesina country advisories)
└── career_readiness/         # ~893 files, ~1.79M tokens (incl. 2 AlmaLaurea national synthesis reports)
```

**Total: ~1,617 files, ~2.88M tokens.**

Files are organized by **verticale** (one of `relocation`, `life_on_campus`, `study_abroad`, `career_readiness`) and named after their source URL slug.

## File format

Every Markdown file has YAML frontmatter:

```markdown
---
verticale: career_readiness
language: en
source_url: https://www.unibocconi.it/en/programs/master-science/finance
last_updated: '2026-05-02'
title: MSc Finance | Bocconi University
token_estimate: 1872
---

[Body content in Markdown]
```

The frontmatter lets you filter at query time (e.g. retrieve only `verticale=relocation` chunks for a relocation question).

## Coverage by verticale

### `relocation/`
Welcome guides, housing (Bocconi residences + partners like Sarfatti, Camplus, Collegiate, Aparto), visa & permit-of-stay, codice fiscale, fiscal code, immigration, airport transit (Linate/Malpensa), banks (Volksbank, accounts for non-residents), cost of living guides, emergency numbers (112, 113, 118), healthcare/SSN/ASL Milano, mobile/SIM operators (Iliad), safety, campus map, transport (ATM, AMAT GTFS), neighborhoods (NIL Milano).

### `life_on_campus/`
Campus services (library, language center, sport center, mensa/dining), student associations (BSIC, BSAMC, Bocconi Capital Markets, plus directory), inclusion/well-being/counseling services, mental health resources, Bocconi events, Bocconi sport center, *Tra i Leoni* (independent student newspaper) articles, *Via Sarfatti 25* news, press releases, free things to do in Milan, museums for students.

### `study_abroad/`
Exchange programs, double-degree programs, partner universities (~293 across 56 countries), summer schools, free-mover programs, CEMS MIM, fact sheet for incoming exchange students, immigration documentation for international students.

### `career_readiness/`
All 11 academic departments (Economics, Finance, Accounting, Marketing, Mgmt&Tech, Decision Sciences, Computing Sciences, Social and Political Sciences, Legal Studies, DMI, Mathematics) and 21 research centers (BAFFI, IGIER, IEP@BU, Dondena, Cergas, BIDSA, ICRIOS, AIDAF-EY, FinTech Lab, Gender Lab, Bayes Lab, ART Lab, SUR Lab, BELSS, CAIL, COVID Crisis, CLEAN, GREEN, BUILT, BLEST, etc.). MSc / BSc / PhD programs with structures, curricula, fees and placement. Career Service, JobGate portal info, scholarships (Bocconi Merit, ISU, International Award), tuition fees by year, alumni community + mentoring program, SDA Bocconi (executive education + MBA), faculty directories, open days.

## Sources

Two collection methods:
- **Web pages (HTML)** scraped via Firecrawl, converted to Markdown
- **PDFs** (calendar, fees, factsheets, brochures, surveys, campus map) processed via Mistral OCR with semantic annotation prompts where the layout is graphical

All scraped between 2 and 5 May 2026 and frozen. `last_updated` reflects the snapshot date.

## Multilingual

The dataset is mostly in English (~98%) with a small minority in Italian (~2%). Use a multilingual embedding model (e.g. `text-embedding-3-large`) for good cross-lingual retrieval - some content (especially on `unibocconi.it/it/...` and Italian press releases) is in Italian. Bocconi-specific terms (CLEF, Triennale, Magistrale, Borse Bocconi Merit) often have no clean English translation.

## Working with the data

- Files are bind-mounted **read-only** in `docker-compose.dev.yml`
- For the production image, the entire `data/` folder is `COPY`-ed into the container by `Dockerfile.prod`
- If you precompute a vector index (FAISS, Chroma, sqlite-vec, ...), save it inside `data/` so it ships with the production image. Otherwise add the index file to `.gitignore`.
- Keep references to real file paths in your `/ask` response's `sources` field - the evaluator may check grounding.

## `extra-sources.md`

A curated list of additional public datasets and sources NOT bundled in this folder, but useful if you want to differentiate. Includes more Comune di Milano open data, ISTAT, university rankings, OpenStreetMap, etc. You'd have to fetch and parse them yourself.

## `manifest.json`

Generated index of every file with `verticale`, `language`, `title`, `source_url`, `token_estimate`, `path`. Useful for:
- Quick stats on what's in the dataset
- Programmatic loading of all files for index building
