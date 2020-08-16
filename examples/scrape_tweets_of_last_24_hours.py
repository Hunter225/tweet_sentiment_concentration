from util import util
from scraper.tweets_scraper import TweetScraper
from models.tweet import Tweet
from elasticsearch_dsl.connections import connections
import ssl
from datetime import datetime
from datetime import timedelta
ssl._create_default_https_context = ssl._create_unverified_context



def main():
    now = datetime.utcnow()
    yesterday = now - timedelta(days=1)
    start_date_str = yesterday.strftime('%Y-%m-%d')
    end_date_str = now.strftime('%Y-%m-%d')

    tweet_accounts = util.read_tweet_accounts()

    for screen_name in tweet_accounts:

        tweets = TweetScraper.get_tweets_from_user_timeline(screen_name, start_date_str, end_date_str)
        Tweet.init()

        print("Tweet account name: %s" % str(screen_name))

        len_of_tweets = len(tweets)
        print("Total length of tweets: %s" % str(len_of_tweets))

        for tweet in tweets:
            try:
                obj = Tweet(meta={'id': tweet['id']})
                obj.screen_name = tweet['screen_name']
                obj.full_text = tweet['full_text']
                obj.created_at = tweet['created_at']
                obj.save()
            except:
                pass

if __name__ == '__main__':
    main()