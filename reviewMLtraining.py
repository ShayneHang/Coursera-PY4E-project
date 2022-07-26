import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import sqlite3
import numpy as np

# extracting the data for training
conn = sqlite3.connect(r'D:\User\Courses\PY4E coursera\project\data for training\Sushi_Express_Somerset.sqlite')
cur = conn.cursor()
cur.execute('''
SELECT users_review, users_rating FROM GoogleMapReviews WHERE users_rating IN ('5', '1') AND (users_review != 'None')
''')
dbreviews = cur.fetchall()
for i in dbreviews:
    x = i[1]
    print(x)
numofreview = len(dbreviews)

# removing the tuples from the db reviews and inserting into list
userreview = []
userrating = []
for i in range(0, numofreview):
    x = dbreviews[i]
    reviews = x[0]
    ratings = x[1]
    userreview.append(reviews)
    userrating.append(ratings)
print(userreview)
print(userrating)

len(userreview) #193 80:20 for train test 80% = 154 - after removing none only have 379 ppl gave review
len(userrating)

### tokenizing the words ###

# splitting data into training and testing
training_review = userreview[:154]
testing_review = userreview[154:]
training_rating = userrating[:154]
testing_rating = userrating[154:]

tokenizer = Tokenizer(num_words = 200, oov_token = '<OOV>')
tokenizer.fit_on_texts(training_review)
word_index = tokenizer.word_index

training_sequences = tokenizer.texts_to_sequences(training_review)
training_padded = pad_sequences(training_sequences, padding='post')

print(word_index)

for i in training_sequences:
    x = len(i)
    y = y+x
print(y) #total word count in the training sequence


for i in training_padded:
    print(i)


print(training_padded.shape) # (303, 168) 684 reviews, with max len of 168 words in the review

testing_sequences = tokenizer.texts_to_sequences(testing_review)
testing_padded = pad_sequences(testing_sequences, padding='post')


training_padded = np.array(training_padded)
testing_padded = np.array(testing_padded)
training_rating = np.array(training_rating)
testing_rating = np.array(testing_rating)

# model = tf.keras.Sequential([
#     tf.keras.layers.Embedding(999, 32), # first input layer
#     tf.keras.layers.GlobalAveragePooling1D(), # hidden layers
#     tf.keras.layers.Dense(24, activation='relu'), # # hidden layers, how many neurons in the layer, and relu is the most default activation function. then change this activation function to adjust the results
#     tf.keras.layers.Dense(1, activation='sigmoid') # the last layer - how many levels of classification we want, use 'softmax' for probability distribution
#
# ])

model = tf.keras.Sequential([
    tf.keras.layers.Embedding(999, 32),
    tf.keras.layers.GlobalAveragePooling1D(),
    tf.keras.layers.Dense(30, activation='relu'),
    tf.keras.layers.Dense(30, activation='relu'),
    tf.keras.layers.Dense(10, activation='softmax')])

# first input layer
# hidden layers, how many neurons in the layer, and relu is the most default activation function. then change this activation function to adjust the results
# the last layer - how many levels of classification we want, use 'softmax' for probability distribution


model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

# loss it the degree of error, neural network actually does not optimise accuracy, its always trying to minimise loss, hence the way we calculate loss is important. binary_crossentropy is more for 2 item classification - e.g. cats vs dogs
# adam optimizer is also the defauly method

model.summary()

model.fit(training_padded,
          training_rating,
          epochs=30,
          validation_data=(testing_padded, testing_rating),
          verbose=2)

# Epoch is just a "full pass" through your entire training dataset. So if you just train on 1 epoch, then the neural network saw each unique sample once. 3 epochs means it passed over your data set 3 times.

### testing the model ###
testreview = ['bad'] #need to bracket it even if one statement only

testsequence = tokenizer.texts_to_sequences(testreview)
testpadded = pad_sequences(testsequence, padding='post')
print(model.predict(testpadded))

# merge all the sql file into 1
# change rating of 5 to 1, rating of 1 to 0
# use only rating 5 & 1 for training
# maybe not there is not enough data.


# testreview = ['Love the service and food']
# testsequence = tokenizer.texts_to_sequences(testreview)
# testpadded = pad_sequences(testsequence, padding='post')
# print(model.predict(testpadded))
# 1/1 [==============================] - 0s 33ms/step
# [[0.99912137]]
# testreview = ['hate the service and food'] #need to bracket it even if one statement only
# testsequence = tokenizer.texts_to_sequences(testreview)
# ... testpadded = pad_sequences(testsequence, padding='post')
# ... print(model.predict(testpadded))
# ...
# 1/1 [==============================] - 0s 12ms/step
# [[0.9993269]]
# testreview = ['hate'] #need to bracket it even if one statement only
# testsequence = tokenizer.texts_to_sequences(testreview)
# testpadded = pad_sequences(testsequence, padding='post')
# print(model.predict(testpadded))
# 1/1 [==============================] - 0s 12ms/step
# [[0.9995841]]
# testreview = ['dislike'] #need to bracket it even if one statement only
# testsequence = tokenizer.texts_to_sequences(testreview)
# testpadded = pad_sequences(testsequence, padding='post')
# print(model.predict(testpadded))
# 1/1 [==============================] - 0s 11ms/step
# [[0.9995841]]
# testreview = ['bad'] #need to bracket it even if one statement only
# testsequence = tokenizer.texts_to_sequences(testreview)
# testpadded = pad_sequences(testsequence, padding='post')
# print(model.predict(testpadded))
# 1/1 [==============================] - 0s 12ms/step
# [[0.99709255]]