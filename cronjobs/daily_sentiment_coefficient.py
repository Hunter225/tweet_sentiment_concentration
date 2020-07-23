from calculation.sentiment_concentration_coefficient import multi_thread_cal_daily_sentiment_concentration, write_result_csv
from datetime import datetime, timedelta
from models.concentration.concentration import Concentration
from elasticsearch_dsl.connections import connections
import statistics

def run():
    daytime0 = datetime.utcnow() - timedelta(days=1)
    daytime1 = daytime0 + timedelta(days=1)
    project_days = 1
    num_of_thread = 1
    runtimes = 1
    trials = []
    while runtimes <= 3:
        results = multi_thread_cal_daily_sentiment_concentration(daytime0, project_days, num_of_thread)
        trials.append(results)
        runtimes = runtimes + 1
    
    Concentration.init()
    start_time = trials[0][0]['start_time']
    end_time = trials[0][0]['end_time']
    word_frequency = trials[0][0]['word_frequency']
    concentrations = []
    for trial in trials:
        concentrations.append(trial[0]['concentration_coefficient'])
    concentration_median = statistics.median(concentrations)

    obj = Concentration(meta={'id': daytime1.strftime("%Y-%m-%d")})
    obj.date = daytime1.strftime("%Y-%m-%d")
    obj.start_time = start_time
    obj.end_time = end_time
    obj.concentration_coefficient = concentration_median
    obj.word_frequency = word_frequency
    obj.day_of_week = daytime1.weekday()
    obj.save()