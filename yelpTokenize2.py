from pymongo import MongoClient

import nltk
from nltk.corpus import stopwords

from config import MONGO_DB_ADDRESS

stopWords = set(stopwords.words('english'))

client = MongoClient(MONGO_DB_ADDRESS, serverSelectionTimeoutMS=1)
yelp_database = client['yelp']

tokenized_review_collection = yelp_database['tokenized_reviews2']
first_million_collection = yelp_database['first_millions']


def get_tokens_without_stopwords(tokens):
  new_tokens = []
  for w in tokens:
    if w not in stopWords and len(w) != 1:
      new_tokens.append(w)

  return new_tokens


if __name__ == '__main__':
  cur = first_million_collection.find()
  new_list = []
  max_length = 0
  for doc in cur:
    if len(new_list) >= 1000:
      tokenized_review_collection.insert_many(new_list)
      new_list.clear()

    new_obj = dict()
    new_obj['review_id'] = doc['review_id']
    new_obj['stars'] = doc['stars']
    text = doc['text'].lower()
    new_obj['tokens'] = nltk.word_tokenize(text)
    new_obj['tokens'] = get_tokens_without_stopwords(new_obj['tokens'])
    if len(new_obj['tokens']) == 0:
      print(doc)
      continue
    # print(new_obj['tokens'])
    max_length = max(max_length, len(new_obj['tokens']))
    new_list.append(new_obj)
  print(max_length)

  if len(new_list) != 0:
    tokenized_review_collection.insert_many(new_list)
    new_list.clear()

