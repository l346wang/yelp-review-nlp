from pymongo import MongoClient

import nltk
from nltk.corpus import stopwords

from config import MONGO_DB_ADDRESS

stopWords = set(stopwords.words('english'))

client = MongoClient(MONGO_DB_ADDRESS, serverSelectionTimeoutMS=1)
yelp_database = client['yelp']

tokenized_review_collection = yelp_database['tokenized_reviews']
first_million_collection = yelp_database['first_millions']


if __name__ == '__main__':
    cur = first_million_collection.find()
    new_list = []
    for doc in cur:
        if len(new_list) >= 1000:
            tokenized_review_collection.insert_many(new_list)
            new_list.clear()
        new_obj = dict()
        new_obj['review_id'] = doc['review_id']
        new_obj['stars'] = doc['stars']
        text = doc['text']
        new_obj['tokens'] = nltk.word_tokenize(text)
        new_list.append(new_obj)

    if len(new_list) != 0:
        tokenized_review_collection.insert_many(new_list)
        new_list.clear()

