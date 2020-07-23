from datetime import datetime, timedelta
from models.suggestion.suggestion import Suggestion
from models.concentration.concentration import Concentration

def _find_last_trade_day(today):
    today_day_of_week = today.weekday()
    if today_day_of_week == 0:
        last_trade_day = today - timedelta(days=3)
    else:
        last_trade_day = today - timedelta(days=1)
    return last_trade_day

def run():
    Suggestion.init()
    today = datetime.utcnow()
    if today.weekday() == 5 or today.weekday() == 6:
        return
    last_trade_day = _find_last_trade_day(today)
    today_concentration_id = today.strftime("%Y-%m-%d")
    last_trade_day_concentration_id = last_trade_day.strftime("%Y-%m-%d")
    today_concentration = Concentration.get(id = today_concentration_id).concentration_coefficient
    last_concentration = Concentration.get(id = last_trade_day_concentration_id).concentration_coefficient

    if today_concentration - last_concentration >= 0.1:
        suggestion = 1
    elif today_concentration - last_concentration <= -0.1:
        suggestion = -1
    else:
        suggestion = 0

    obj = Suggestion(meta={'id': today.strftime("%Y-%m-%d")})
    obj.date = today.strftime("%Y-%m-%d")
    obj.current_concentraion = today_concentration
    obj.previous_concentraion = last_concentration
    obj.suggestion = suggestion
    obj.save()

    return