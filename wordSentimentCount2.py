
from pymongo import MongoClient
import pymongo

from config import MONGO_DB_ADDRESS


client = MongoClient(MONGO_DB_ADDRESS, serverSelectionTimeoutMS=1)
yelp_database = client['yelp']

words_hit_count_collection = yelp_database['words_hit_count2']
tokenized_review_collection = yelp_database['tokenized_reviews']


def add_word_to_dict(wc_dict, wd):
    if wd in wc_dict:
        wc_dict[wd] += 1
    else:
        wc_dict[wd] = 1


if __name__ == '__main__':
    cur = tokenized_review_collection.find()

    star_word_count_dict = dict()
    star_word_count_dict[1] = dict()
    star_word_count_dict[2] = dict()
    star_word_count_dict[3] = dict()
    star_word_count_dict[4] = dict()
    star_word_count_dict[5] = dict()

    for doc in cur:
        tokens = doc['tokens']
        stars = doc['stars']
        for word in tokens:
            word = word.lower()
            add_word_to_dict(star_word_count_dict[stars], word)

    request_list = []
    for star in star_word_count_dict:
        for word in star_word_count_dict[star]:
            request_list.append({
                'word': word,
                'stars': star,
                'count':  star_word_count_dict[star][word]
            })
    words_hit_count_collection.insert_many(request_list)