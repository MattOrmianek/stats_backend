"""
This module contains the tests for the live data generation endpoint.
"""

import pytest
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


def test_get_random_data_default_values():
    """
    Test the get_random_data endpoint with default values.
    """
    response = client.get("/get_random_data")

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 100  # Default num_points
    for x_data, y_data in data:
        assert 0 <= x_data <= 1  # Default min_value and max_value
        assert 0 <= y_data <= 1


def test_get_random_data_custom_values():
    """
    Test the get_random_data endpoint with custom values.
    """
    num_points = 5
    min_value = -10
    max_value = 10

    response = client.get(f"/get_random_data?num_points={num_points}&min_value={min_value}&max_value={max_value}")

    assert response.status_code == 200
    data = response.json()

    assert len(data) == num_points
    for x_data, y_data in data:
        assert min_value <= x_data <= max_value
        assert min_value <= y_data <= max_value


def test_get_random_data_invalid_num_points():
    """
    Test the get_random_data endpoint with invalid num_points.
    """
    response = client.get("/get_random_data?num_points=0")

    assert response.status_code == 422  # Unprocessable Entity


def test_get_random_data_invalid_range():
    """
    Test the get_random_data endpoint with invalid range (min > max).
    """
    response = client.get("/get_random_data?min_value=10&max_value=5")

    assert response.status_code == 422  # Unprocessable Entity


@pytest.mark.parametrize("num_points", [1, 50, 1000])
def test_get_random_data_various_num_points(num_points):
    """
    Test the get_random_data endpoint with various numbers of points.
    """
    response = client.get(f"/get_random_data?num_points={num_points}")

    assert response.status_code == 200
    data = response.json()

    assert len(data) == num_points


def test_get_random_data_float_values():
    """
    Test the get_random_data endpoint with float values.
    """
    min_value = -1.5
    max_value = 1.5

    response = client.get(f"/get_random_data?min_value={min_value}&max_value={max_value}")

    assert response.status_code == 200
    data = response.json()

    for x_data, y_data in data:
        assert min_value <= x_data <= max_value
        assert min_value <= y_data <= max_value
        assert isinstance(x_data, float)
        assert isinstance(y_data, float)
