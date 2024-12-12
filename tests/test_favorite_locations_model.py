import pytest

from weather_app.models.favorite_locations_model import FavoriteLocations
from weather_app.models.user_model import User


@pytest.fixture()
def Favorite_Locations():
    """Fixture to provide a new instance of PlaylistModel for each test."""
    return FavoriteLocations()

@pytest.fixture
def mock_update_play_count(mocker):
    """Mock the update_play_count function for testing purposes."""
    return mocker.patch("music_collection.models.playlist_model.update_play_count")


@pytest.fixture
def sample_playlist(sample_song1, sample_song2):
    return [sample_song1, sample_song2]


##################################################
# Add Song Management Test Cases
##################################################

def test_add_favorite_new():
    User.create_user("Hello","poopoo")
    userID = User.get_id_by_username("Hello")
    FavoriteLocations.add_favorite(userID, "New York")

def test_add_favorite_two():
    User.create_user("Hello","poopoo")
    userID = User.get_id_by_username("Hello")
    FavoriteLocations.add_favorite(userID, "Philly")
    FavoriteLocations.add_favorite(userID, "London")
def test_get_favorites():
    User.create_user("Hello","poopoo")
    userID = User.get_id_by_username("Hello")
    FavoriteLocations.add_favorite(userID, "Philly")
    FavoriteLocations.add_favorite(userID, "London")
    FavoriteLocations.get_favorites(userID)

def test_delete_favorite():
    User.create_user("Hello","poopoo")
    userID = User.get_id_by_username("Hello")
    FavoriteLocations.add_favorite(userID, "New York City")
    FavoriteLocations.add_favorite(userID, "Philly")
    FavoriteLocations.delete_favorite(userID, "Philly")
    FavoriteLocations.get_favorites(userID)

def test_get_weather_for_favorite(locname):
    User.create_user("Hello","poopoo")
    userID = User.get_id_by_username("Hello")
    FavoriteLocations.add_favorite(userID, locname)
    FavoriteLocations.get_weather_for_favorite(locname)

def test_get_weather_for_all_favorites():
    User.create_user("Hello","poopoo")
    userID = User.get_id_by_username("Hello")
    FavoriteLocations.add_favorite(userID, "New York")
    FavoriteLocations.add_favorite(userID, "Boston")
    FavoriteLocations.add_favorite(userID, "Chicago")
    FavoriteLocations.get_all_favorites_with_weather(userID)

test_get_weather_for_all_favorites()