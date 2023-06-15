from keras.utils import text_dataset_from_directory
from sklearn.model_selection import train_test_split
from keras.layers import TextVectorization, GlobalAveragePooling1D, Activation
from keras.layers import Embedding, Input, Dropout, Conv1D, Dense, Flatten
from keras import Sequential
from tensorflow.python.data.experimental import cardinality
from tensorflow.python.data import AUTOTUNE
from tensorflow import expand_dims
from nltk.stem.wordnet import WordNetLemmatizer
import keras as tf
from keras.losses import SparseCategoricalCrossentropy
import os
import json
import string
import nltk


max_features = 20000
embedding_dim = 128
sequence_length = 500
data = []
labels = []

lem = WordNetLemmatizer()






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
print(labels_set)
#X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.20, random_state=42)
#print(len(X_train), len(X_test))

raw_train_ds = text_dataset_from_directory(
    "character_dataset",
    batch_size=12,
    validation_split=0.2,
    subset="training",
    seed=1337,
)

raw_val_ds = text_dataset_from_directory(
    "character_dataset",
    batch_size=12,
    validation_split=0.2,
    subset="validation",
    seed=1337,
)

val_batches = cardinality(raw_val_ds)
raw_test_ds = raw_val_ds.take((2*val_batches) // 3)
raw_val_ds = raw_val_ds.skip((2*val_batches) // 3)

vectorize_layer = TextVectorization(
    max_tokens=max_features,
    output_mode="int",
    output_sequence_length=sequence_length,
)


text_ds = raw_train_ds.map(lambda x, y: x)
vectorize_layer.adapt(text_ds)

def vectorize_text(text, label):
  text = expand_dims(text, -1)
  return vectorize_layer(text), label

train_ds = raw_train_ds.map(vectorize_text)
val_ds = raw_val_ds.map(vectorize_text)
test_ds = raw_test_ds.map(vectorize_text)


train_ds = train_ds.cache().prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)
test_ds = test_ds.cache().prefetch(buffer_size=AUTOTUNE)

"""text_input = Input(shape=(1,), dtype='string')
x = vectorize_layer(text_input)
x = Embedding(max_features + 1, embedding_dim)(x)
x = Dropout(0.5)(x)

x = Conv1D(64, 3, padding='same')(x)
x = Conv1D(64, 4, padding='same')(x)
x = Conv1D(64, 5, padding='same')(x)
#x = GlobalMaxPooling2D()(x)


# We add a vanilla hidden layer:
x = Flatten()(x)
x = Dropout(0.5)(x)


# We project onto a single unit output layer, and squash it with a sigmoid:

predictions = Dense(len(labels_set), activation="softmax", name="predictions")(x)

model = tf.Model(text_input, predictions)"""
model = Sequential([
  Embedding(max_features + 1, embedding_dim),
  Dropout(0.2),
GlobalAveragePooling1D(),
Dropout(0.2),
  Dense(6)])


# Compile the model with binary crossentropy loss and an adam optimizer.
model.compile(loss=SparseCategoricalCrossentropy(from_logits=False), optimizer="adam", metrics=["accuracy"])

model.fit(train_ds, validation_data=val_ds, epochs=10)
model.save("char_classify_model.tf")

#y_prob = model.predict(["I am a chatbot made for Artifindr application"])
#print(y_prob)

export_model = Sequential([
  vectorize_layer,
  model,
  Activation('sigmoid')
])

export_model.compile(
    loss=SparseCategoricalCrossentropy(from_logits=False), optimizer="adam", metrics=['accuracy']
)

y_prob = export_model.predict(["I am a chatbot made for Artifindr application", "I like heavy-metal, ha...ha....ha",
                               "Sadly I do not have any news to share with you",
                               "Cars are of no concern to me, I have a chauffeur."])
print(y_prob)