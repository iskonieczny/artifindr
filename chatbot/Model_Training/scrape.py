import praw
import sys
import nltk
from praw.models import MoreComments

#nltk.download('averaged_perceptron_tagger')
from char_classify_train import *
from operator import itemgetter

reddit = praw.Reddit(
    client_id="zp91oGdOkDTZLkar0kzV4A",
    client_secret="qp0g6VFBge34T_wJZGtV7a22kqK6SQ",
    user_agent="artifindr"
)

message_tags = []

classes = sorted(labels_set)

sentence = "What do you think about america?" #NN, NNP
character = "old"


def comp_tags(tags1, tags2):
    score = 0
    divisor = len(tags1)
    words2 = [word for word, tag in tags2]
    for word, tag in tags1:
        if word[0].lower()+word[1:] in words2 or word[0].upper()+word[1:] in words2:
            score+=1
            if 'NN' in tag:
                score+=4
                divisor+=4
                message_tags.append(word.lower())

    return score, divisor


def sent_similarity(message, title):  # 0-1
    print("Title:", title)
    mes_tokens = nltk.word_tokenize(message)
    mes_tagged = nltk.pos_tag(mes_tokens)
    ttl_tokens = nltk.word_tokenize(title)
    ttl_tagged = nltk.pos_tag(ttl_tokens)
    score1, div1 = comp_tags(mes_tagged, ttl_tagged)
    score2, div2 = comp_tags(ttl_tagged, mes_tagged)
    score = (score1+score2)/(div1+div2)
    print("Title score", score)
    return score


def classify(comment):
    pred = model.predict([comment])
    print("Comment:", comment)
    for i, cl in enumerate(classes):
        print(cl, ":", pred[0][i], end=", ")
    print("\n")
    idx = classes.index(character)
    return pred[0][idx]


def iter_top_level(comments):
    for top_level_comment in comments:
        if isinstance(top_level_comment, MoreComments):
            yield from iter_top_level(top_level_comment.comments())
        else:
            yield top_level_comment



search_term='all'


keyword=sentence


subreddit = reddit.subreddit(search_term)

resp = subreddit.search(keyword,limit=5)

scrape_data = []
for submission in resp:
    submission.comment_limit = 25
    #submission.comments.replace_more(limit=1)
    top_level_comments = []
    for com in iter_top_level(submission.comments):
        top_level_comments.append(com.body)
    scrape_data.append((submission.title,
                    top_level_comments))
    #submission.comments.replace_more(limit=0)

comment_scores = []
print(scrape_data)
for entry in scrape_data:
    title_score = sent_similarity(sentence, entry[0])
    for comment in entry[1]:
        com_score = classify(comment)
        comment_scores.append((comment, title_score+com_score))
    print('&'.join(set(message_tags)))


print("\nBEST SCORE:", max(comment_scores, key=itemgetter(1)))
