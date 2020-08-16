from calculation.sentiment_concentration import cal_sentiment_concentration
from datetime import datetime
from datetime import timedelta
from threading import Thread
from models.getter import Getter
from util import preprocess, util


def main():
    start_time = datetime.utcnow() - timedelta(days=1)
    end_time = datetime.utcnow()
    tweets = util.get_tweets(start_time, end_time)
    concentration_coefficient = cal_sentiment_concentration(tweets)
    print(concentration_coefficient)