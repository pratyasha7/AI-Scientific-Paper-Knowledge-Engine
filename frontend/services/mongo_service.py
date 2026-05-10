import os
import sys
from pymongo import MongoClient
from dotenv import load_dotenv

# Add parent directory to path to import from mongo_version if needed
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "scientific_paper_engine")
CLEANED_COLLECTION_NAME = os.getenv("MONGO_CLEANED_COLLECTION", "after_cleaning_final_research_data")

class MongoService:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[MONGO_DB_NAME]
        self.collection = self.db[CLEANED_COLLECTION_NAME]

    def get_all_papers(self, limit=1000):
        return list(self.collection.find({}, {"_id": 0}).limit(limit))

    def get_paper_by_url(self, url):
        return self.collection.find_one({"url": url}, {"_id": 0})

    def get_trending_keywords(self, top_n=10):
        # Aggregation to find most common keywords
        pipeline = [
            {"$unwind": "$cleaned_keywords"},
            {"$group": {"_id": "$cleaned_keywords", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": top_n}
        ]
        return list(self.collection.aggregate(pipeline))

    def get_stats(self):
        total_papers = self.collection.count_documents({})
        # Placeholder for other stats
        return {
            "total_papers": total_papers,
            "sources": ["arXiv"],
            "last_updated": "Recently"
        }
