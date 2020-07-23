from elasticsearch import Elasticsearch
from elasticsearch_dsl import Document, Date, Text, Float, Integer
from elasticsearch_dsl.connections import connections

connections.create_connection(hosts=['localhost'])

class Concentration(Document):
    date = Date()
    start_time = Date()
    end_time = Date()
    concentration = Float()
    word_frequency = Text()
    day_of_week = Integer()
    class Index:
        name = 'concentration'
