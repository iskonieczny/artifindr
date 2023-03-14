
import nltk
# nltk.download()
from nltk.stem.wordnet import WordNetLemmatizer
import json
import string
import random
import numpy as np
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Dropout

nltk.download("punkt")
nltk.download("wordnet")


def clean_text(text):
    tokens = nltk.word_tokenize(text)
    tokens = (lem.lemmatize(word) for word in tokens)
    return tokens


def bag_of_words(text, vocab):
    tokens = clean_text(text)
    bow = [0] * len(vocab)
    for w in tokens:
        for idx, word in enumerate(vocab):
            if word == w:
                bow[idx] = 1
    return np.array(bow)


def pred_class(text, vocab, labels):
    bow = bag_of_words(text, vocab)
    result = model.predict(np.array([bow]))[0]
    thresh = 0.5
    y_pred = [[indx, res] for indx, res in enumerate(result) if res > thresh]
    y_pred.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in y_pred:
        return_list.append(labels[r[0]])
    return return_list


def get_response(intents_list, intents_json):
    if len(intents_list) == 0:
        list_of_intents = intents_json["intents"]
        tag = "noanswer"
        for i in list_of_intents:
            if i["tag"] == tag:
                # result = random.choice(i["responses"])
                result = i["tag"]
                break
    else:
        tag = intents_list[0]
        list_of_intents = intents_json["intents"]
        for i in list_of_intents:
            if i["tag"] == tag:
                # result = random.choice(i["responses"])
                result = i["tag"]
                break
    return result


data_file = open("./intents.json").read()
data = json.loads(data_file)


words = []
classes = []
data_X = []
data_Y = []

for intent in data["intents"]:
    for pattern in intent["patterns"]:
        tokens = nltk.word_tokenize(pattern)
        words.extend(tokens)
        data_X.append(pattern)
        data_Y.append(intent["tag"])

        if intent["tag"] not in classes:
            classes.append(intent["tag"])

lem = WordNetLemmatizer()

words = [lem.lemmatize(word.lower()) for word in words if word not in string.punctuation]

words = sorted(set(words))
classes = sorted(set(classes))

training = []
out_empty = [0] * len(classes)

for idx, doc in enumerate(data_X):
    bow = []
    text = lem.lemmatize(doc.lower())
    for word in words:
        bow.append(1) if word in text else bow.append(0)
    output_row = list(out_empty)
    output_row[classes.index(data_Y[idx])] = 1

    training.append([bow, output_row])

random.shuffle(training)
training = np.array(training, dtype=object)

train_X = np.array(list(training[:, 0]))
train_Y = np.array(list(training[:, 1]))

model = Sequential()
model.add(Dense(128, input_shape=(len(train_X[0]),), activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(64, activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(len(train_Y[0]), activation="softmax"))
adam = tf.keras.optimizers.Adam(learning_rate=0.007)
model.compile(loss='categorical_crossentropy',
              optimizer=adam,
              metrics=["accuracy"])

print(model.summary())

model.fit(x=train_X, y=train_Y, epochs=200, verbose=1)

model.save('chat_model')



# generowanie tekstu do tego modelu
