import crawler.helper.db as dbHelper
import crawler.helper.db.industries as industries
import crawler.helper.db.markets as markets
import crawler.helper.db.stocks as stocks
import crawler.helper.idx as idx
import mysql.connector.errorcode as errorcode

HISTORIES = 'histories'
HISTORY_ID = 'id'
HISTORY_STOCK = 'stock_id'
HISTORY_DATE = 'history_date'
HISTORY_OPEN = 'open'
HISTORY_HIGH = 'high'
HISTORY_LOW = 'low'
HISTORY_CLOSE = 'close'
HISTORY_VOLUME = 'volume'
HISTORY_DIVIDEND = 'dividend'
HISTORY_SPLIT = 'split'

class Histories(object):

  @staticmethod
  def getHistoryId(db, marketName, stockCode, historyDate):
    query = """
        SELECT history.%s FROM %s AS history
          LEFT JOIN %s AS stock ON history.%s = stock.%s
          LEFT JOIN %s AS market ON stock.%s = market.%s
        WHERE history.%s = '%s'
          AND stock.%s = '%s'
          AND market.%s = '%s'
        LIMIT 1
        """
    data = ( HISTORY_ID, HISTORIES,
        stocks.STOCKS, HISTORY_STOCK, stocks.STOCK_ID,
        markets.MARKETS, stocks.STOCK_MARKET, markets.MARKET_ID,
        HISTORY_DATE, historyDate,
        stocks.STOCK_CODE, stockCode,
        markets.MARKET_NAME, marketName )

    try:
      cursor = db.cursor()
      cursor.execute(query % data)
    except Exception as err:
      print('ERR: Failed to get history id = ' + str(err))
      raise RuntimeError('Failed to get history id = ' + str(err))

    id = cursor.fetchone()[0]
    cursor.close()

    return id

  @staticmethod
  def insertHistory(db, stockId, historyDate, openPrice, highPrice, lowPrice,
      closePrice, volume, dividend=0.0, split=0.0):
    query = """
        INSERT INTO %s ( %s, %s, %s, %s, %s, %s, %s, %s, %s )
        SELECT * FROM (
          SELECT %s as stock_id, '%s' as history_date, %s as open, %s as high,
            %s as low, %s as close, %s as volume, %s as dividend, %s as split ) AS tmp
        WHERE NOT EXISTS (
          SELECT %s FROM %s
          WHERE %s = %s AND %s = '%s' LIMIT 1
        ) LIMIT 1
        """
    data = ( HISTORIES, HISTORY_STOCK, HISTORY_DATE, HISTORY_OPEN, HISTORY_HIGH,
          HISTORY_LOW, HISTORY_CLOSE, HISTORY_VOLUME, HISTORY_DIVIDEND, HISTORY_SPLIT,
        stockId, historyDate, openPrice, highPrice, lowPrice, closePrice, volume,
          dividend, split,
        HISTORY_ID, HISTORIES,
        HISTORY_STOCK, stockId, HISTORY_DATE, historyDate )

    try:
      cursor = db.cursor()
      cursor.execute(query % data)
    except Exception as err:
      if err.errno != errorcode.ER_DUP_ENTRY:
        print('ERR: Failed to insert history = ' + str(err))
        raise RuntimeError('Failed to insert history = ' + str(err))

    cursor.close()
    db.commit()

  @staticmethod
  def updateHistory(db, stockId, historyDate, openPrice, highPrice, lowPrice,
      closePrice, volume):
    query = """
        UPDATE %s
        SET %s = %s, %s = %s, %s = %s, %s = %s, %s = %s
        WHERE %s = %s AND %s = '%s'
        """
    data = ( HISTORIES,
        HISTORY_OPEN, openPrice, HISTORY_HIGH, highPrice, HISTORY_LOW,
          lowPrice, HISTORY_CLOSE, closePrice, HISTORY_VOLUME, volume,
        HISTORY_STOCK, stockId, HISTORY_DATE, historyDate)

    try:
      cursor = db.cursor()
      cursor.execute(query % data)
    except Exception as err:
      if err.errno != errorcode.ER_DUP_ENTRY:
        print('ERR: Failed to update history = ' + str(err))
        raise RuntimeError('Failed to update history = ' + str(err))

    cursor.close()
    db.commit()

  @staticmethod
  def getLastStockHistory(db):
    query = """
        SELECT stock.%s, market.%s, stock.%s,
          CASE WHEN history.%s is NULL then '%s'
          ELSE DATE_ADD(history.%s, INTERVAL 1 DAY) END AS %s
        FROM %s AS stock
          LEFT JOIN ( SELECT %s, MAX(%s) as %s FROM %s GROUP BY %s ) AS history
            ON stock.%s = history.%s
          LEFT JOIN %s AS market ON market.%s = stock.%s
        WHERE stock.%s
        """
    data = ( stocks.STOCK_ID, markets.MARKET_NAME, stocks.STOCK_CODE,
        HISTORY_DATE, dbHelper.DEFAULT_DATE,
        HISTORY_DATE, HISTORY_DATE,
        stocks.STOCKS,
        HISTORY_STOCK, HISTORY_DATE, HISTORY_DATE, HISTORIES, HISTORY_STOCK,
        stocks.STOCK_ID, HISTORY_STOCK,
        markets.MARKETS, markets.MARKET_ID, stocks.STOCK_MARKET,
        stocks.STOCK_ACTIVE)

    try:
      cursor = db.cursor()
      cursor.execute(query % data)
    except Exception as err:
      if err.errno != errorcode.ER_DUP_ENTRY:
        print('ERR: Failed to insert history = ' + str(err))
        raise RuntimeError('Failed to insert history = ' + str(err))

    lastHistory = cursor.fetchall()
    cursor.close()
    db.commit()

    return lastHistory

  @staticmethod
  def updateEvent(db, stockId, historyDate, dividend, split):
    query = """
        UPDATE %s AS history,
          ( SELECT %s FROM %s
            WHERE %s = %s AND %s = '%s'
            ORDER BY %s DESC LIMIT 1 ) AS tmp
        SET %s = %s, %s = %s
        WHERE history.%s = tmp.%s
        """
    data = ( HISTORIES,
        HISTORY_ID, HISTORIES,
        HISTORY_STOCK, stockId, HISTORY_DATE, historyDate,
        HISTORY_DATE,
        HISTORY_DIVIDEND, dividend, HISTORY_SPLIT, split,
        HISTORY_ID, HISTORY_ID )

    try:
      cursor = db.cursor()
      cursor.execute(query % data)
    except Exception as err:
      if err.errno != errorcode.ER_DUP_ENTRY:
        print('ERR: Failed to update history = ' + str(err))
        raise RuntimeError('Failed to update history = ' + str(err))

    cursor.close()
    db.commit()

  @staticmethod
  def getLastStockEvent(db):
    query = """
        SELECT stock.%s, market.%s, stock.%s,
          CASE WHEN history.%s is NULL then '%s'
          ELSE DATE_ADD(history.%s, INTERVAL 1 DAY) END AS %s
        FROM %s AS stock
          LEFT JOIN
            ( SELECT %s, MAX(%s) as %s FROM %s
              WHERE %s != 0 OR %s != 0 GROUP BY %s ) AS history
            ON stock.%s = history.%s
          LEFT JOIN %s AS market ON market.%s = stock.%s
        WHERE stock.%s
        """
    data = ( stocks.STOCK_ID, markets.MARKET_NAME, stocks.STOCK_CODE,
        HISTORY_DATE, dbHelper.DEFAULT_DATE,
        HISTORY_DATE, HISTORY_DATE,
        stocks.STOCKS,
        HISTORY_STOCK, HISTORY_DATE, HISTORY_DATE, HISTORIES,
        HISTORY_DIVIDEND, HISTORY_SPLIT, HISTORY_STOCK,
        stocks.STOCK_ID, HISTORY_STOCK,
        markets.MARKETS, markets.MARKET_ID, stocks.STOCK_MARKET,
        stocks.STOCK_ACTIVE)

    try:
      cursor = db.cursor()
      cursor.execute(query % data)
    except Exception as err:
      if err.errno != errorcode.ER_DUP_ENTRY:
        print('ERR: Failed to insert history = ' + str(err))
        raise RuntimeError('Failed to insert history = ' + str(err))

    lastHistory = cursor.fetchall()
    cursor.close()
    db.commit()

    return lastHistory

if __name__ == '__main__':
  from crawler.collector import Collector

  stock = 'BBCA'
  stockId = stocks.Stocks.getStockId(Collector().db, idx.IDX, stock)
  historyDate = '2020-01-01'

  Histories.insertHistory(Collector().db, stockId, historyDate, 10000.0, 12000.0, 7000.0,
      10500, 123456789)
  Histories.updateHistory(Collector().db, stockId, historyDate, 5000.0, 6000.0, 3500.0,
      5250, 987654321)
  Histories.updateEvent(Collector().db, stockId, historyDate, 50.0, 0.0)
  print(stock, historyDate, 'id =',
      Histories.getHistoryId(Collector().db, idx.IDX, stock, historyDate))

  print()
  print('===== LAST HISTORY =====')
  for history in Histories.getLastStockHistory(Collector().db):
    print(history)

  print()
  print('===== LAST EVENT =====')
  for event in Histories.getLastStockEvent(Collector().db):
    print(event)

  Collector().stop()
