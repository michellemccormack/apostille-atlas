# Datasets

Generated pages read the JSON copies in `src/data/`; the CSV files here are flat exports of the same rows.

| File | Rows | Source | Pages |
| --- | --- | --- | --- |
| `src/data/hague-countries.json` / `hague-countries.csv` | 129 (every Contracting Party except the U.S.) | HCCH status table for the 1961 Apostille Convention (https://www.hcch.net/en/instruments/conventions/status-table/?cid=41), each country's HCCH Competent Authority page (`authority_pages[].source_url`), and the HCCH objection notes (`objection_notes_url`) | `/apostille-countries/` and `/apostille-countries/<slug>/` |
| `src/data/us-apostille-authorities.json` / `us-apostille-authorities.csv` | 53 (50 states, D.C., American Samoa, Guam) | U.S. Competent Authority page on the HCCH site (https://www.hcch.net/en/states/authorities/details3/?aid=353, page updated September 2, 2026). Verification links tested November 23, 2026; only links that loaded are kept. | `/apostille-offices-by-state/` |

Every row carries `last_checked`. Missing values are `null` in JSON and render as an em dash. Fees are copied exactly as each country reported them to the HCCH. Refresh by re-reading the same HCCH pages; do not fill gaps from memory.
