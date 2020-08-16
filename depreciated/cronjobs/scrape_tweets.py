from util import util
from scraper.tweets_scraper import TweetScraper
from models.tweet import Tweet
import ssl
from datetime import datetime
from datetime import timedelta
ssl._create_default_https_context = ssl._create_unverified_context

def _add_one_day_to_date_string(date_str):
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    date_obj = date_obj + timedelta(days = 1)
    date_str = date_obj.strftime('%Y-%m-%d')
    return date_str


def _scrape_tweets(start_date_str, num_of_date_project, max_count_per_day):
    tweet_accounts = util.read_tweet_accounts()

    for i in range(num_of_date_project):
        print(datetime.now())
        end_date_str = _add_one_day_to_date_string(start_date_str)
        print(start_date_str)
        
        for screen_name in tweet_accounts:

            #print(screen_name)
            tweets = TweetScraper.get_tweets_from_user_timeline(screen_name, start_date_str, end_date_str, max_count_per_day)

            Tweet.init()
            
            len_of_tweets = len(tweets)
            print("Total length of tweets: %s" % str(len_of_tweets))

            no_of_tweets_saved = 1
            for tweet in tweets:
                try:
                    if no_of_tweets_saved % 1000 == 0:
                        print("%s tweets have been saved to database." % str(no_of_tweets_saved))
                    obj = Tweet(meta={'id': tweet['id']})
                    obj.screen_name = tweet['screen_name']
                    obj.full_text = tweet['full_text']
                    obj.created_at = tweet['created_at']
                    obj.save()
                    no_of_tweets_saved = no_of_tweets_saved + 1
                except:
                    no_of_tweets_saved = no_of_tweets_saved + 1
                    pass

        start_date_str = _add_one_day_to_date_string(start_date_str)

def run():
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    _scrape_tweets(yesterday, 1, 40)