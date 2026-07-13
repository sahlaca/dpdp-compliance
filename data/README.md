# DPDP Phase 1 — Data Directory

## `sources/`

Official and secondary legal documents used to ground the compliance guidance.

| File | Type | Description |
|------|------|-------------|
| `dpdp_act_2023.pdf` | Primary | DPDP Act, 2023 (MeitY) |
| `dpdp_rules_2025.pdf` | Primary | DPDP Rules, 2025 — G.S.R. 846(E) |
| `dpdp_rules_2025_mirror.pdf` | Primary | English mirror of Rules |
| `pib_rules_summary_2025.pdf` | Primary | PIB press release on Rules notification |
| `dsci_rules_index_2025.pdf` | Secondary | DSCI Rule-to-Section index |
| `dla_piper_guide_india.pdf` | Secondary | DLA Piper India guide |
| `manifest.json` | Catalog | Metadata + official URLs for all sources |

**Re-download sources:**
```bash
cd backend && python scripts/download_sources.py
```

## `corpus/`

Searchable text chunks extracted from source PDFs.

**Rebuild corpus after downloading new sources:**
```bash
cd backend && python scripts/ingest_corpus.py
```
