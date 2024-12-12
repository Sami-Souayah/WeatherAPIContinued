from pymongo import MongoClient
from dotenv import load_dotenv
import logging
from weather_app.utils.logger import configure_logger
import os

logger = logging.getLogger(__name__)
configure_logger(logger)

load_dotenv()
def get_database():
    try:
        logger.info("Connecting to database")
        CONNECTION_STRING = os.getenv("CONNECTION_STRING")
        client = MongoClient(CONNECTION_STRING)
        logger.info("Success")
        return client["UserDatabase"]
    except:
        logger.error("DB connection failed")

if __name__=="__main__":
    dbname = get_database()
def get_client():
    try:
        logger.info("Connecting to database")
        CONNECTION_STRING = os.getenv("CONNECTION_STRINGDB")
        client = MongoClient(CONNECTION_STRING)
        return client
    except:
        logger.error("DB connection failed")



