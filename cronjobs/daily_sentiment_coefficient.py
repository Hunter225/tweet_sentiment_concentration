from calculation.sentiment_concentration_coefficient import multi_thread_cal_daily_sentiment_concentration, write_result_csv
from datetime import datetime, timedelta


def run():
    daytime0 = datetime.now() - timedelta(days=1)
    project_days = 1
    num_of_thread = 1
    results = multi_thread_cal_daily_sentiment_concentration(daytime0, project_days, num_of_thread)
    write_result_csv(results)