
from pymongo import MongoClient
import pymongo

from config import MONGO_DB_ADDRESS


client = MongoClient(MONGO_DB_ADDRESS, serverSelectionTimeoutMS=1)
yelp_database = client['yelp']

words_hit_count_collection = yelp_database['words_hit_count']

print(len(words_hit_count_collection.find().distinct('word')))



