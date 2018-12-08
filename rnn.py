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

model = keras.Sequential()
# model.add(keras.layers.Embedding(vocab_size, 256))
# model.add(keras.layers.GlobalAveragePooling1D())
# model.add(keras.layers.Dense(256, activation=tf.nn.relu))
# model.add(keras.layers.Dense(10, activation=tf.nn.relu))
# model.add(keras.layers.Dense(NUMBER_OF_CLASS, activation=tf.nn.softmax))
model.add(keras.layers.Embedding(vocab_size, 144))
model.add(keras.layers.GlobalAveragePooling1D())
model.add(keras.layers.Dense(144, activation=tf.nn.relu))
model.add(keras.layers.Dense(10, activation=tf.nn.relu))
model.add(keras.layers.Dense(NUMBER_OF_CLASS, activation=tf.nn.softmax))

model.summary()

model.compile(optimizer=tf.train.AdamOptimizer(),
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

x_val = np_token_matrix[8000:]
y_val = np_label_matrix[8000:]

test_data = np_token_matrix[:8000]
test_labels = np_label_matrix[:8000]

history = model.fit(x_val,
                    y_val,
                    epochs=10,
                    batch_size=512,
                    validation_split=0.2,
                    verbose=1)


# model.save('original_model.h5')
model.save('my_model.h5')


results = model.evaluate(test_data, test_labels)

print(results)
predict = model.predict(test_data)


