
from pymongo import MongoClient

import nltk
from config import MONGO_DB_ADDRESS


client = MongoClient(MONGO_DB_ADDRESS, serverSelectionTimeoutMS=1)
yelp_database = client['yelp']

words_hit_count_collection = yelp_database['words_hit_count']
tokenized_review_collection = yelp_database['tokenized_reviews']


if __name__ == '__main__':
    cur = tokenized_review_collection.find()
    count = 0

    for doc in cur:
        if count % 100 == 0:
            print(count)
        count += 1
        tokens = doc['tokens']
        stars = doc['stars']
        for word in tokens:
            upsert_data = {
                '$set': {
                    'word': word,
                    'stars': stars,
                },
                '$inc': {
                    'count': 1
                }
            }
            words_hit_count_collection.find_one_and_update(
                {
                    'word': word,
                    'stars': stars,
                }, upsert_data, upsert=True
            )


