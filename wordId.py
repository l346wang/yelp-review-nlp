
from pymongo import MongoClient
import pymongo

from config import MONGO_DB_ADDRESS


client = MongoClient(MONGO_DB_ADDRESS, serverSelectionTimeoutMS=1)
yelp_database = client['yelp']

words_hit_count_collection = yelp_database['words_hit_count']

idx = 0
for word in words_hit_count_collection.find().distinct('word'):
  words_hit_count_collection.update({
    'word': word
  }, {
    '$set': {
      'index': idx,
    },
  }, multi=True, w=0)
  idx += 1



