# Mosquito Trap Data (San Diego)

Represents the cleaned and transformed structure of the `traps` table created in `db/mosquito.duckdb`.  
The table was created from the source CSV file `data/san_diego_mosquito_traps.csv` and loaded using `scripts/load_duckdb.py`.

## Table: `traps`

| Column Name      | Type    | Description                                      |
|------------------|---------|--------------------------------------------------|
| `id`             | INTEGER | Internal ID from the source system              |
| `record_id`      | TEXT    | Unique record ID string (e.g., DEH2016-CVLAB…)  |
| `city`           | TEXT    | City where trap was placed                      |
| `state`          | TEXT    | State abbreviation (e.g., CA)                   |
| `zip_code`       | TEXT    | Zip code of trap location                       |
| `community`      | TEXT    | Community name associated with the trap         |
| `date_collected` | DATE    | Date the trap was collected                     |
| `species`        | TEXT    | Full mosquito species name                      |
| `count`          | INTEGER | Number of mosquitoes captured in trap           |

## Date Range & Count of Traps

- MIN_DATE_COLLECTED=2015-01-07
- MAX_DATE_COLLECTED=2018-08-28
- Fetched 11925 traps

## Distinct Mosquito Species in Dataset

These are the 20 known mosquito species collected in the San Diego mosquito trap data:

1. Aedes aegypti
2. Aedes albopictus
3. Aedes dorsalis
4. Aedes increpitus
5. Aedes melanimon
6. Aedes nigromaculis
7. Aedes sierrensis
8. Aedes sollicitans
9. Anopheles freeborni
10. Anopheles hermsi
11. Anopheles punctipennis
12. Culex erythrothorax
13. Culex pipiens
14. Culex quinquefasciatus - Southern House Mosquito
15. Culex stigmatosoma
16. Culex tarsalis - Western Encephalitis Mosquito
17. Culiseta incidens
18. Culiseta inornata
19. Psorophora columbiae
20. Uranotaenia lowii
