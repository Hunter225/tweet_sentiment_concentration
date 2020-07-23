from cronjobs import scrape_tweets
from cronjobs import daily_sentiment_coefficient
from cronjobs import generate_suggestion

def main():
    scrape_tweets.run()
    daily_sentiment_coefficient.run()
    generate_suggestion.run()

if __name__ == '__main__':
    main()