"""
This module contains the tests for the file upload functionality.
"""

import os
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_upload_file_success():
    """
    Test successful file upload.
    """
    test_path = "docs/example_data/test_file_valid.xlsx"
    assert os.path.exists(test_path)
    with open(test_path, "rb") as file:
        response = client.post(
            "/upload_file",
            files={
                "file": (
                    test_path,
                    file,
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
            },
        )

    assert response.status_code == 200
    assert response.json()["status"] == "File uploaded and processed successfully"
    assert response.json()["original_filename"] == test_path
    assert response.json()["rows"] >= 0  # Adjust based on your expected data frame


def test_upload_file_no_file():
    """
    Test upload with no file provided.
    """
    response = client.post("/upload_file")
    assert response.status_code == 422


def test_upload_file_invalid_file():
    """
    Test upload with an invalid file type.
    """
    test_path = "docs/example_data/test_file_invalid.txt"
    assert os.path.exists(test_path)
    with open(test_path, "rb") as file:
        response = client.post("/upload_file", files={"file": (test_path, file, "text/plain")})

    assert response.status_code == 400
