from elasticsearch import Elasticsearch
from elasticsearch_dsl import Document, Date, Text, Float

class Concentration(Document):
    start_time = Date()
    end_time = Date()
    concentration = Float()
    word_frequency = Text()
    class Index:
        name = 'conentration'
