"""
scripts/load_duckdb.py
This script loads mosquito trap data into a DuckDB database.
It reads the data from a CSV file and creates a table named 'traps'.

Example CSV header and data:

_id,Record ID,City,State,Zip Code,Community,Date Collected,Mosquito Species,Count
1,DEH2016-CVLAB-003207,Vista,CA,92083,Vista,2016-07-31T00:00:00,Culex quinquefasciatus - Southern House Mosquito,4
2,DEH2014-CVLAB-000002,Carlsbad,CA,92008,Carlsbad,2015-03-17T00:00:00,Culex tarsalis - Western Encephalitis Mosquito,15

"""
# Import from the standard library
import os
import pathlib
import sys

# Import third-party libraries
import duckdb
import pandas as pd
from loguru import logger

# Configure logger
logger.add(sys.stderr, level="INFO", format="{time} {level} {message}")

# Define paths using pathlib
DIR_SCRIPTS = os.path.dirname(os.path.abspath(__file__))
DIR_ROOT = pathlib.Path(DIR_SCRIPTS).parent
DIR_DATA = DIR_ROOT / "data"
DIR_DB = DIR_ROOT / "db"
FILE_DB = DIR_DB / "mosquito.duckdb"
FILE_CSV = DIR_DATA / "san_diego_mosquito_traps.csv"

# Log paths
logger.info(f"{DIR_SCRIPTS}=")
logger.info(f"{DIR_ROOT}=")
logger.info(f"{DIR_DATA}=")
logger.info(f"{DIR_DB}=")

# Create directories if they don't exist
os.makedirs(DIR_DB, exist_ok=True)

# If DIR_DATA doesn't exist or is empty, warn and exit
if not os.path.exists(DIR_DATA) or not os.listdir(DIR_DATA):
    logger.warning(f"Directory {DIR_DATA} does not exist or is empty. Nothing to load")
    sys.exit(1)

# Check if CSV file exists
if not FILE_CSV.exists():
    logger.warning(f"File not found: {FILE_CSV}")
    sys.exit(1)

# Load CSV to DataFrame
df = pd.read_csv(FILE_CSV)
if df.empty:
    logger.warning(f"CSV {FILE_CSV} is empty. Nothing to load.")
    sys.exit(1)


# ===================================
# Feature Engineering / Data Cleaning
# ===================================

# Rename columns to be SQL-friendly (no spaces, lowercase, snake_case)
df = df.rename(
    columns={
        "_id": "id",
        "Record ID": "record_id",
        "City": "city",
        "State": "state",
        "Zip Code": "zip_code",
        "Community": "community",
        "Date Collected": "date_collected",
        "Mosquito Species": "species",
        "Count": "count"
    }
)

# Convert date_collected to datetime (if not already)
df["date_collected"] = pd.to_datetime(df["date_collected"], errors="coerce")

# Drop rows with invalid dates
df = df.dropna(subset=["date_collected"])

# ==================================
# Load clean DataFrame into DuckDB
# ==================================

# Connect and write to DuckDB
try:
    con = duckdb.connect(str(FILE_DB))
    con.execute("CREATE OR REPLACE TABLE traps AS SELECT * FROM df")
    logger.info(f"Loaded {len(df)} rows into {FILE_DB}")
except duckdb.DuckDBError as e:
    logger.error(f"DuckDB error: {e}")
    sys.exit(1)
finally:
    try:
        con.close()
    except:
        pass