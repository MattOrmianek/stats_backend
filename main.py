"""
This is a simple FastAPI application that generates random data points and returns them as a list.
"""

import random
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/get_data")
async def get_data():
    """
    This endpoint generates a list of random data points.
    """
    data = []
    for _ in range(0, 100):
        random_x = random.randint(0, 1000)
        random_y = random.randint(0, 1000)
        data.append((random_x, random_y))
    return data


@app.post("/upload_file")
async def upload_file(file: UploadFile = File(...)):
    """
    This endpoint uploads a file to the server.
    """
    upload_dir = "uploaded_files"
    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": file.filename, "status": "File uploaded successfully"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=3000, reload=True)
