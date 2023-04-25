from parrot import Parrot
import torch
import os
import warnings
import itertools
import json
warnings.filterwarnings("ignore")

parrot = Parrot(model_tag="prithivida/parrot_paraphraser_on_T5")


def paraphrase(input_list):
    print(input_list)
    out_list = []
    for phrase in input_list:
        print("-" * 100)
        print("Input_phrase: ", phrase)
        print("-" * 100)
        sentences = phrase.split(". ")
        split_paraphrases = []
        for sent in sentences:
            para_phrases = parrot.augment(input_phrase=sent, use_gpu=True, do_diverse=False)
            if para_phrases:
                split_paraphrases.append([x[0][0].upper()+x[0][1:] if sent[0].isupper() else x[0] for x in para_phrases])
            else:
                split_paraphrases.append([sent])
        if split_paraphrases:
            combinations = list(itertools.product(*split_paraphrases))
            for para_phrase in combinations:
                print('. '.join(para_phrase))

                out_list.append('. '.join(para_phrase))
    return out_list


for filename in os.listdir("characters"):
    responses = open(f'characters/{filename}').read()
    data = json.loads(responses)

    for key in ['responses', 'patterns']:
        for intent in data['intents']:
            paraphrased_list = paraphrase(intent[key])
            if paraphrased_list:
                intent[key] += paraphrased_list

    with open(f'para_{filename}', 'w') as out_file:
        json.dump(data, out_file)

