import pytest
from weather_app.models.favorite_locations_model import FavoriteLocations
from weather_app.models.user_model import User

@pytest.fixture()
def Favorite_Locations():
    """Fixture to provide a new instance of PlaylistModel for each test."""
    return FavoriteLocations()

@pytest.fixture()
def user():
    return User()

@pytest.fixture
def mock_update_play_count(mocker):
    """Mock the update_play_count function for testing purposes."""
    return mocker.patch("music_collection.models.playlist_model.update_play_count")


##################################################
# Add Song Management Test Cases
##################################################


def test_add_favorite_new(user, favorite_locations):
    user_id = user.get_id_by_username("Hello")
    favorite_locations.add_favorite(user_id, "New York")

    favorites = favorite_locations.get_favorites(user_id)
    assert "New York" in favorites

def test_add_favorite_two():
    try:
        userID = user.get_id_by_username("Hello")
        Favorite_Locations.add_favorite(userID, "Philly")
        Favorite_Locations.add_favorite(userID, "London")
    except Exception as e:
        print("Failed because of:",e)

def test_get_favorites():
    userID = user.get_id_by_username("Hello")
    Favorite_Locations.add_favorite(userID, "Philly")
    Favorite_Locations.add_favorite(userID, "London")
    favorites = Favorite_Locations.get_favorites(userID)
    assert {"Philly", "London"} <= set(favorites)

def test_delete_favorite():
    userID = user.get_id_by_username("Hello")
    Favorite_Locations.add_favorite(userID, "New York City")
    Favorite_Locations.add_favorite(userID, "Philly")
    Favorite_Locations.delete_favorite(userID, "Philly")
    favorites = Favorite_Locations.get_favorites(userID)
    assert "Philly" not in favorites

def test_get_weather_for_favorite():
    userID = user.get_id_by_username("Hello")
    Favorite_Locations.add_favorite(userID, "Boston")
    result = Favorite_Locations.get_weather_for_favorite("Boston")
    assert result is not None

def test_get_weather_for_all_favorites():
    userID = user.get_id_by_username("Hello")
    Favorite_Locations.add_favorite(userID, "New York")
    Favorite_Locations.add_favorite(userID, "Boston")
    Favorite_Locations.add_favorite(userID, "Chicago")
    all_weather = Favorite_Locations.get_all_favorites_with_weather(userID)
    assert len(all_weather) == 3

def test_get_daily_forecast():
    userID = user.get_id_by_username("Hello")
    Favorite_Locations.add_favorite(userID, "New York")
    Favorite_Locations.add_favorite(userID, "Boston")
    Favorite_Locations.add_favorite(userID, "Chicago")
    forecast = Favorite_Locations.get_daily_forecast("Chicago")
    assert forecast is not None

