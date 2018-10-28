#!/usr/bin/python3
import json
from pymongo import MongoClient
from config import MONGO_DB_ADDRESS

client = MongoClient(MONGO_DB_ADDRESS, serverSelectionTimeoutMS=1)
yelp_database = client['yelp']
PROCESSED_REVIEWS = 'processed_reviews'
processed_collection = yelp_database['processed_reviews']

first_million_collection = yelp_database['first_millions']

if __name__ == '__main__':
    cur = processed_collection.find().limit(100000)
    first_million_collection.insert_many(cur)
    # count = 0
    # for doc in cur:
    #     if count % 100 == 0:
    #         print(count)
    #     if count >= 1E5:
    #         break
    #     first_million_collection.insert_one(doc, w=0)
    #     count += 1

