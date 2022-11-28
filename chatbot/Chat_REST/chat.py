
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
import json
import string
import random
import numpy as np
from tensorflow import keras

nltk.download("punkt")
nltk.download("wordnet")

import os

print(os.path)


def ask_a_question():
    result = random.randint(0, 100)
    if result > 80:
        return True
    return False


class Chat:
    def __init__(self):

        self.lem = WordNetLemmatizer()

        self.words = []

        self.classes = []

        data_file = open("intents.json").read()
        data = json.loads(data_file)

        for intent in data["intents"]:
            for pattern in intent["patterns"]:
                tokens = nltk.word_tokenize(pattern)
                self.words.extend(tokens)
                if intent["tag"] not in self.classes:
                    self.classes.append(intent["tag"])

        self.words = [self.lem.lemmatize(word.lower()) for word in self.words if word not in string.punctuation]

        self.words = sorted(set(self.words))

        self.classes = sorted(set(self.classes))

        self.model = keras.models.load_model("chat_model")





    def clean_text(self, text):
        tokens = nltk.word_tokenize(text)
        tokens = (self.lem.lemmatize(word) for word in tokens)
        return tokens

    def bag_of_words(self, text, vocab):
        tokens = self.clean_text(text)
        bow = [0] * len(vocab)
        for w in tokens:
            for idx, word in enumerate(vocab):
                if word == w:
                    bow[idx] = 1
        return np.array(bow)

    def pred_class(self, text, vocab, labels):
        bow = self.bag_of_words(text, vocab)
        result = self.model.predict(np.array([bow]))[0]
        thresh = 0.6
        y_pred = [[indx, res] for indx, res in enumerate(result) if res > thresh]
        y_pred.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        for r in y_pred:
            return_list.append(labels[r[0]])
        return return_list

    def get_response(self, intents_list, intents_json, last_tag):
        list_of_intents = intents_json["intents"]
        question = ask_a_question()
        result = ""
        tag_to_return = last_tag
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
                        break
            if tag == last_tag:
                for i in list_of_intents:
                    if i["tag"] == "repeating":
                        result = random.choice(i["responses"])
                        break
            if tag not in ["noanswer", "exclaim", "greeting", "goodbye", "thanks", "haha", "niceToMeetYou", "appreciate",
                           "no", "yes", "opinion", "greetreply", "suggest", "followup"]:
                tag_to_return = tag
            for i in list_of_intents:
                if i["tag"] == tag:
                    if result:
                        result += " " + random.choice(i["responses"])
                    else:
                        result = random.choice(i["responses"])
                    break
        if question:
            for i in list_of_intents:
                if i["tag"] == "question":
                    result += " |" + random.choice(i["responses"])
        return {
            "response": result,
            "tag_used": tag_to_return
        }

    def response_to_api(self, character_type, last_tag, message):
        file_with_responses = open(f'characters/{character_type}.json').read()
        data = json.loads(file_with_responses)
        intents = self.pred_class(message.lower(), self.words, self.classes)
        result = self.get_response(intents, data, last_tag)
        return result
