import hashlib
import logging
import os
from db.db_connection import get_database

from weather_app.utils.logger import configure_logger

logger = logging.getLogger(__name__)
configure_logger(logger)

dbname = get_database()
dbname = dbname["Users"]


class User():
    id = int
    username = str
    salt = str  # 16-byte salt in hex
    password = str # SHA-256 hash in hex
    
    @classmethod
    def _generate_hashed_password(cls, password: str) -> tuple[str, str]:
        """
        Generates a salted, hashed password.

        Args:
            password (str): The password to hash.

        Returns:
            tuple: A tuple containing the salt and hashed password.
        """
        salt = os.urandom(16).hex()
        hashed_password = hashlib.sha256((password + salt).encode()).hexdigest()
        return salt, hashed_password

    @classmethod
    def create_user(cls, username: str, password: str) -> None:
        """
        Create a new user with a salted, hashed password.

        Args:
            username (str): The username of the user.
            password (str): The password to hash and store.

        Raises:
            ValueError: If a user with the username already exists.
        """
        salt, hashed_password = cls._generate_hashed_password(password)
        logger.info("Attempting to create user")
        try:
            existing_user = dbname.find_one({"Username": username})
            if existing_user:
                logger.error("Duplicate username: %s", username)
                raise ValueError(f"User with username '{username}' already exists")

            dbname.insert_one({"Username":username, "Salt":salt,"Hashed password":hashed_password})
            logger.info("User successfully added to the database: %s", username)
        except ValueError:
             raise
        except Exception as e:
                logger.error(f"Database error: {e}")
                raise

    @classmethod
    def check_password(cls, username: str, password: str) -> bool:
        """
        Check if a given password matches the stored password for a user.

        Args:
            username (str): The username of the user.
            password (str): The password to check.

        Returns:
            bool: True if the password is correct, False otherwise.

        Raises:
            ValueError: If the user does not exist.
        """
        user = dbname.find_one({"Username":username})
        logger.info(f"Attempting to check password for {username}")
        if not user:
            logger.info("User %s not found", username)
            return ValueError(f"User {username} not found")
        try:
            hashed_password = user["Hashed password"]
            userpass = hashlib.sha256((password + user["Salt"]).encode()).hexdigest()
            return hashed_password == userpass
        except:
            logger.info("Error when conducting check_password")

            
    @classmethod
    def get_id_by_username(cls, username: str) -> int:
        """
        Retrieve the ID of a user by username.

        Args:
            username (str): The username of the user.

        Returns:
            int: The ID of the user.

        Raises:
            ValueError: If the user does not exist.
        """
        user = dbname.find_one({"Username":username})
        logger.info("Attempting to find ID with username")
        try:
            if not user:
                logger.info("User %s not found", username)
                return ValueError(f"User {username} not found")
            else:
                logger.info("Success in findng ID with username")
                return user["_id"]
        except:
            logger.error("Error during get_id_by_username function")


    @classmethod
    def update_password(cls, username: str, new_password: str) -> None:
        """
        Update the password for a user.

        Args:
            username (str): The username of the user.
            new_password (str): The new password to set.

        Raises:
            ValueError: If the user does not exist.
        """
        user = dbname.find_one({"Username":username})
        try:
            if not user:
                logger.error("User %s not found", username)
                raise ValueError(f"User {username} not found")
            else:
                salt,hashed_password = User._generate_hashed_password(new_password)
                dbname.update_one(
                {"Username": username}, 
                {"$set": {"Salt": salt, "Hashed password": hashed_password}})
                logger.info("Password updated")
        except Exception as e:
            logger.error("Error replacing password:", e)
    
    @classmethod
    def delete_user(cls, username: str) -> None:
        """Deletes user. For internal use only, not to be implemented on the front end side"""
        user = dbname.find_one({"Username": username})
        try:
            if not user:
                logger.error("User %s not found", username)
                raise ValueError(f"User {username} not found")
            else:
                dbname.delete_one(user)
                logger.info("User %s deleted", username)
        except Exception as e:
            logger.error("Error deleting user:", e)

