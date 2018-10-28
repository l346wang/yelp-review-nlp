#!/usr/bin/python3
import json
from pymongo import MongoClient
from config import MONGO_DB_ADDRESS

client = MongoClient(MONGO_DB_ADDRESS, serverSelectionTimeoutMS=1)
yelp_database = client['yelp']
reviews_collection = yelp_database['reviews']


def process_data():
    fname = './yelp_dataset/yelp_academic_dataset_review.json'
    with open(fname) as f:
        content = f.readlines()

    for line in content:
        review_data = json.loads(line)
        reviews_collection.insert_one(review_data, w=0)


if __name__ == '__main__':
    process_data()