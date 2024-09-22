"""
This is a simple FastAPI application that generates random data points and returns them as a list.
"""

import os
import uuid
import random
from typing import List, Tuple
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File, HTTPException

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
    return [
        (random.randint(min_value, max_value), random.randint(min_value, max_value))
        for _ in range(num_points)
    ]


@app.post("/upload_file")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a file to the server.

    Args:
        file (UploadFile): The file to be uploaded.

    Returns:
        dict: A dictionary containing the filename and status of the upload.

    Raises:
        HTTPException: If there's an error during the file upload process.
    """
    try:
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

        return {
            "filename": unique_filename,
            "original_filename": file.filename,
            "status": "File uploaded successfully",
        }

    except Exception as error:
        raise HTTPException(
            status_code=500, detail=f"An error occurred while uploading the file: {str(error)}"
        ) from error


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=3000, reload=True)
