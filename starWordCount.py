
from pymongo import MongoClient
import pprint

from config import MONGO_DB_ADDRESS


client = MongoClient(MONGO_DB_ADDRESS, serverSelectionTimeoutMS=1)
yelp_database = client['yelp']

star_word_count_collection = yelp_database['star_word_count']
tokenized_review_collection = yelp_database['tokenized_reviews']


def count_word_of_each_star():
    star_statistic_list = tokenized_review_collection.aggregate(
        [
            {
                '$group':
                    {
                        '_id': "$stars",
                        'total_words': {
                            '$sum': {
                                '$size': '$tokens',
                            }
                        },
                        'total_reviews': {
                            '$sum': 1,
                        },
                    },
            },
        ]
    )
    star_statistic_list = list(star_statistic_list)
    pprint.pprint(star_statistic_list)


if __name__ == '__main__':
    count_word_of_each_star()
