from elasticsearch import Elasticsearch
from elasticsearch_dsl import Document, Date, Text, Float, Integer
from elasticsearch_dsl.connections import connections

connections.create_connection(hosts=['localhost'])

class Suggestion(Document):
    date = Date()
    previous_concentraion = Float()
    current_concentraion = Float()
    suggestion = Integer()

    class Index:
        name = 'suggestion'