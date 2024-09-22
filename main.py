"""
This is a simple FastAPI application that generates random data points and returns them as a list.
"""

from typing import List, Tuple
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from lib.logger.logger_config import setup_logger
from lib.data_processing.generate_data import generate_data
from lib.data_processing.file_handler import handle_file_upload

logger = setup_logger(__name__)
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/get_random_data")
async def get_data(
    num_points: int = Query(default=100, ge=1),
    min_value: float = Query(default=0.0),
    max_value: float = Query(default=1.0),
) -> List[Tuple[float, float]]:
    """
    Generate a list of random data points.

    Args:
        num_points (int): Number of data points to generate. Defaults to 100.
        min_value (float): Minimum value for x and y coordinates. Defaults to 0.0.
        max_value (float): Maximum value for x and y coordinates. Defaults to 1.0.

    Returns:
        List[Tuple[float, float]]: A list of tuples containing random (x, y) coordinates.
    """
    if min_value > max_value:
        raise HTTPException(
            status_code=422, detail="min_value must be less than or equal to max_value"
        )
    generated_data = generate_data(num_points, min_value, max_value, logger)

    return generated_data


@app.post("/upload_file")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a file and read the data.
    """
    return await handle_file_upload(file)


if __name__ == "__main__":
    import uvicorn

    logger.info("Starting the FastAPI application")
    uvicorn.run("main:app", host="0.0.0.0", port=3000, reload=True)
