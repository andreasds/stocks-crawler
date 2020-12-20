import json
import requests

from bs4 import BeautifulSoup
from datetime import datetime

CHART_URL = 'https://chart.poems.co.id'
HISTORY_API = '/api/history'
MARKS_API = '/api/marks'

class PoemsChart(object):

  @staticmethod
  def history(symbol, resolution, years):
    print('History', symbol, resolution, years)

    now = datetime.now()
    start = datetime(now.year - years - 1, now.month, now.day)
    print(int(datetime.timestamp(datetime.now())))

    # send history request
    response = requests.get(
        url = CHART_URL + HISTORY_API,
        params = {
            'symbol': symbol,
            'resolution': resolution,
            'from': int(datetime.timestamp(start)),
            'to': int(datetime.timestamp(now))
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
    ]

    for data in outputData:
      print(data)

  @staticmethod
  def marks(symbol, resolution, years):
    print('Marks', symbol, resolution, years)

    now = datetime.now()
    start = datetime(now.year - years - 1, now.month, now.day)
    print(int(datetime.timestamp(datetime.now())))

    # send history request
    response = requests.get(
        url = CHART_URL + MARKS_API,
        params = {
            'symbol': symbol,
            'resolution': resolution,
            'from': int(datetime.timestamp(start)),
            'to': int(datetime.timestamp(now))
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

    for data in outputData:
      for k, v in data.items():
        print(k, v)
