import yfinance as yf

from datetime import datetime

class Yahoo(object):

  @staticmethod
  def history(stockCode, interval, startDate):
    endDate = datetime.now().strftime('%Y-%m-%d')

    stock = yf.Ticker(stockCode)
    historyData = stock.history('max', interval, startDate, endDate,
        auto_adjust = False)

    outputData = [
        {
            'history_date': date.strftime('%Y-%m-%d'),
            'open': historyData['Open'][i],
            'close': historyData['Close'][i],
            'high': historyData['High'][i],
            'low': historyData['Low'][i],
            'volume': historyData['Volume'][i],
            'dividend': historyData['Dividends'][i],
            'split': historyData['Stock Splits'][i]
        }
        for i, date in enumerate(historyData.index)
        if date != endDate # remove today data
    ]

    return outputData

  @staticmethod
  def event(stockCode, interval, startDate):
    history = Yahoo.history(stockCode, interval, startDate)

    outputData = [
      data for data in history
      if data['dividend'] != 0 or data['split'] != 0
    ]

    return outputData

if __name__ == '__main__':
  stock = 'BBCA.JK'
  interval = '1D'
  startDate = '1990-01-01'

  print()
  print('===== HISTORY =====')
  for history in Yahoo.history(stock, interval, startDate):
    print(history)

  print()
  print('===== EVENT =====')
  for event in Yahoo.event(stock, interval, startDate):
    print(event)
