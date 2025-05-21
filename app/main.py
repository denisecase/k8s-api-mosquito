""" main.py
    Main entry point for the Mosquito API.
    This file contains the FastAPI application instance and the root endpoint.
    It serves as the starting point for the API server.
"""

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Mosquito API is alive!"}
