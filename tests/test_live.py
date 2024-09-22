"""
This module contains the tests for the live data generation endpoint.
"""

from fastapi.testclient import TestClient
from main import app  # Direct import from main.py

client = TestClient(app)


def test_get_random_data():
    """
    Test the get_random_data endpoint.
    """
    num_points = 10
    min_value = 0
    max_value = 100

    response = client.get(
        f"/get_random_data?num_points={num_points}&min_value={min_value}&max_value={max_value}"
    )

    assert response.status_code == 200
    data = response.json()

    assert len(data) == num_points
    for x_data, y_data in data:
        assert min_value <= x_data <= max_value
        assert min_value <= y_data <= max_value
