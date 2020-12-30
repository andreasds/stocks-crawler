import crawler.helper.config as config
import crawler.helper.idx as idx
import mysql.connector as mysql

from crawler.helper.db.histories import Histories
from crawler.helper.singleton import Singleton

DB_CONFIG = '.config'
DB_NAME = 'stocks_crawler'

INIT_SQL = 'db.sql'

class Collector(metaclass=Singleton):

  stockSource = {
    idx.IDX: idx.Idx.storeStocks
  }

  historySource = {
    idx.IDX: idx.Idx.storeHistory
  }

  eventSource = {
    idx.IDX: idx.Idx.updateEvent
  }

  def __init__(self):
    # read config
    self.__dbConfig = config.readDbConfig(DB_CONFIG)

    # initialize database
    self.start()

  def start(self):
    # connect database
    self.__connectDatabase()

  def stop(self):
    # close database
    self.db.close()

  def __connectDatabase(self):
    try:
      self.db = mysql.connect(
          host=self.__dbConfig['dbHost'],
          port=int(self.__dbConfig['dbPort']),
          user=self.__dbConfig['dbUser'],
          password=self.__dbConfig['dbPassword'],
          database=DB_NAME
      )
      print('Connected to database')
    except Exception:
      # create database
      self.db = mysql.connect(
          host=self.__dbConfig['dbHost'],
          port=int(self.__dbConfig['dbPort']),
          user=self.__dbConfig['dbUser'],
          password=self.__dbConfig['dbPassword']
      )
      self.__initDatabase()
      self.stop()

      # reconnect to database
      self.__connectDatabase()

  def __initDatabase(self):
    print('Initialize database')
    cursor = self.db.cursor()

    queries = []
    with open(INIT_SQL) as f:
      queries = f.read().split(';')

    for query in queries:
      if query.strip() == '':
        # ignore empty line
        continue

      result = cursor.execute(query.strip())

    cursor.close()
    self.db.commit()

  def addMarket(self, market):
    print('Add', market, 'to database')

    self.stockSource.get(
        market,
        lambda db : self.__undefinedMarket(market)
    )(self.db)

  def __undefinedMarket(self, market):
    raise NotImplementedError(str(market) + ' market sources not defined')

  def updateMarket(self):
    histories = Histories.getLastStockHistory(self.db)
    for stockId, market, stockCode, startDate in histories:
      self.historySource.get(
        market,
        lambda db, id, code, date: self.__undefinedMarket(market)
      )(self.db, stockId, stockCode, startDate)

    events = Histories.getLastStockEvent(self.db)
    for stockId, market, stockCode, startDate in events:
      self.eventSource.get(
        market,
        lambda db, id, code, date: self.__undefinedMarket(market)
      )(self.db, stockId, stockCode, startDate)

if __name__ == '__main__':
  Collector()
  Collector().addMarket('IDX')
  Collector().updateMarket()
  Collector().stop()
