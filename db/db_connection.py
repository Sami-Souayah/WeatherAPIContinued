from pymongo import MongoClient
from dotenv import load_dotenv
import logging
from weather_app.utils.logger import configure_logger

logger = logging.getLogger(__name__)
configure_logger(logger)

import os

load_dotenv()
def get_database():
    try:
        logger.info("Connecting to database")
        CONNECTION_STRING = os.getenv("CONNECTION_STRINGDB")
        client = MongoClient(CONNECTION_STRING)
        return client["Users"]
    except:
        logger.error("DB connection failed")

if __name__=="__main__":
    dbname = get_database()



