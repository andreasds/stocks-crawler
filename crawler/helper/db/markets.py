import crawler.helper.idx as idx
import mysql.connector.errorcode as errorcode

from crawler.collector import Collector

MARKETS = 'markets'
MARKET_ID = 'id'
MARKET_NAME = 'market_name'
MARKET_DESC = 'description'

class Markets(object):

  @staticmethod
  def getMarketId(db, marketName):
    query = """
        SELECT %s FROM %s
        WHERE %s = '%s'
        LIMIT 1
        """
    data = ( MARKET_ID, MARKETS,
        MARKET_NAME, marketName )

    try:
      cursor = db.cursor()
      cursor.execute(query % data)
    except Exception as err:
      print('ERR: Failed to get market id = ' + str(err))
      raise RuntimeError('Failed to get market id = ' + str(err))

    id = cursor.fetchone()[0]
    cursor.close()

    return id

  @staticmethod
  def insertMarket(db, marketName, marketDescription):
    query = """
        INSERT INTO %s ( %s, %s )
        SELECT * FROM ( SELECT '%s', '%s' ) AS tmp
        WHERE NOT EXISTS (
          SELECT %s FROM %s
          WHERE %s = '%s' LIMIT 1
        ) LIMIT 1
        """
    data = ( MARKETS, MARKET_NAME, MARKET_DESC,
        marketName, marketDescription,
        MARKET_ID, MARKETS,
        MARKET_NAME, marketName )

    try:
      cursor = db.cursor()
      cursor.execute(query % data)
    except Exception as err:
      if err.errno != errorcode.ER_DUP_ENTRY:
        print('ERR: Failed to insert market = ' + str(err))
        raise RuntimeError('Failed to insert market = ' + str(err))

    cursor.close()
    db.commit()

if __name__ == '__main__':
  Markets.insertMarket(Collector().db, idx.IDX, idx.IDX_DESC)
  print(idx.IDX, 'id =', Markets.getMarketId(Collector().db, idx.IDX))
  Collector().stop()
