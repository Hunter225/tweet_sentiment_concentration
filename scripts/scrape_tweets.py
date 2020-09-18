from django.conf import settings
from tweet.models import TweetSchema
from datetime import datetime, timedelta
import tweepy
import math

def _scrape_tweets_from_user_timeline(api_client, screen_name, start_date, end_date, tweets_external_ids):
    tweets = []
    new_tweets = []

    for i in range(2):
        page = i + 1
        tweets_recieved = api_client.user_timeline(screen_name=screen_name, page=page, tweet_mode="extended", count=20)
        for tweet in tweets_recieved:
            if tweet.created_at >= start_date and tweet.created_at <=end_date:
                tweets.append(tweet)
    for tweet in tweets:
        if tweet.id_str not in tweets_external_ids:
            new_tweet = TweetSchema(screen_name=screen_name, 
            tweet_create_time=tweet.created_at, tweet_external_id=tweet.id_str,
            full_text=tweet.full_text, status='A')
            new_tweets.append(new_tweet)

    return new_tweets


def _save_tweets_to_db(api_client, start_date, end_date):
    screen_names = settings.TWITTER_ACCOUNTS
    tweet_external_ids = TweetSchema.objects.all().values_list('tweet_external_id', flat=True)
    tweets_to_be_saved = []
    for screen_name in screen_names:
        print(screen_name)
        new_tweets = _scrape_tweets_from_user_timeline(api_client, screen_name, start_date, end_date, tweet_external_ids)
        tweets_to_be_saved.extend(new_tweets)
    TweetSchema.objects.bulk_create(tweets_to_be_saved)

def _init_api_client():
    consumer_key = settings.CONSUMER_KEY
    consumer_secret = settings.CONSUMER_SECRET
    access_token = settings.ACCESS_TOKEN
    access_token_secret = settings.ACCESS_TOKEN_SECRET

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api_client = tweepy.API(auth)
    return api_client

def main():
    api_client = _init_api_client()
    start_date = datetime.utcnow() - timedelta(days=1)
    end_date = datetime.utcnow()
    _save_tweets_to_db(api_client, start_date, end_date)

def run():
    main()