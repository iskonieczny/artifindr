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
import matplotlib.pyplot as plt
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

train_ds = raw_train_ds
val_ds = raw_val_ds
test_ds = raw_test_ds

train_ds = train_ds.cache().prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)
test_ds = test_ds.cache().prefetch(buffer_size=AUTOTUNE)

text_input = Input(shape=(1,), dtype='string')
x = vectorize_layer(text_input)
x = Embedding(max_features + 1, embedding_dim)(x)
x = Dropout(0.2)(x)
x = Conv1D(64, 3, padding='same')(x)
x = Conv1D(64, 4, padding='same')(x)
x = Conv1D(64, 5, padding='same')(x)
x = Flatten()(x)
x = Dropout(0.2)(x)
predictions = Dense(len(labels_set), activation="sigmoid", name="predictions")(x)

model = tf.Model(text_input, predictions)
tf.utils.plot_model(model, to_file="char_classify_model.png", show_shapes=True)

model.compile(loss=SparseCategoricalCrossentropy(from_logits=False), optimizer="adam", metrics=["accuracy"])

history = model.fit(train_ds, validation_data=val_ds, epochs=15)
model.save("char_classify_model.tf")

model.compile(
    loss=SparseCategoricalCrossentropy(from_logits=False), optimizer="adam", metrics=['accuracy']
)

y_prob = model.predict(["I am a chatbot made for Artifindr application", "I like heavy-metal, ha...ha....ha",
                               "Sadly I do not have any news to share with you",
                               "Cars are of no concern to me, I have a chauffeur."])
print(y_prob)

acc = history.history['accuracy']
loss = history.history['loss']


epochs = range(1, len(acc) + 1)

plt.plot(epochs, acc, 'b', label='Dokładność')
plt.plot(epochs, loss, 'r', label='Strata')
plt.title('Dokładność i strata epok trenowania')
plt.legend()

plt.show()

plt.savefig('model_epochs.png')