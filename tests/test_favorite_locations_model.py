import pytest
from weather_app.models.favorite_locations_model import FavoriteLocations
from weather_app.models.user_model import User
import logging

logger = logging.getLogger(__name__)

@pytest.fixture()
def Favorite_Locations():
    """Fixture to provide a new instance of PlaylistModel for each test."""
    return FavoriteLocations()

@pytest.fixture()
def user():
    return User()


##################################################
# Add Song Management Test Cases
##################################################


def test_add_favorite_new(user, Favorite_Locations):
    user_id = user.get_id_by_username("Hello")
    Favorite_Locations.add_favorite(user_id, "New York")

    favorites = Favorite_Locations.get_favorites(user_id)
    assert "New York" in favorites
    Favorite_Locations.delete_favorite(user_id, "New York")

def test_add_favorite_two(user, Favorite_Locations):
        userID = user.get_id_by_username("Hello")
        Favorite_Locations.add_favorite(userID, "Philly")
        Favorite_Locations.add_favorite(userID, "London")
        favorites = Favorite_Locations.get_favorites(userID)
        try:
            assert "Philly" in favorites and "London" in favorites
        finally:
            Favorite_Locations.delete_favorite(userID, "Philly")
            Favorite_Locations.delete_favorite(userID, "London")

def test_get_favorites(user, Favorite_Locations):
    userID = user.get_id_by_username("Hello")
    Favorite_Locations.add_favorite(userID, "Philly")
    Favorite_Locations.add_favorite(userID, "London")
    favorites = Favorite_Locations.get_favorites(userID)
    try:
        assert "Philly", "London" == favorites
    finally:
        Favorite_Locations.delete_favorite(userID, "Philly")
        Favorite_Locations.delete_favorite(userID, "London")

def test_delete_favorite(user, Favorite_Locations):
    userID = user.get_id_by_username("Hello")
    Favorite_Locations.add_favorite(userID, "New York City")
    Favorite_Locations.add_favorite(userID, "Philly")
    Favorite_Locations.delete_favorite(userID, "Philly")
    favorites = Favorite_Locations.get_favorites(userID)
    try:
        assert "Philly" not in favorites
    finally:
        Favorite_Locations.delete_favorite(userID, "New York")

def test_get_weather_for_favorite(user, Favorite_Locations):
    userID = user.get_id_by_username("Hello")
    Favorite_Locations.add_favorite(userID, "Boston")
    result = Favorite_Locations.get_weather_for_favorite("Boston")
    try:
        assert result is not None
    finally:
        Favorite_Locations.delete_favorite(userID, "Boston")

def test_get_weather_for_all_favorites(user, Favorite_Locations):
    userID = user.get_id_by_username("Hello")
    Favorite_Locations.add_favorite(userID, "New York")
    Favorite_Locations.add_favorite(userID, "Boston")
    Favorite_Locations.add_favorite(userID, "Chicago")
    all_weather = Favorite_Locations.get_all_favorites_with_weather(userID)
    try:
        assert len(all_weather) == 3
    finally:
        Favorite_Locations.delete_favorite(userID, "New York")
        Favorite_Locations.delete_favorite(userID, "Boston")
        Favorite_Locations.delete_favorite(userID, "Chicago")



def test_get_daily_forecast(user, Favorite_Locations):
    userID = user.get_id_by_username("Hello")
    Favorite_Locations.add_favorite(userID, "New York")
    Favorite_Locations.add_favorite(userID, "Boston")
    Favorite_Locations.add_favorite(userID, "Chicago")
    forecast = Favorite_Locations.get_daily_forecast("Chicago")
    try:
        assert forecast is not None
    finally:
        Favorite_Locations.delete_favorite(userID, "New York")
        Favorite_Locations.delete_favorite(userID, "Boston")
        Favorite_Locations.delete_favorite(userID, "Chicago")

