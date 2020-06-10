from cronjobs import scrape_tweets
from cronjobs import daily_sentiment_coefficient

if __name__ == '__main__':
    scrape_tweets.run()
    daily_sentiment_coefficient.run()