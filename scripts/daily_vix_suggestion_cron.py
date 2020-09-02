from scripts.scrape_tweets import main as scrape_tweets
from scripts.generate_daily_suggestion import main as generate_daily_suggestion
from datetime import datetime

def run():
    today = datetime.utcnow()
    if today.weekday() == 5 or today.weekday() == 6:
        return
    print('VIX suggestion cronjob started...')
    scrape_tweets()
    print('Calculating suggestion...')
    generate_daily_suggestion()