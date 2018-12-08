
from pymongo import MongoClient
import pymongo

from config import MONGO_DB_ADDRESS


client = MongoClient(MONGO_DB_ADDRESS, serverSelectionTimeoutMS=1)
yelp_database = client['yelp']

words_hit_count_collection = yelp_database['words_hit_count']
tokenized_reviews_collection = yelp_database['tokenized_reviews2']

import json

MAX_SENTENCE_LENGTH = 200

vocabulary_list = words_hit_count_collection.aggregate([
  {
    '$group': {
      '_id': {
        'word': '$word',
        'index': '$index',
      },
    }
  },
  {
    '$project': {
      '_id': 0,
      'word': '$_id.word',
      'index': '$_id.index'
    }
  }
])

vocabulary_dict = dict()

for vocab in vocabulary_list:
  vocabulary_dict[vocab['word']] = vocab['index']

vocab_size = len(vocabulary_dict) + 1


tokenized_reviews_list = tokenized_reviews_collection.find()

tokens_as_index_matrix = []
star_matrix = []

for review in tokenized_reviews_list:
  index_row = []
  for word in review['tokens']:
    index_row.append(vocabulary_dict[word])
  if len(index_row) < MAX_SENTENCE_LENGTH:
    length_of_padding = MAX_SENTENCE_LENGTH - len(index_row)
    index_row.extend([0] * length_of_padding)
  else:
    index_row = index_row[:MAX_SENTENCE_LENGTH]

  tokens_as_index_matrix.append(index_row)
  minus_1_star = review['stars'] - 1
  star_matrix.append([minus_1_star])

  tokens_as_index_matrix.append(index_row)
  star_matrix.append([minus_1_star])
  tokens_as_index_matrix.append(index_row)
  star_matrix.append([minus_1_star])
  tokens_as_index_matrix.append(index_row)
  star_matrix.append([minus_1_star])
  tokens_as_index_matrix.append(index_row)
  star_matrix.append([minus_1_star])
  if 0 < minus_1_star < 4:
    tokens_as_index_matrix.append(index_row)
    tokens_as_index_matrix.append(index_row)
    star_matrix.append([minus_1_star + 1])
    star_matrix.append([minus_1_star - 1])
  elif minus_1_star == 0:
    tokens_as_index_matrix.append(index_row)
    star_matrix.append([minus_1_star + 1])
  else:
    tokens_as_index_matrix.append(index_row)
    star_matrix.append([minus_1_star - 1])

vocab_size = len(vocabulary_dict) + 1

def write_to_file(filename, data):
  with open(filename, 'w') as the_file:
    json.dump(data, the_file)

write_to_file('tokens_as_index_matrix.json', tokens_as_index_matrix)
write_to_file('star_matrix.json', star_matrix)
write_to_file('vocabulary_size.json', {
  'vocab_size': vocab_size
})