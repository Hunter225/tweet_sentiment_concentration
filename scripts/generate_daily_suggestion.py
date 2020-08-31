from tweet.models import TweetSchema
from concentration.models import ConcentrationSchema
from suggestion.models import SuggestionSchema
from calculation.sentiment_concentration import cal_sentiment_concentration
from datetime import datetime, timedelta
import statistics
import json
from django.conf import settings

def get_latest_24h_tweets():
    dt1 = datetime.utcnow() - timedelta(days=1)
    dt2 = datetime.utcnow()
    # To align with the version verified by back test, the tweets are retreieved with the order of the twitter acconts
    # It has been tested that, the order of tweet has very small effect on the concentration result calculated
    # The effect on PnL need to be verified again before the ordering is removed
    tweets = []
    for screen_name in settings.TWITTER_ACCOUNTS:
        tweets_of_an_account= [tweet for tweet in TweetSchema.objects.filter(screen_name=screen_name, tweet_create_time__gte=dt1, tweet_create_time__lte=dt2).values_list('full_text', flat=True)]
        tweets.extend(tweets_of_an_account)
    return tweets

def main():
    dt1 = datetime.utcnow() - timedelta(days=1)
    dt2 = datetime.utcnow()
    tweets = get_latest_24h_tweets()
    today = datetime.today()
    day_of_week = today.weekday()
    trial_results = []
    word_frequency_in_tweets = None
    
    for i in range(3):
        sentiment_concentration, word_frequency_in_tweets = cal_sentiment_concentration(tweets)
        trial_results.append(sentiment_concentration)
    
    median_of_results = statistics.median(trial_results)
    
    previous_concentration_object = None
    
    concentration_data = dict(concentration_coefficient = median_of_results, calculation_date=today,
                            status='A', word_frequency = json.dumps(word_frequency_in_tweets), day_of_week=day_of_week,
                            start_time= dt1, end_time=dt2, previous_concentration =previous_concentration_object)
    
    current_concentration_object, is_created = ConcentrationSchema.objects.update_or_create(calculation_date=today, defaults=concentration_data)

    concentration_query_set = ConcentrationSchema.objects.all().order_by('calculation_date')

    if is_created:
        previous_concentration_object = concentration_query_set.last()
    else:
        previous_concentration_object = concentration_query_set[len(concentration_query_set) - 2]
        
    suggestion = 0
    if current_concentration_object.concentration_coefficient - previous_concentration_object.concentration_coefficient > 0.1:
        suggestion = 1
    elif current_concentration_object.concentration_coefficient - previous_concentration_object.concentration_coefficient < -0.1:
        suggestion = -1
    else:
        suggestion = 0

    suggestion_data = dict(suggestion=suggestion, concentration=current_concentration_object)

    SuggestionSchema.objects.update_or_create(suggestion_date=today, defaults=suggestion_data)

def run():
    main()
