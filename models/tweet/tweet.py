from elasticsearch import Elasticsearch
from elasticsearch_dsl import Document, Date, Text, Integer
from elasticsearch_dsl.connections import connections

connections.create_connection(hosts=['localhost'])

class Tweet(Document):
    screen_name = Text()
    full_text = Text()
    created_at = Date()
    class Index:
        name = 'twitter'