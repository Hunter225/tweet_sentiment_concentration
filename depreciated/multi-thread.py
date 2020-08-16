from calculation.sentiment_concentration import cal_sentiment_concentration
from datetime import datetime
from datetime import timedelta
from threading import Thread

def cal_daily_sentiment_concentration(daytime0, num_of_date, thread_results, index):
    thread_result = []
    for i in range(num_of_date):
        start_time = daytime0
        end_time = daytime0 + timedelta(days=1)
        
        concentration_coefficient = cal_sentiment_concentration(tweets)
        result = dict(start_time = start_time.strftime("%Y-%m-%dT%H:%M:%S"), end_time = end_time.strftime("%Y-%m-%dT%H:%M:%S"), concentration_coefficient = concentration_coefficient)
        
        thread_result.append(result)
        thread_results[index] = thread_result

        daytime0 = daytime0 + timedelta(days=1)

def multi_thread_cal_daily_sentiment_concentration(daytime0, project_days, num_of_thread):
    days_processed_by_each_core = int(project_days / num_of_thread)
    threads = [None] * num_of_thread
    threads_results = [None] * num_of_thread
    
    for i in range(num_of_thread):
        threads[i] = Thread(target = cal_daily_sentiment_concentration, args=(daytime0, days_processed_by_each_core, threads_results, i))
        threads[i].start()
        daytime0 = daytime0 + timedelta(days=days_processed_by_each_core)

    for i in range(num_of_thread):
        threads[i].join()

    final_results = []
    for results in threads_results:
        for result in results:
            final_results.append(result)

    return final_results

def write_result_csv(results):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    with open('result/sentiment_concentration/sentiment_concentration_coefficient-%s.csv' % timestamp, 'w') as result_file:

        for result in results:
            result_file.write(result['start_time'])
            result_file.write(',')
            result_file.write(result['end_time'])
            result_file.write(',')
            result_file.write(str(result['concentration_coefficient']))
            result_file.write('\n')

if __name__ == '__main__':
    daytime0 = datetime(2019,6,8,13,30,0)
    project_days = 100
    num_of_thread = 10
    results = multi_thread_cal_daily_sentiment_concentration(daytime0, project_days, num_of_thread)
    write_result_csv(results)