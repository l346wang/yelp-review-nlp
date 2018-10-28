
from pymongo import MongoClient
import pymongo

from config import MONGO_DB_ADDRESS


client = MongoClient(MONGO_DB_ADDRESS, serverSelectionTimeoutMS=1)
yelp_database = client['yelp']

words_hit_count_collection = yelp_database['words_hit_count']
tokenized_review_collection = yelp_database['tokenized_reviews']

if __name__ == '__main__':
    cur = tokenized_review_collection.find()
    result = tokenized_review_collection.aggregate([
        {
            '$unwind': '$tokens'
        },
        # {
        #     '$limit': 1000,
        # },
        {
            '$project': {
                'stars': 1,
                'tokens': {
                    '$toLower': '$tokens',
                },
            }
        },
        {
            '$group': {
                '_id': {
                    'stars': '$stars',
                    'word': '$tokens'
                },
                'count': {
                    '$sum': 1
                }
            }
        },
        {
            '$project': {
                'count': 1,
                '_id': 0,
                'stars': '$_id.stars',
                'word': '$_id.word',
            }
        },
        {
            '$out': 'words_hit_count'
        },
    ])
    documents = list(result)
    # print(documents)
    # words_hit_count_collection.insert_many(documents)