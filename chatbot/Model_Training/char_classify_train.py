from keras.utils import text_dataset_from_directory
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers.core import Activation, Dropout, Dense
from tensorflow.python.keras.layers import Flatten, LSTM
from tensorflow.python.keras.layers import GlobalMaxPooling1D
from tensorflow.python.keras.models import Model
from tensorflow.python.keras.layers.embeddings import Embedding
from sklearn.model_selection import train_test_split
from tensorflow.python.keras.layers import Input
from tensorflow.python.keras.layers.merge import Concatenate
from keras.layers import TextVectorization, Embedding, Input, Dropout, Conv2D, GlobalMaxPooling2D, Dense, Flatten
from tensorflow.python.data import Dataset
from tensorflow.python.data.experimental import cardinality
from nltk.stem.wordnet import WordNetLemmatizer
import tensorflow.python as tf
from tensorflow.python.keras.losses import SparseCategoricalCrossentropy
from keras.models import save_model
from tensorflow.python import layers
import os
import json
import string
import nltk
import numpy as np


max_features = 20000
embedding_dim = 128
sequence_length = 500
data = []
labels = []

lem = WordNetLemmatizer()

def vectorize_str(text):
    tokens = nltk.word_tokenize(text)
    lemmatized = [lem.lemmatize(token.lower() if token not in string.punctuation else token) for token in tokens]




for filename in os.listdir("characters"):
    responses = open(f'characters/{filename}').read()
    json_data = json.loads(responses)
    try:
        os.mkdir(f'character_dataset/{filename[:-5]}')
    except:
        pass
    for i, intent in enumerate(json_data['intents']):
        for sentence in intent['responses']:
            file = open(f'character_dataset/{filename[:-5]}/{i}.txt', 'w+')
            labels.append(filename[:-5])
            data.append(sentence)
            file.write(f"{sentence}\n")
            file.close()


labels_set = set(labels)
X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.20, random_state=42)

train_ds = text_dataset_from_directory(
    "character_dataset",
    batch_size=32,
    validation_split=0.2,
    subset="training",
    seed=1337,
)

val_ds = text_dataset_from_directory(
    "character_dataset",
    batch_size=32,
    validation_split=0.2,
    subset="validation",
    seed=1337,
)

val_batches = cardinality(val_ds)
test_ds = val_ds.take((2*val_batches) // 3)
val_ds = val_ds.skip((2*val_batches) // 3)

vectorize_layer = TextVectorization(
    max_tokens=max_features,
    output_mode="int",
    output_sequence_length=sequence_length,
)

text_ds = train_ds.map(lambda x, y: x)
vectorize_layer.adapt(text_ds)

text_input = Input(shape=(1,), dtype='string')
x = vectorize_layer(text_input)
x = Embedding(max_features + 1, embedding_dim)(x)
x = Dropout(0.5)(x)

"""x = Conv2D(128, 7, padding="valid", activation="relu", strides=3)(x)
x = Conv2D(128, 7, padding="valid", activation="relu", strides=3)(x)
x = GlobalMaxPooling2D()(x)

# We add a vanilla hidden layer:
x = Dense(128, activation="relu")(x)
x = Dropout(0.5)(x)"""

# We project onto a single unit output layer, and squash it with a sigmoid:
x = Flatten()(x)
predictions = Dense(len(labels_set), activation="softmax", name="predictions")(x)

model = tf.keras.Model(text_input, predictions)

# Compile the model with binary crossentropy loss and an adam optimizer.
model.compile(loss=SparseCategoricalCrossentropy(from_logits=False), optimizer="adam", metrics=["accuracy"])

model.fit(train_ds, validation_data=val_ds, epochs=3, verbose=False)

y_prob = model.predict(["I like america"])