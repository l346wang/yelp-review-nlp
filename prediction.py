from keras.models import load_model

model = load_model('my_model.h5')
original_model = load_model('original_model.h5')


import json

with open('./star_matrix.json') as f:
  star_matrix = json.load(f)

with open('./tokens_as_index_matrix.json') as f:
  tokens_as_index_matrix = json.load(f)

with open('./vocabulary_size.json') as f:
  vocabulary_size_file = json.load(f)
vocab_size = vocabulary_size_file['vocab_size']

NUMBER_OF_CLASS = 5

import tensorflow as tf
from tensorflow import keras
import numpy as np



np_token_matrix = np.asarray(tokens_as_index_matrix, dtype=np.int)
np_label_matrix = np.asarray(star_matrix, dtype=np.int)

test_data = np_token_matrix[:8000]
test_labels = np_label_matrix[:8000]

prediction = model.predict(test_data)
original_model_prediction = original_model.predict(test_data)

def find_max(row):
  idx = 0
  ma = -1
  for ii in list(range(len(row))):
    if row[ii] > ma:
      ma = row[ii]
      idx = ii
  return idx, ma


count = 0
close_count = 0
error_count = 0

for ii in range(len(prediction)):
  idx, ma = find_max(prediction[ii])
  ori_idx, ori_ma = find_max(original_model_prediction[ii])
  correct_idx = test_labels[ii]
  if ori_idx != correct_idx and idx == correct_idx:
    count += 1
    if -1 <= ori_idx - idx <= 1:
      close_count += 1
    # print(ori_idx)
    # print(idx)
    # print(test_labels[ii])
    # print()
  if idx != correct_idx and ori_idx == correct_idx:
    error_count += 1

print(count)
print(close_count)
print(error_count)


