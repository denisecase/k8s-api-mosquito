"""app/db.py

    Database module for the Mosquito API.
    This module handles database connections and queries for the application.
    It uses DuckDB to store and retrieve mosquito trap data.
"""

# Import from the standard library
import os
import pathlib
import sys

# Import third-party libraries
import duckdb
from loguru import logger

# Configure logger
logger.add(sys.stderr, level="INFO", format="{time} {level} {message}")

# Define paths using pathlib
DIR_APP = os.path.dirname(os.path.abspath(__file__))
DIR_ROOT = pathlib.Path(DIR_APP).parent
DIR_DATA = f"{DIR_ROOT}/data"
DIR_DB = f"{DIR_ROOT}/db"
FILE_DB = pathlib.Path(DIR_DB) / "mosquito.duckdb" # Use pathlib for path concatenation

# Log paths
logger.info(f"{DIR_APP=}")
logger.info(f"{DIR_ROOT=}")
logger.info(f"{DIR_DATA=}")
logger.info(f"{DIR_DB=}")
logger.info(f"{FILE_DB=}")

# ==================================================
# About the data
# ===================================================

# Get min and max date_collected from the traps table
try:
    with duckdb.connect(str(FILE_DB)) as con:
        con.execute("SELECT MIN(date_collected), MAX(date_collected) FROM traps")
        MIN_DATE_COLLECTED, MAX_DATE_COLLECTED = con.fetchone()
        logger.info(f"{MIN_DATE_COLLECTED=}")
        logger.info(f"{MAX_DATE_COLLECTED=}")
        # Log in the format YYYY-MM-DD
        logger.info(f"MIN_DATE_COLLECTED={MIN_DATE_COLLECTED.strftime('%Y-%m-%d')}")
        logger.info(f"MAX_DATE_COLLECTED={MAX_DATE_COLLECTED.strftime('%Y-%m-%d')}")
except Exception as e:
    MIN_DATE_COLLECTED, MAX_DATE_COLLECTED = None, None
    logger.warning(f"Could not retrieve min/max date_collected: {e}")

# Get distinct species from the traps table
try:
    with duckdb.connect(str(FILE_DB)) as con:
        con.execute("SELECT DISTINCT species FROM traps ORDER BY species")
        SPECIES_LIST = [row[0] for row in con.fetchall()]
        logger.info(f"Found {len(SPECIES_LIST)} species:")
        for species in SPECIES_LIST:
            logger.info(f"- {species}")
except Exception as e:
    SPECIES_LIST = []
    logger.warning(f"Could not retrieve species list: {e}")

# ==================================================
# Return the helper information
# ===================================================

def get_min_date_collected():
    try:
        with duckdb.connect(str(FILE_DB)) as con:
            result = con.execute("SELECT MIN(date_collected) FROM traps").fetchone()
            return result[0].strftime("%Y-%m-%d") if result[0] else None
    except Exception as e:
        logger.error(f"Error getting min date_collected: {e}")
        return None

def get_max_date_collected():
    try:
        with duckdb.connect(str(FILE_DB)) as con:
            result = con.execute("SELECT MAX(date_collected) FROM traps").fetchone()
            return result[0].strftime("%Y-%m-%d") if result[0] else None
    except Exception as e:
        logger.error(f"Error getting max date_collected: {e}")
        return None
    
def get_species_list():
    try:
        with duckdb.connect(str(FILE_DB)) as con:
            result = con.execute("SELECT DISTINCT species FROM traps").fetchall()
            return [row[0] for row in result]
    except Exception as e:
        logger.error(f"Error getting species list: {e}")
        return []
    
# =================================================
# Define API service functions
# =================================================

def get_all_traps():
    """Fetch all traps from the database."""
    try:
        with duckdb.connect(str(FILE_DB)) as con:
            con.execute("SELECT COUNT(*) FROM traps")  # Will raise if not exists
            return con.execute("SELECT * FROM traps LIMIT 100").fetchall()
    except Exception as e:
        logger.error(f"Failed to load 'traps' from the database: {e}")
        return []

def get_some_traps(count=100):
    """Fetch a limited number of traps from the database."""
    try:
        with duckdb.connect(str(FILE_DB)) as con:
            con.execute("SELECT COUNT(*) FROM traps")  # Will raise if not exists
            # Parameterized query for LIMIT clause
            return con.execute("SELECT * FROM traps LIMIT ?", [count]).fetchall()
    except Exception as e:
        logger.error(f"Failed to load 'traps' from the database: {e}")
        return []
        

def get_trap_by_id(trap_id):
    """Fetch a specific trap by its ID from the database."""
    try:
        with duckdb.connect(str(FILE_DB)) as con:
            # Check if the table exists
            con.execute("SELECT COUNT(*) FROM traps")
            # Parameterized query for trap_id
            return con.execute("SELECT * FROM traps WHERE id = ?", [trap_id]).fetchone()
    except Exception as e:
        logger.error(f"Table 'traps' does not exist in the database or query failed: {e}")
        return None
    

def get_traps_by_species(species):
    """Fetch traps by species from the database."""
    try:
        with duckdb.connect(str(FILE_DB)) as con:
            # Check if table exists
            con.execute("SELECT COUNT(*) FROM traps")
            
            # Validate species
            valid_species = [row[0] for row in con.execute("SELECT DISTINCT species FROM traps").fetchall()]
            if species not in valid_species:
                raise ValueError(f"Species not found. Valid options include: {', '.join(valid_species[:5])}...")

            # Return filtered records
            return con.execute("SELECT * FROM traps WHERE species = ?", [species]).fetchall()
    except ValueError as ve:
        raise ve
    except Exception as e:
        logger.error(f"Query failed for species: {e}")
        return []

    

def get_traps_by_date(start_date=None, end_date=None):
    """Fetch traps within a date range from the database."""
    if start_date is None:
        start_date = MIN_DATE_COLLECTED
    if end_date is None:
        end_date = MAX_DATE_COLLECTED

    try:
        with duckdb.connect(str(FILE_DB)) as con:
            con.execute("SELECT COUNT(*) FROM traps")
            return con.execute(
                "SELECT * FROM traps WHERE date_collected BETWEEN ? AND ?",
                [start_date, end_date]
            ).fetchall()
    except Exception as e:
        logger.error(f"Date range query failed: {e}")
        return []

def get_species_list():
    """Fetch distinct species from the database."""
    try:
        with duckdb.connect(str(FILE_DB)) as con:
            # Check if the table exists
            con.execute("SELECT COUNT(*) FROM traps")
            return con.execute("SELECT DISTINCT species FROM traps").fetchall()
    except Exception as e:
        logger.error(f"Table 'traps' does not exist in the database: {e}")
        return []
    

# Conditional execution for testing
if __name__ == "__main__":
    # Test the database connection and queries
    try:
        con = duckdb.connect(str(FILE_DB))
        logger.info("Connected to DuckDB")
        
        # Test get_all_traps
        traps = get_all_traps()
        logger.info(f"Fetched {len(traps)} traps")

        # Test get_some_traps
        some_traps = get_some_traps(5)
        logger.info(f"Fetched {len(some_traps)} specific traps")

        # Test get_trap_by_id (assuming '1' is a valid ID)
        trap_by_id = get_trap_by_id(1)
        logger.info(f"Fetched trap by ID: {trap_by_id}")

        # Test get_traps_by_species (assuming 'Aedes aegypti' is a valid species)
        traps_by_species = get_traps_by_species('Aedes aegypti')
        logger.info(f"Fetched {len(traps_by_species)} traps for Aedes aegypti")

        # Test get_traps_by_date (use the min/max dates if not provided)
        if MIN_DATE_COLLECTED and MAX_DATE_COLLECTED:
            traps_by_date = get_traps_by_date(MIN_DATE_COLLECTED, MAX_DATE_COLLECTED)
            logger.info(f"Fetched {len(traps_by_date)} traps for date range")
        else:
            logger.warning("No valid date range available for testing get_traps_by_date")

        # Test get_species_list
        species = get_species_list()
        logger.info(f"Fetched {len(species)} unique species")

    except Exception as e:
        logger.error(f"DuckDB error during testing: {e}")
    finally:
        try:
            if 'con' in locals() and con:
                con.close()
                logger.info("Closed DuckDB connection.")
        except Exception as e:
            logger.error(f"Error closing connection: {e}")
