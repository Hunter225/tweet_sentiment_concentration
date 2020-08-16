from models.getter import Getter
from util import preprocess
from datetime import datetime

def read_tweet_accounts():
    tweet_accounts = []
    with open('settings/twitter_accounts.txt') as tweet_accounts_file:
        tweet_accounts = tweet_accounts_file.read().split('\n')
    return tweet_accounts


def is_en_word_in_string(word, string):
    if ' ' + word + ' ' in string:
        return True
    return False


def count_en_word_in_string(word, string):
    space_b4 = string.count(' ' + word)
    space_after = string.count(word + ' ')
    space_b4_and_after = string.count(' ' + word + ' ')

    return space_b4 + space_after - space_b4_and_after


def get_tweets(start_time, end_time):
    # reformat start_time and end_time
    if isinstance(start_time, datetime):
        start_time = start_time.strftime("%Y-%m-%dT%H:%M:%S")
    if isinstance(end_time, datetime):
        end_time = end_time.strftime("%Y-%m-%dT%H:%M:%S")

    # get tweets within the time range
    getter = Getter()
    tweets = getter.get_by_time_range(start_time, end_time)
    tweets = [preprocess.prepro_for_en(tweet.full_text) for tweet in tweets]
    return tweets