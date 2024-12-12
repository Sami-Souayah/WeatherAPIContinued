import logging
from typing import List, Any
from dataclasses import asdict, dataclass
from db.db_connection import get_database

from weather_app.utils.logger import configure_logger
from weather_app.utils.weather_client import WeatherClient


logger = logging.getLogger(__name__)
configure_logger(logger)

dbname = get_database()
dbname = dbname["Favorite Locations"]


@dataclass
class FavoriteLocations():
    """
    This class represents a user's favorite locations
    """

    Locid: str
    user_id: str
    location_name: str

    """
    A class to manage a list of favorite locations.

    Attributes:
        id (int): The ID of the user associated with the favorite locations.
    """


    ##################################################
    # Locationa Management Functions
    ##################################################
    @classmethod
    def add_favorite(cls, user_id: int, location_name: str) -> None:
        """
        Adds a favorite location for a user.

        Args:
            user_id (int): The user's ID.
            location_name (str): The location to add.

        Raises:
            ValueError: If the location is already a favorite.
        """

        logger.info("Adding favorite location '%s' for user_id %s", location_name, str(user_id))
        try:
           existing_user = dbname.find_one({"UserID": user_id})
           if existing_user:
               if location_name in FavoriteLocations.get_favorites(user_id):
                    logger.warning("Location '%s' is already a favorite for user_id %s", location_name, str(user_id))
                    return ValueError(f"Location '{location_name}' is already a favorite.")
               dbname.update_one({"UserID":user_id}, {"$push":{"Location names":location_name}})
           else:
                dbname.insert_one({"UserID":user_id,"Location names":[location_name]})
                logger.info("Added location to user's favorite locations")
        except:
            logger.error("Error adding location to user's favorite locations")

    @classmethod
    def get_favorites(cls, user_id: int):
        """
        Retrieves all favorite locations for a user.

        Args:
            user_id (int): The user's ID.

        Returns:
            List[dict[str, Any]]: List of favorite locations as dictionaries.
        """
        logger.info("Fetching favorite locations for user_id %s", user_id)
        favorites = dbname.find_one({"UserID":user_id})
        if not favorites["Location names"]:
            logger.info("No favorite locations found for user_id %s", user_id)
            return []
        logger.info("Fetched favorite locations for user")
        print(favorites["Location names"])
        return favorites["Location names"]
    
    @classmethod
    def delete_favorite(cls, user_id: int, location_name: str):
        """
        Deletes a favorite location for a user.

        Args:
            user_id (int): The user's ID.
            location_name (str): The location to delete.

        Raises:
            ValueError: If the location is not found.
        """
        logger.info("Deleting favorite location '%s' for user_id %s", location_name, user_id)
        favorites = dbname.find_one({"UserID":user_id})
        if not favorites["Location names"]:
            logger.info("No favorite locations found for user_id %s", user_id)
            return []
        try:
            dbname.update_one({"UserID":user_id},{"$pull":{"Location names":location_name}})
            logger.info("Location pulled from existing list")
        except:
            logger.error("Location not found on existing list or error with function")

    @classmethod
    def get_favorite_by_id(cls, favorite_id: int):
        """
        Retrieves a favorite location by its ID.

        Args:
            favorite_id (int): The ID of the favorite location.

        Returns:
            dict[str, Any]: The favorite location data.

        Raises:
            ValueError: If the favorite location is not found.
        """
        logger.info("Fetching favorite location by ID: %s", favorite_id)
        favorite = dbname.find_one({"_id":favorite_id})
        if not favorite:
            logger.error("Favorite location with ID %s not found", favorite_id)
            return ValueError(f"Favorite location with ID {favorite_id} not found.")
        logger.info("Fetched favorite location by ID")
        return asdict(favorite)
    
    ##################################################
    # Weather API Integration
    ##################################################

    @classmethod
    def get_weather_for_favorite(cls, location_name) -> dict[str, Any]:
        """
        Retrieves the weather data for a favorite location.

        Args:
            location_name (str): The name of the location.
            weather_client (WeatherClient): The weather client to use.

        Returns:
            dict[str, Any]: The weather data for the location.

        Raises:
            ValueError: If fetching weather data fails.
        """
        logger.info("Fetching weather for location '%s'", location_name)
        try: 
            weathercl = WeatherClient()
            weather_data = weathercl.get_weather(location_name)
            logger.info("Weather data for '%s': %s", location_name, weather_data)
            return weather_data
        except Exception as e:
            logger.error("Error fetching weather for location '%s': %s", location_name, str(e))
            raise ValueError(f"Error fetching weather for location '{location_name}': {str(e)}")
        
    @classmethod
    def get_all_favorites_with_weather(cls, user_id: int):
        """
        Retrieves all favorite locations for a user along with their weather data.

        Args:
            user_id (int): The user's ID.
            weather_client (WeatherClient): The weather client to use.

        Returns:
            List[dict[str, Any]]: List of favorite locations with weather data.
        """
        favorites = dbname.find_one({"UserID":user_id})
        result = []
        for fav in favorites["Location names"]:
            result+=[FavoriteLocations.get_weather_for_favorite(fav)]
        return result
    
    @classmethod

    def get_hourly_forecast(cls, location_name):
          """
        Retrieves hourly forecast for a specified location.

        Args:
            location_name (str): The name of the location


        Returns:
            Weather data
        """
          logger.info("Fetching weather for location '%s'", location_name)
          try:
            weathercl = WeatherClient()
            weather_data = weathercl.get_hourly_forecast(location_name)
            logger.info("Weather data for '%s': %s", location_name, weather_data)
            return weather_data
          except Exception as e:
            logger.error("Error fetching weather for location '%s': %s", location_name, str(e))
            raise ValueError(f"Error fetching weather for location '{location_name}': {str(e)}")
    
    @classmethod

    def get_daily_forecast(cls, location_name):
          """
        Retrieves daily forecast for a specified location.

        Args:
            location_name (str): The name of the location

        Returns:
           Weather data
        """
          logger.info("Fetching weather for location '%s'", location_name)
          try:
            weathercl = WeatherClient()
            weather_data = weathercl.get_daily_forecast(location_name)
            logger.info("Weather data for '%s': %s", location_name, weather_data)
            return weather_data
          except Exception as e:
            logger.error("Error fetching weather for location '%s': %s", location_name, str(e))
            raise ValueError(f"Error fetching weather for location '{location_name}': {str(e)}")
    
    @classmethod

    def get_dated_forecast(cls, location_name, date_tm):
          """
        Retrieves daily forecast for a specified location and date up to 45 years in the past and 1.5 years in the future.

        Args:
            location_name (str): The name of the location
            date_tm (str): The date in YYYY-MM-DD format

        Returns:
           Weather data
        """
          logger.info("Fetching weather for location '%s'", location_name)
          try:
            weathercl = WeatherClient()
            weather_data = weathercl.get_date_forecast(location_name, date_tm)
            logger.info("Weather data for '%s': %s", location_name, weather_data)
            return weather_data
          except Exception as e:
            logger.error("Error fetching weather for location '%s': %s", location_name, str(e))
            raise ValueError(f"Error fetching weather for location '{location_name}': {str(e)}")