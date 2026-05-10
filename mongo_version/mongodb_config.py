import os

from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "scientific_paper_engine")
RAW_COLLECTION_NAME = os.getenv("MONGO_RAW_COLLECTION", "arxiv_data")
CLEANED_COLLECTION_NAME = os.getenv(
    "MONGO_CLEANED_COLLECTION",
    "after_cleaning_final_research_data",
)


def get_database():
    client = MongoClient(MONGO_URI)
    return client[MONGO_DB_NAME]


def get_raw_collection():
    return get_database()[RAW_COLLECTION_NAME]


def get_cleaned_collection():
    return get_database()[CLEANED_COLLECTION_NAME]
