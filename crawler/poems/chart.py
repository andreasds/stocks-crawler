import json
import requests

from bs4 import BeautifulSoup
from datetime import datetime

CHART_URL = 'https://chart.poems.co.id'
HISTORY_API = '/api/history'
MARKS_API = '/api/marks'

class PoemsChart(object):

  @staticmethod
  def history(symbol, resolution, year, month, day, hour=0, minute=0, second=0):
    now = int(datetime.timestamp(datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)))
    start = int(datetime.timestamp(datetime(year, month, day, hour, minute, second, 0)))

    # send history request
    response = requests.get(
        url = CHART_URL + HISTORY_API,
        params = {
            'symbol': symbol,
            'resolution': resolution,
            'from': start,
            'to': now
        }
    )
    historyData = response.json()

    outputData = [
        {
            'date': datetime.fromtimestamp(t),
            'open': historyData['o'][i],
            'close': historyData['c'][i],
            'high': historyData['h'][i],
            'low': historyData['l'][i],
            'volume': historyData['v'][i]
        }
        for i, t in enumerate(historyData['t'])
        if t != now # remove today data
    ]

#    for data in outputData:
#      print(data)

  @staticmethod
  def marks(symbol, resolution, year, month, day, hour=0, minute=0, second=0):
    now = int(datetime.timestamp(datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)))
    start = int(datetime.timestamp(datetime(year, month, day, hour, minute, second, 0)))

    # send marks request
    response = requests.get(
        url = CHART_URL + MARKS_API,
        params = {
            'symbol': symbol,
            'resolution': resolution,
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

#    for data in outputData:
#      for k, v in data.items():
#        print(k, v)

if __name__ == '__main__':
  PoemsChart.history('BBRI', '1D', 1990, 1, 1)
  PoemsChart.marks('BBRI', '1D', 1990, 1, 1)
