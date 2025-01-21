from dotenv import load_dotenv
from flask import Flask, jsonify, make_response, Response, request
from flask_cors import CORS
from werkzeug.exceptions import BadRequest, Unauthorized
import logging
from weather_app.models import favorite_locations_model
from weather_app.utils.logger import configure_logger
from weather_app.models.user_model import User
from weather_app.utils.weather_client import WeatherClient
from db.db_connection import get_database
import re

from config import ProductionConfig
# Load environment variables from .env file
load_dotenv()

app=Flask(__name__)
CORS(app)

logger = logging.getLogger(__name__)
configure_logger(logger)

database = get_database()
dbusers = database["Users"]
dbfavorites = database["Favorite Locations"]

    ####################################################
    #
    # Healthchecks
    #
    ####################################################

@app.route('/healthcheck', methods=['GET'])
def healthcheck() -> Response:
        """
        Health check route to verify the service is running.

        Returns:
            JSON response indicating the health status of the service.
        """
        logger.info('Health check')
        try:
             db = database.admin
             response = db.command("ping")
             logger.info("Health check passed")
             return make_response(jsonify({'status': 'healthy'}), 200)
        except Exception as e:
             logger.error("Health check failed")
             return make_response(jsonify({"Health check failed:",str(e)}))




    ##########################################################
    #
    # Favorite Locations Management
    #
    ##########################################################

@app.route('/favorites/add', methods=['POST'])
def add_location() -> Response:
        """
        Route to add a new location to favorite locations.

        Expected JSON Input:
            - location_name (str): the location's name
            - user_id (int): The user ID .

        Returns:
            JSON response indicating the success of the location addition.
        Raises:
            400 error if input validation fails.
            500 error if there is an issue adding the location to the favorites.
        """
        logger.info('Adding a new location to favorites')
        try:
            data = request.get_json()

            user_id = data.get('user_id')
            location_name = data.get('location_name')

            if not user_id or not location_name:
                logger.error('Invalid input: user_id and location_name are required')
                return make_response(jsonify({'error': 'Invalid input, all fields are required with valid values'}), 400)

            # Add the song to the playlist
            logger.info('Adding location:', location_name)
            favorite_locations_model.FavoriteLocations.add_favorite(user_id=user_id,location_name=location_name)
            logger.info("Location added to favorites: ", location_name)
            return make_response(jsonify({'status': 'success', 'location': location_name}), 201)
        except Exception as e:
            logger.error("Failed to add location: %s", str(e))
            return make_response(jsonify({'error': str(e)}), 500)


@app.route('/favorites/delete/', methods=['DELETE'])
def delete_location() -> Response:
        """
        Route to delete a location by its name.

        Path Parameter:
            - user_id (int): The ID of the user.
            - location_name (str): The name of the location to delete

        Returns:
            JSON response indicating success of the operation or error message.
        """
        data = request.get_json()
        location_name = data.get("location_name")
        user_id = data.get("user_id")
        try:
            logger.info(f"Deleting location by name: {location_name}")
            favorite_locations_model.FavoriteLocations.delete_favorite(user_id=user_id,location_name=location_name)
            return make_response(jsonify({'status': 'success'}), 200)
        except Exception as e:
            logger.error(f"Errorw deleting location: {e}")
            return make_response(jsonify({'error': str(e)}), 500)
@app.route('/favorites/get-all-favs/', methods =['GET'] )
def get_all_favs():
     user_id = request.args.get("user_id")
     try:
          logger.info(f"Fetching all favorites for user_id: {str(user_id)}")
          favlocs = favorite_locations_model.FavoriteLocations.get_favorites(user_id)
          logger.info(f"Favorite locs: {favlocs}")
          if favlocs==[]:
                return make_response(jsonify({"error":"No favorite locations for user exist"}),404)
          else:
            return make_response(jsonify({"status":"success", "favorite_locations":favlocs}),200)
     except Exception as e:
          logger.error(f"Error fetching all favorites: {e}")
          return make_response(jsonify({'error': str(e)}), 500)
     


@app.route('/favorite/get-weather-for-favo/', methods=['GET'])
def get_weather_for_favorite() -> Response:
        """
        Route to retrieve the weather at a specific location by its name.

        Path Parameter:
            - location_name (str): The name of the desired location

        Returns:
            JSON response with the song details or error message.
        """
        location_name = request.args.get("location_name")
        user_id =  request.args.get("user_id")
        try:
            if location_name not in favorite_locations_model.FavoriteLocations.get_favorites(user_id):
                 return make_response(jsonify({'error':"Location not one of your favorites"}), 404)
            logger.info(f"Retrieving weather by location name: {location_name}")
            weather = favorite_locations_model.FavoriteLocations.get_weather_for_favorite(location_name)
            logger.info(f"Weather is {weather}")
            return make_response(jsonify({'status': 'success', 'weather_loc': weather}), 200)
        except Exception as e:
            logger.error(f"Error retrieving weather at location by name: {e}")
            return make_response(jsonify({'error': str(e)}), 500)
        

@app.route('/weather/favorites', methods=['GET'])
def get_weather_for_favorites() -> Response:
        """
        Route to retrieve weather information for all favorite locations of a user.

        Expected JSON Input:
            - user_id (int): The ID of the user.

        Returns:
            JSON response with the list of favorite locations and their weather data.
        """
        try:
            user_id = request.args.get("user_id")
            if not user_id:
                logger.error("Invalid input: 'user_id' is required.")

            logger.info("Fetching weather data for all favorite locations for user_id %s", user_id)

            # Assuming you have an initialized WeatherClient instance (e.g., weather_client)
            from weather_app.utils.weather_client import WeatherClient  # Import your weather client utility
            weather_client = WeatherClient()

            locations_with_weather = favorite_locations_model.FavoriteLocations.get_all_favorites_with_weather(user_id)
            logger.info(f"Locations with weather: {locations_with_weather}")
            #return make_response(jsonify({'status': 'success', 'locations': locations_with_weather}), 200)
            return Response(response=locations_with_weather, content_type='text/plain')

        except Exception as e:
            logger.error(f"Error retrieving weather data for favorites: {e}")
            return make_response(jsonify({'error': str(e)}), 500)
        
@app.route('/favorite/daily/', methods=['GET'])
def get_daily_forecast() -> Response:
        """
        Route to retrieve the weather at a specific location by its name.

        Path Parameter:
            - location_name (str): The name of the desired location

        Returns:
            JSON response with the song details or error message.
        """
        location_name = request.args.get("location_name")
        user_id =  request.args.get("user_id")
        try:
            if location_name not in favorite_locations_model.FavoriteLocations.get_favorites(user_id):
                 return make_response(jsonify({'status':'error','error':"Location not one of your favorites"}))
            logger.info(f"Retrieving daily forecast by location name: {location_name}")
            weather = favorite_locations_model.FavoriteLocations.get_daily_forecast(location_name)
            return make_response(jsonify({'status': 'success', 'daily_forecast': weather}), 200)
        except Exception as e:
            logger.error(f"Error retrieving weather at location by name: {e}")
            return make_response(jsonify({'error': str(e)}), 500)
        
@app.route('/favorite/hourly/', methods=['GET'])
def get_hourly_forecast() -> Response:
        """
        Route to retrieve the weather at a specific location by its name.

        Path Parameter:
            - location_name (str): The name of the desired location

        Returns:
            JSON response with the song details or error message.
        """
        location_name = request.args.get("location_name")
        user_id =  request.args.get("user_id")
        try:
            if location_name not in favorite_locations_model.FavoriteLocations.get_favorites(user_id):
                 return make_response(jsonify({'status':'error','error':"Location not one of your favorites"}))
            logger.info(f"Retrieving hourly forecast by location name: {location_name}")
            weather = favorite_locations_model.FavoriteLocations.get_hourly_forecast(location_name)
            return make_response(jsonify({'status': 'success', 'hourly_forecast': weather}), 200)
        except Exception as e:
            logger.error(f"Error retrieving weather at location by name: {e}")
            return make_response(jsonify({'error': str(e)}), 500)

        

    ############################################################
    #
    # User Management
    #
    ############################################################

@app.route('/user/create', methods=['POST'])
def create_user():
        """
        Route to create a new user.

        Expected JSON Input:
            - username (str): The username for the user.
            - password (str): The password for the user.

        Returns:
            JSON response indicating the success of user creation.
        Raises:
            400 error if input validation fails.
            500 error if there is an issue creating the user.
        """
        try:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
            confirmpas = data.get("confirmPass")
            
        
            if not username or not password:
                logger.error("Invalid input: 'username' and 'password' are required.")
                return make_response(jsonify({'error': 'Invalid input, both username and password are required'}), 400)
            
            if len(password)<8:
                 logger.error("Invalid input: Password must be greater than 8 characters long")
                 return make_response(jsonify({'error': 'Invalid input, password must be greater than 8 characters'}), 400)
            

            if not re.search(r'[A-Z]', password):
                 logger.error("Password must contain at least one uppercase letter.")
                 return make_response(jsonify({'error': 'Password must contain at least one uppercase letter'}), 400)
        
            if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):  # checks for special characters
                logger.error("Password must contain a special character.")
                return make_response(jsonify({'error': 'Password must contain a special character'}), 400)

            if confirmpas!=password:
                 logger.error("Passwords do not match")
                 return make_response(jsonify({'error': 'Invalid input, passwords do not match'}), 400)


            logger.info(f"Creating user: {username}")
            try:
                User.create_user(username, password)
            except ValueError as ve:
                 logger.error(f"ValueError caught: {ve}")
                 return make_response(jsonify({'status': 'error','error': str(ve)}), 404)

            logger.info(f"User created successfully: {username}")
            return make_response(jsonify({'status': 'user added', 'username': username}), 201)
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            return make_response(jsonify({'error': str(e)}), 500)

@app.route('/user/login', methods=['POST'])
def login() -> Response:
        """
        Route to log in a user and load their combatants.

        Expected JSON Input:
            - username (str): The username of the user.
            - password (str): The user's password.

        Returns:
            JSON response indicating the success of the login.

        Raises:
            400 error if input validation fails.
            401 error if authentication fails (invalid username or password).
            500 error for any unexpected server-side issues.
        """
        try: 
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                    logger.error("Invalid login payload.")
                    return make_response((jsonify({'status': 'error', 'error': 'Username and password must be filled'}), 400))
            
            if User.check_password(username, password):
                    user_id = User.get_id_by_username(username)
                    logger.info(f"User '{username}' logged in successfully")
                    return make_response(jsonify({'status': 'success', 'message': 'Login successful', 'user_id': str(user_id)}), 200)
            else:
                logger.warning(f"Invalid login attempt for username '{username}'")
                return make_response(jsonify({'status': 'error', 'error': 'Invalid username or password'}), 401)
        except Exception as e:
            logger.error("Error during login for username %s: %s", username, str(e))
            return jsonify({"error": "An unexpected error occurred."}), 500



@app.route('/user/update_password/', methods=['POST'])
def update_password() -> Response:
        """
        Route to remove a location from the user's favorite locations.

        Path Parameter:
            - username (str): User's username.

        Returns:
            JSON response indicating the success of the password update.
        """
        try:
            data = request.get_json()
            username = data.get('username')
            old_password = data.get('password')
            new_password = data.get('newPassword')

            if not username or not old_password or not new_password:
                logger.error("Invalid input: 'username', 'old_password', and 'new_password' are required.")
                return make_response(jsonify({'status':'error','error':"Must have an input in all fields"}),400)


            # Verify current password
            if not User.check_password(username=username, password=old_password):
                logger.warning(f"Password mismatch for user '{username}'.")
                return make_response(jsonify({'status':'error','error':"Username or password are incorrect"}),401)

            # Update password
            try:
                User.update_password(username=username, new_password=new_password)
            except ValueError as ve:
                logger.warning(f"Failed to update password: {ve}")
                return make_response(jsonify({'status': 'error', 'error': str(ve)}), 404) 
                
            return make_response(jsonify({'status': 'success', 'message': 'Password updated successfully'}), 200)
        except Exception as e:
            logger.error(f"Error updating password: {e}")
            return make_response(jsonify({'error': str(e)}), 500)

