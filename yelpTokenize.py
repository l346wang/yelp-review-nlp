from pymongo import MongoClient

import nltk
from config import MONGO_DB_ADDRESS


client = MongoClient(MONGO_DB_ADDRESS, serverSelectionTimeoutMS=1)
yelp_database = client['yelp']

tokenized_review_collection = yelp_database['tokenized_reviews']
first_million_collection = yelp_database['first_millions']


if __name__ == '__main__':
    cur = first_million_collection.find()
    count = 0

    for doc in cur:
        if count % 100 == 0:
            print(count)
        count += 1
        new_obj = dict()
        new_obj['review_id'] = doc['review_id']
        new_obj['stars'] = doc['stars']
        text = doc['text']
        new_obj['tokens'] = nltk.word_tokenize(text)
        tokenized_review_collection.insert_one(new_obj, w=0)


