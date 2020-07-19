from calculation.sentiment_concentration_coefficient import multi_thread_cal_daily_sentiment_concentration, write_result_csv
from datetime import datetime, timedelta
from models.concentration.concentration import Concentration
from elasticsearch_dsl.connections import connections

def run():
    daytime0 = datetime.now() - timedelta(days=1)
    project_days = 1
    num_of_thread = 1
    results = multi_thread_cal_daily_sentiment_concentration(daytime0, project_days, num_of_thread)
    connections.create_connection(hosts=['localhost'])
    Concentration.init()
    for result in results:
        obj = Concentration(meta={'id': datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")})
        obj.start_time = result['start_time']
        obj.end_time = result['end_time']
        obj.concentration_coefficient = result['concentration_coefficient']
        obj.word_frequency = result['word_frequency']
        obj.save()
        print(obj)