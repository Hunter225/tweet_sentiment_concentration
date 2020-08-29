from scripts.scrape_tweets import main as scrape_tweets
from scripts.generate_daily_suggestion import main as generate_daily_suggestion
from datetime import datetime

def execute():
    today = datetime.utcnow()
    if today.weekday() == 5 or today.weekday() == 6:
        return
    scrape_tweets()
    generate_daily_suggestion()