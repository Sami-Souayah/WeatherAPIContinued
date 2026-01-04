import pytest
from unittest.mock import patch
from weather_app.utils.weather_client import WeatherClient,get_lat_long



##################################################
# Add Song Management Test Cases
##################################################

@pytest.fixture
def client():
    return WeatherClient(base_url="https://api.openweathermap.org/data/2.5/weather?")


def test_lat_log():
    result = get_lat_long("New York")
    assert result == (40.7127281, -74.0060152)
def test_get_weather_Valid_location(client):
    result = client.get_weather("New York")
    return result