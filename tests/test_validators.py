import pytest

# VALIDATION CHECKS
def test_rates_missing_params(client):
    response = client.get('/rates?date_from=2023-01-01&date_to=2023-01-05&origin=CNSGH')
    assert response.status_code == 400
    assert b"Missing required parameters" in response.data

def test_rates_invalid_date_format(client):
    response = client.get('/rates?date_from=2023-01-01&date_to=invalid_date&origin=CNSGH&destination=NLRTM')
    assert response.status_code == 400
    assert b"Invalid date format" in response.data

def test_rates_date_from_after_date_to(client):
    response = client.get('/rates?date_from=2023-01-05&date_to=2023-01-01&origin=CNSGH&destination=NLRTM')
    assert response.status_code == 400
    assert b"date_from must be earlier than date_to" in response.data
