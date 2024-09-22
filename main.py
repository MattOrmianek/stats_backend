"""
This is a simple FastAPI application that generates random data points and returns them as a list.
"""

import os
import uuid
import random
from typing import List, Tuple
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File, HTTPException
from lib.logger.logger_config import setup_logger
from lib.data_processing.read_data import read_data

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
async def get_data(num_points: int, min_value: int, max_value: int) -> List[Tuple[int, int]]:
    """
    Generate a list of random data points.

    Args:
        num_points (int): Number of data points to generate. Defaults to 100.
        min_value (int): Minimum value for x and y coordinates. Defaults to 0.
        max_value (int): Maximum value for x and y coordinates. Defaults to 1000.

    Returns:
        List[Tuple[int, int]]: A list of tuples containing random (x, y) coordinates.
    """
    logger.info(
        "Generating %d random data points between %d and %d", num_points, min_value, max_value
    )
    data = [
        (random.randint(min_value, max_value), random.randint(min_value, max_value))
        for _ in range(num_points)
    ]
    return data


@app.post("/upload_file")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a file and read the data.
    """
    try:
        logger.info("Uploading file: %s", file.filename)
        upload_dir = "uploaded_files"
        os.makedirs(upload_dir, exist_ok=True)

        # Generate a unique filename to prevent overwriting
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(upload_dir, unique_filename)

        # Use a context manager for file handling
        with open(file_path, "wb") as buffer:
            await file.seek(0)  # Ensure we're at the start of the file
            while content := await file.read(1024 * 1024):  # Read in 1MB chunks
                buffer.write(content)

        logger.info("File uploaded successfully: %s", unique_filename)
        data_frame = read_data(file_path)
        logger.info("Data frame from file: %s", data_frame)

        return {
            "filename": unique_filename,
            "original_filename": file.filename,
            "status": "File uploaded and processed successfully",
            "rows": data_frame.shape[0],
            "columns": data_frame.shape[1],
        }

    except Exception as error:
        logger.error("Error uploading file: %s", str(error), exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"An error occurred while uploading the file: {str(error)}"
        ) from error


if __name__ == "__main__":
    import uvicorn

    logger.info("Starting the FastAPI application")
    uvicorn.run("main:app", host="0.0.0.0", port=3000, reload=True)
