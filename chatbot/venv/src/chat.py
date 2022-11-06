
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
import json
import string
import random
import numpy as np
from tensorflow import keras

nltk.download("punkt")
nltk.download("wordnet")

last_tag = ""


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
    thresh = 0.6
    y_pred = [[indx, res] for indx, res in enumerate(result) if res > thresh]
    y_pred.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in y_pred:
        return_list.append(labels[r[0]])
    return return_list


def get_response(intents_list, intents_json):
    global last_tag
    list_of_intents = intents_json["intents"]
    result = ""
    if len(intents_list) == 0:
        tag = "noanswer"
        for i in list_of_intents:
            if i["tag"] == tag:
                result = random.choice(i["responses"])
                break
    else:
        tag = intents_list[0]
        if tag == "followup":
            for i in list_of_intents:
                if i["tag"] == last_tag:
                    result = random.choice(i["responses"])
                    return result
        if tag == last_tag:
            for i in list_of_intents:
                if i["tag"] == "repeating":
                    result = random.choice(i["responses"])
                    break
        if tag not in ["noanswer", "exclaim", "greeting", "goodbye", "thanks", "haha", "niceToMeetYou", "appreciate",
                       "no", "yes", "opinion", "greetreply", "suggest"]:
            last_tag = tag
        for i in list_of_intents:
            if i["tag"] == tag:
                if result:
                    result += random.choice(i["responses"])
                else:
                    result = random.choice(i["responses"])
                break
    return result


data_file = open("intents.json").read()
data = json.loads(data_file)


words = []
classes = []

for intent in data["intents"]:
    for pattern in intent["patterns"]:
        tokens = nltk.word_tokenize(pattern)
        words.extend(tokens)
        if intent["tag"] not in classes:
            classes.append(intent["tag"])

lem = WordNetLemmatizer()

words = [lem.lemmatize(word.lower()) for word in words if word not in string.punctuation]

words = sorted(set(words))
classes = sorted(set(classes))


model = keras.models.load_model('first_model')

print("Type 0 to end the conversation")
while True:
    message = input("")
    if message == "0":
        break
    intents = pred_class(message, words, classes)
    result = get_response(intents, data)
    print(result)
