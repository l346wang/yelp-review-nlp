#!/usr/bin/python3
import json
from pymongo import MongoClient
from dateutil import parser

from config import MONGO_DB_ADDRESS

client = MongoClient(MONGO_DB_ADDRESS, serverSelectionTimeoutMS=1)
yelp_database = client['yelp']
reviews_collection = yelp_database['reviews']
processed_collection = yelp_database['processed_reviews']


def sanitary_data():
    cur = reviews_collection.find()
    for doc in cur:
        doc['timestamp'] = parser.parse(doc['date']).timestamp()
        processed_collection.insert_one(doc, w=0)



if __name__ == '__main__':
    sanitary_data()