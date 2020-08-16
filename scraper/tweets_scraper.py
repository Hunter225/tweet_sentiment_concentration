from util import util
import GetOldTweets3 as got
from datetime import datetime

class TweetScraper():

    @classmethod
    def get_tweets_from_user_timeline(cls, screen_name, start_date_str, end_date_str, max_count=40):

        tweetCriteria = got.manager.TweetCriteria().setUsername(screen_name)\
                                                .setSince(start_date_str)\
                                                .setUntil(end_date_str)\
                                                .setMaxTweets(max_count)

        tweets = got.manager.TweetManager.getTweets(tweetCriteria)

        extracted_tweets = []

        for tweet in tweets:
            extracted_tweet = {}
            extracted_tweet['screen_name'] = screen_name
            extracted_tweet['created_at'] = tweet.date.replace(tzinfo=None)
            extracted_tweet['id'] = tweet.id
            extracted_tweet['full_text'] = tweet.text

            extracted_tweets.append(extracted_tweet)

        return extracted_tweets