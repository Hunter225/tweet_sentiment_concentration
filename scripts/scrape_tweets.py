from django.conf import settings
from tweet.models import TweetSchema
import GetOldTweets3 as got
from datetime import datetime, timedelta


def _scrape_tweets_from_user_timeline(screen_name, start_date_str, end_date_str, tweets_external_ids, max_count=40):
    new_tweets = []
    tweetCriteria = got.manager.TweetCriteria().setUsername(screen_name)\
                                            .setSince(start_date_str)\
                                            .setUntil(end_date_str)\
                                            .setMaxTweets(max_count)

    tweets = got.manager.TweetManager.getTweets(tweetCriteria)

    for tweet in tweets:
        if tweet.id not in tweets_external_ids:
            new_tweet = TweetSchema(screen_name=screen_name, 
            tweet_create_time=tweet.date.replace(tzinfo=None), tweet_external_id=tweet.id,
            full_text=tweet.text, status='A')
            new_tweets.append(new_tweet)

    return new_tweets


def _save_tweets_to_db(start_date_str, end_date_str, max_count=40):
    screen_names = settings.TWITTER_ACCOUNTS
    tweet_external_ids = TweetSchema.objects.all().values_list('tweet_external_id', flat=True)
    tweets_to_be_saved = []
    for screen_name in screen_names:
        new_tweets = _scrape_tweets_from_user_timeline(screen_name, start_date_str, end_date_str, tweet_external_ids, max_count=max_count)
        tweets_to_be_saved.extend(new_tweets)
    TweetSchema.objects.bulk_create(tweets_to_be_saved)

def main():
    start_date_str = (datetime.utcnow() - timedelta(days=1)).strftime('%Y-%m-%d')
    end_date_str = (datetime.utcnow()).strftime('%Y-%m-%d')
    _save_tweets_to_db(start_date_str, end_date_str)

def run():
    main()