from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
def get_database():
    CONNECTION_STRING = os.getenv("CONNECTION_STRINGDB")
    client = MongoClient(CONNECTION_STRING)
    return client["Users"]

if __name__=="__main__":
    dbname = get_database()
