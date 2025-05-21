""" app/main.py
    Main entry point for the Mosquito API using FastAPI.
    Serves a simple root endpoint and sets up the application.
"""
# Import from the standard library
import sys

# Import third-party libraries
from fastapi import FastAPI, HTTPException
from loguru import logger

# Import local modules
from app.db import (
    get_min_date_collected,
    get_max_date_collected,
    get_species_list,
    get_all_traps,
    get_some_traps,
    get_trap_by_id,
    get_traps_by_species,
    get_traps_by_date
)


# Configure logger
logger.add(sys.stderr, level="INFO", format="{time} {level} {message}")

# Create the FastAPI app instance
app = FastAPI()

# =================================
# Get data information
# =================================

# Get valid ranges on startup (read-only)
MIN_DATE = get_min_date_collected()
MAX_DATE = get_max_date_collected()

# unpack list of tuples
SPECIES_LIST = [s[0] for s in get_species_list()]  

# =================================
# Define API endpoints that 
# call the service functions in app/db.py
# =================================


@app.get("/")
def read_root():
    """Root endpoint returns a confirmation message."""
    logger.info("GET / called")
    return {"message": "Mosquito API is alive!"}


@app.get("/traps")
def read_traps(limit: int = 100):
    """Return up to {limit} traps."""
    logger.info(f"GET /traps?limit={limit} called")
    return get_some_traps(count=limit)


@app.get("/traps/{trap_id}")
def read_trap_by_id(trap_id: int):
    """Return a specific trap by ID."""
    logger.info(f"GET /traps/{trap_id} called")
    return get_trap_by_id(trap_id)


@app.get("/species")
def read_species():
    logger.info("GET /species called")
    return SPECIES_LIST

@app.get("/species/{species_name}")
def read_traps_by_species(species_name: str):
    """Return traps that match the given species."""
    logger.info(f"GET /species/{species_name} called")
    try:
        return get_traps_by_species(species_name)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/dates")
def read_traps_by_date_range(start: str, end: str):
    logger.info(f"GET /dates?start={start}&end={end} called")
    if start < MIN_DATE or end > MAX_DATE:
        raise HTTPException(
            status_code=400,
            detail=f"Date range must be between {MIN_DATE} and {MAX_DATE}."
        )
    return get_traps_by_date(start_date=start, end_date=end)