import json
from concentration.models import ConcentrationSchema
from tweet.models import TweetSchema
from suggestion.models import SuggestionSchema
from datetime import datetime

def _str_to_dt(datetime_string):
    return datetime.strptime(datetime_string, '%Y-%m-%dT%H:%M:%S')

def _str_with_ms_to_dt(datetime_string):
    return datetime.strptime(datetime_string, '%Y-%m-%dT%H:%M:%S.%f')

def _is_new_tweet(tweet, tweet_external_ids):
    if tweet.get('_id') not in tweet_external_ids:
        return True
    return False

def save_new_tweets_to_mysql(tweets):
    tweets_objects = []
    for tweet in tweets:
        tweet_external_id = tweet.get('_id')
        screen_name = tweet.get('_source').get('screen_name')
        full_text = tweet.get('_source').get('full_text')
        tweet_create_time = _str_to_dt(tweet.get('_source').get('created_at'))
        tweet_obj = TweetSchema(tweet_external_id=tweet_external_id, status='A', screen_name=screen_name, full_text=full_text, tweet_create_time=tweet_create_time)
        tweets_objects.append(tweet_obj)
    TweetSchema.objects.bulk_create(tweets_objects)

def save_concentration_to_mysql(concentration):
    calculation_date = _str_to_dt(concentration.get('_source').get('date'))
    start_time = _str_with_ms_to_dt(concentration.get('_source').get('start_time'))
    end_time = _str_with_ms_to_dt(concentration.get('_source').get('end_time'))
    concentration_coefficient = concentration.get('_source').get('concentration_coefficient')
    word_frequency = concentration.get('_source').get('word_frequency')
    day_of_week = concentration.get('_source').get('day_of_week')
    concentration_data = dict(start_time=start_time, end_time=end_time, concentration_coefficient=concentration_coefficient, word_frequency=word_frequency, day_of_week=day_of_week)
    ConcentrationSchema.objects.update_or_create(calculation_date = calculation_date, defaults=concentration_data)

def link_concentration_to_previous_concentration():
    concentrations = ConcentrationSchema.objects.all().order_by('calculation_date')
    previous_concentration = None
    for concentration in concentrations:
        if previous_concentration is None:
            previous_concentration = concentration
            continue
        concentration.previous_concentration = previous_concentration
        concentration.save()
        previous_concentration = concentration

def save_suggestion_to_mysql(suggestion):
    suggestion_date = _str_to_dt(suggestion.get('_source').get('date'))
    suggestion = suggestion.get('_source').get('suggestion')
    concentration = ConcentrationSchema.objects.get(calculation_date = suggestion_date)
    suggestion_data = dict(suggestion_date=suggestion_date, suggestion=suggestion, concentration=concentration)
    SuggestionSchema.objects.update_or_create(suggestion_date=suggestion_date, defaults=suggestion_data)

def run():
    with open('es_to_mysql_json/es_to_mysql_migration.json', 'r') as json_file:
        documents = json_file.readlines()
        tweet_external_ids = TweetSchema.objects.all().values_list('tweet_external_id', flat=True)
        new_tweets = []
        for document in documents:
            document_json = json.loads(document)
            if document_json.get('_index') == 'twitter':
                tweet = document_json
                if _is_new_tweet(tweet, tweet_external_ids):
                    new_tweets.append(tweet)
            elif document_json.get('_index') == 'concentration':
                save_concentration_to_mysql(document_json)
            elif document_json.get('_index') == 'suggestion':
                save_suggestion_to_mysql(document_json)

    save_new_tweets_to_mysql(new_tweets)
    link_concentration_to_previous_concentration()