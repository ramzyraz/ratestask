import pytest
from flask import json

def test_rates_port_to_port(client, db):
    # setup_db fixture ensures database is connected and populated with test data
    response = client.get('/rates?date_from=2023-01-01&date_to=2023-01-05&origin=CNSGH&destination=NLRTM')

    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 5
    assert all(item['average_price'] is not None for item in data)

def test_rates_port_to_region(client, db):
    response = client.get('/rates?date_from=2023-01-01&date_to=2023-01-05&origin=CNSGH&destination=north_europe_main')

    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 5
    assert all(item['average_price'] is not None for item in data)

def test_rates_region_to_port(client, db):
    response = client.get('/rates?date_from=2023-01-01&date_to=2023-01-05&origin=china_main&destination=NLRTM')

    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 5
    assert all(item['average_price'] is not None for item in data)

def test_rates_region_to_region(client, db):
    response = client.get('/rates?date_from=2023-01-01&date_to=2023-01-05&origin=china_main&destination=north_europe_main')

    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 5
    assert all(item['average_price'] is not None for item in data)

def test_rates_single_date(client, db):
    response = client.get('/rates?date_from=2023-01-01&date_to=2023-01-01&origin=CNSGH&destination=NLRTM')

    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1
    assert data[0]['day'] == '2023-01-01'
    assert data[0]['average_price'] == 1001

def test_rates_no_data_for_date_range(client, db):
    response = client.get('/rates?date_from=2022-12-01&date_to=2022-12-05&origin=CNSGH&destination=NLRTM')

    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 5
    assert all(item['average_price'] is None for item in data)

def test_rates_integer_average_price(client, db):
    response = client.get('/rates?date_from=2023-01-01&date_to=2023-01-05&origin=CNSGH&destination=NLRTM')

    assert response.status_code == 200
    data = json.loads(response.data)
    assert all(isinstance(item['average_price'], int) or item['average_price'] is None for item in data)

def test_rates_null_prices(client, db):    
    # Delete prices for a specific day
    with db.cursor() as cur:
        cur.execute("DELETE FROM prices WHERE day = '2023-01-03'")
    db.commit()
    
    response = client.get('/rates?date_from=2023-01-01&date_to=2023-01-05&origin=CNSGH&destination=NLRTM')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 5
    assert any(item['average_price'] is None for item in data)
    assert any(item['day'] == '2023-01-03' and item['average_price'] is None for item in data), "Expected 2023-01-03 to have None average_price"
