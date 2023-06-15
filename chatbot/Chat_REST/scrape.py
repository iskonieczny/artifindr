import praw
import nltk
from praw.models import MoreComments

#nltk.download('averaged_perceptron_tagger')
from operator import itemgetter
from tensorflow import keras


class RedditScrape:
    def __init__(self):
        self.message_tags = []
        self.model = keras.models.load_model('./char_classify_model.tf')
        self.reddit = praw.Reddit(
            client_id="zp91oGdOkDTZLkar0kzV4A",
            client_secret="qp0g6VFBge34T_wJZGtV7a22kqK6SQ",
            user_agent="artifindr")
        self.classes = sorted({'formal', 'old', 'regular', 'teenager', 'high_ego', 'robot'})

    def comp_tags(self, tags1, tags2):
        score = 0
        divisor = len(tags1)
        words2 = [word for word, tag in tags2]
        for word, tag in tags1:
            if word[0].lower() + word[1:] in words2 or word[0].upper() + word[1:] in words2:
                score += 1
                if 'NN' in tag:
                    score += 4
                    divisor += 4
                    self.message_tags.append(word.lower())

        return score, divisor

    def sent_similarity(self, message, title):  # 0-1
        # ("Title:", title)
        mes_tokens = nltk.word_tokenize(message)
        mes_tagged = nltk.pos_tag(mes_tokens)
        ttl_tokens = nltk.word_tokenize(title)
        ttl_tagged = nltk.pos_tag(ttl_tokens)
        score1, div1 = self.comp_tags(mes_tagged, ttl_tagged)
        score2, div2 = self.comp_tags(ttl_tagged, mes_tagged)
        score = (score1 + score2) / (div1 + div2)
        # print("Title score", score)
        return score

    def classify(self, comment, character):
        pred = self.model.predict([comment], verbose=False)
        # print("Comment:", comment)
        # for i, cl in enumerate(self.classes):
        # print(cl, ":", pred[0][i], end=", ")
        # print("\n")
        idx = self.classes.index(character)
        return pred[0][idx]

    def iter_top_level(self, comments):
        for top_level_comment in comments:
            if isinstance(top_level_comment, MoreComments):
                yield from self.iter_top_level(top_level_comment.comments())
            else:
                yield top_level_comment

    def search(self, sentence, character):
        self.message_tags = []
        search_term = 'all'
        subreddit = self.reddit.subreddit(search_term)
        resp = subreddit.search(sentence, limit=5)
        #resp = self.reddit.info(subreddits=[sub.name for sub in resp])
        fullnames = [f"t3_{id}" for id in [str(r) for r in resp]]
        scrape_data = []
        for submission in self.reddit.info(fullnames=fullnames):
            submission.comment_limit = 30
            submission.comments.replace_more(limit=None, threshold=5)
            # submission.comments.replace_more(limit=1)
            top_level_comments = []
            for com in self.iter_top_level(self.reddit.info(fullnames=[f"t1_{id}" for id in [str(r) for r in submission.comments]])):
                top_level_comments.append(com.body)
            scrape_data.append((submission.title,
                                top_level_comments))
            # submission.comments.replace_more(limit=0)

        comment_scores = []
        # print(scrape_data)
        for entry in scrape_data:
            title_score = self.sent_similarity(sentence, entry[0])
            for comment in entry[1]:
                com_score = self.classify(comment, character)
                if comment != '[deleted]' and len(comment)<100:
                    comment_scores.append((comment, title_score + com_score))

        res = max(comment_scores, key=itemgetter(1))
        print("\nBEST SCORE:", f"\"{res}\"")
        return *res, '&'.join(set(self.message_tags))


if __name__ == "__main__":
    scr = RedditScrape()
    print("INPUT: \"What do you think about america?\"")
    print("CHARACTER: \"old\"")
    scr.search("What do you think about america?", "old")
    print("CHARACTER: \"formal\"")
    scr.search("What do you think about america?", "formal")