from elasticsearch import Elasticsearch
from elasticsearch_dsl import Document, Date, Text, Integer

class Tweet(Document):
    screen_name = Text()
    full_text = Text()
    created_at = Date()
    class Index:
        name = 'twitter'