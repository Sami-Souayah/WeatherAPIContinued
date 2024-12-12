import hashlib
import logging
import os
from db.db_connection import get_database

from sqlalchemy.exc import IntegrityError
from weather_app.utils.logger import configure_logger

logger = logging.getLogger(__name__)
configure_logger(logger)

dbname = get_database()

class User():
    __tablename__ = 'users'

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
        try:
            count = dbname["Users"].count_documents({})+1
            name = dbname[username]
            name.insert_one({"Salt:":salt,"Hashed password:":hashed_password, "UserID:":count})
            logger.info("User successfully added to the database: %s", username)
        except IntegrityError:
            existing_user = name.find_one({"username": username})
            if existing_user:
                name.delete_one(username)
                logger.error("Duplicate username: %s", username)
                raise ValueError(f"User with username '{username}' already exists")
        except Exception as e:
            logger.error("Database error: %s", str(e))
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
        user = cls.query.filter_by(username=username).first()
        if not user:
            logger.info("User %s not found", username)
            raise ValueError(f"User {username} not found")
        hashed_password = hashlib.sha256((password + user.salt).encode()).hexdigest()
        return hashed_password == user.password

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
        user = cls.query.filter_by(username=username).first()
        if not user:
            logger.info("User %s not found", username)
            raise ValueError(f"User {username} not found")
        return user.id

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
        user = cls.query.filter_by(username=username).first()
        if not user:
            logger.info("User %s not found", username)
            raise ValueError(f"User {username} not found")

        salt, hashed_password = cls._generate_hashed_password(new_password)
        user.salt = salt
        user.password = hashed_password
        db.session.commit()
        logger.info("Password updated successfully for user: %s", username)