from elasticsearch import Elasticsearch
from elasticsearch_dsl import Q, Search, MultiSearch
from util import util
from datetime import datetime

class Getter():

    def __init__(self):
        self.client = Elasticsearch()

    def get_by_time_range(self, start_time, end_time):

        # reformat start_time and end_time
        if isinstance(start_time, datetime):
            start_time = start_time.strftime("%Y-%m-%dT%H:%M:%S")
        if isinstance(end_time, datetime):
            end_time = end_time.strftime("%Y-%m-%dT%H:%M:%S")

        tweets = []
        time_query = Q('range', created_at={
            'gte': start_time,
            'lte': end_time
        })
        tweet_accounts = util.read_tweet_accounts()

        for tweet_account in tweet_accounts:

            screen_query = Q('match', screen_name=tweet_account)
            search = Search(using=self.client, index="twitter").extra(from_=0, size=10000).sort('created_at')
            search.query = Q('bool', must=[time_query, screen_query])
            responses = search.execute()
            tweets = tweets + [response for response in responses]
        
        return tweets