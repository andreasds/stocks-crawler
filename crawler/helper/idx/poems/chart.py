import json
import requests

from bs4 import BeautifulSoup
from datetime import datetime

CHART_URL = 'https://chart.poems.co.id'
HISTORY_API = '/api/history'
MARKS_API = '/api/marks'

class PoemsChart(object):

  @staticmethod
  def history(stockCode, interval, startDate):
    now = int(datetime.timestamp(datetime.now().replace(
        hour=0, minute=0, second=0, microsecond=0)))
    start = int(datetime.timestamp(datetime.strptime(startDate, '%Y-%m-%d')))

    # send history request
    response = requests.get(
        url = CHART_URL + HISTORY_API,
        params = {
            'symbol': stockCode,
            'resolution': interval,
            'from': start,
            'to': now
        }
    )
    historyData = response.json()

    outputData = [
        {
            'history_date': datetime.fromtimestamp(t).strftime('%Y-%m-%d'),
            'open': float(historyData['o'][i]),
            'close': float(historyData['c'][i]),
            'high': float(historyData['h'][i]),
            'low': float(historyData['l'][i]),
            'volume': int(historyData['v'][i]),
            'dividend': 0.0,
            'split': 0.0
        }
        for i, t in enumerate(historyData['t'])
        if t != now # remove today data
          and int(historyData['v'][i]) != 0 # no transaction
    ]

    return outputData

  @staticmethod
  def event(stockCode, interval, startDate):
    now = int(datetime.timestamp(datetime.now().replace(
        hour=0, minute=0, second=0, microsecond=0)))
    start = int(datetime.timestamp(datetime.strptime(startDate, '%Y-%m-%d')))

    # send marks request
    response = requests.get(
        url = CHART_URL + MARKS_API,
        params = {
            'symbol': stockCode,
            'resolution': interval,
            'from': start,
            'to': now
        }
    )
    markData = response.json()

    outputData = [
        {
            'date': datetime.fromtimestamp(t),
            'label': markData['label'][i],
            'text': BeautifulSoup(markData['text'][i], 'lxml').prettify()
        }
        for i, t in enumerate(markData['time'])
    ]

    return outputData

if __name__ == '__main__':
  stock = 'BBCA'
  interval = '1D'
  startDate = '1990-01-01'

  print()
  print('===== HISTORY =====')
  for history in PoemsChart.history(stock, interval, startDate):
    print(history)

  print()
  print('===== EVENT =====')
  for event in PoemsChart.event(stock, interval, startDate):
    print(event)
