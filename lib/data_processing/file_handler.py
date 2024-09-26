"""
This module contains functions for handling file uploads.
"""

import os
import uuid
from fastapi import UploadFile, HTTPException
from lib.data_processing.read_data import read_data
from lib.logger.logger_config import setup_logger

logger = setup_logger(__name__)


async def handle_file_upload(file: UploadFile) -> dict:
    """
    Handle the file upload and processing.

    Args:
        file (UploadFile): The uploaded file.

    Returns:
        dict: Information about the uploaded file and processed data.
    """
    try:
        logger.info("Uploading file: %s", file.filename)
        upload_dir = "uploaded_files"
        os.makedirs(upload_dir, exist_ok=True)

        # Generate a unique filename to prevent overwriting
        file_extension = os.path.splitext(file.filename)[1] or ""

    except Exception as error:
        logger.error("Error uploading file: %s", str(error))
        raise HTTPException(
            status_code=500, detail=f"An error occurred while uploading the file: {str(error)}"
        ) from error

    try:
        # Check if the file extension is .xlsx
        if file_extension.lower() not in [".xlsx", ".xls"]:
            logger.warning("Attempted to upload invalid file type: %s", file_extension)
            return {"error": "Invalid file type. Only .xlsx and .xls files are allowed."}

        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(upload_dir, unique_filename)
    except Exception as error:
        logger.error("Error uploading file: %s", str(error))
        raise HTTPException(
            status_code=500, detail=f"An error occurred while uploading the file: {str(error)}"
        ) from error

    try:
        # Use a context manager for file handling
        with open(file_path, "wb") as buffer:
            await file.seek(0)  # Ensure we're at the start of the file
            while content := await file.read(1024 * 1024):  # Read in 1MB chunks
                buffer.write(content)
    except Exception as error:
        logger.error("Error uploading file: %s", str(error))
        raise HTTPException(
            status_code=500, detail=f"An error occurred while uploading the file: {str(error)}"
        ) from error

    try:
        # Check if the file is a valid Excel file
        data_frame = read_data(file_path, logger)
    except Exception as error:  # pylint: disable=broad-exception-caught
        logger.error("Error reading data from file: %s", str(error))
        return {"error": "Uploaded file is not a valid Excel file."}

    logger.info("Data frame from file: %s", data_frame)

    return {
        "filename": unique_filename,
        "original_filename": file.filename,
        "status": "File uploaded and processed successfully",
        "rows": data_frame.shape[0],
        "columns": data_frame.shape[1],
    }
