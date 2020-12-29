import crawler.helper.idx as idx
import crawler.helper.db.industries as industries
import crawler.helper.db.markets as markets
import mysql.connector.errorcode as errorcode

STOCKS = 'stocks'
STOCK_ID = 'id'
STOCK_MARKET = 'market_id'
STOCK_INDUSTRY = 'industry_id'
STOCK_CODE = 'stock_code'
STOCK_DESC = 'description'
STOCK_ACTIVE = 'is_active'

class Stocks(object):

  @staticmethod
  def getStockId(db, marketName, stockCode):
    query = """
        SELECT stock.%s FROM %s AS stock
          LEFT JOIN %s AS market ON stock.%s = market.%s
        WHERE stock.%s = '%s' AND market.%s = '%s'
        LIMIT 1
        """
    data = ( STOCK_ID, STOCKS,
        markets.MARKETS, STOCK_MARKET, markets.MARKET_ID,
        STOCK_CODE, stockCode, markets.MARKET_NAME, marketName )

    try:
      cursor = db.cursor()
      cursor.execute(query % data)
    except Exception as err:
      print('ERR: Failed to get stock id = ' + str(err))
      raise RuntimeError('Failed to get stock id = ' + str(err))

    id = cursor.fetchone()[0]
    cursor.close()

    return id

  @staticmethod
  def insertStock(db, marketName, industryName, stockCode, description=''):
    query = """
        INSERT INTO %s ( %s, %s, %s, %s )
        SELECT * FROM ( SELECT '%s', '%s',
          ( SELECT %s FROM %s WHERE %s = '%s' LIMIT 1 ),
          ( SELECT %s FROM %s WHERE %s = '%s' LIMIT 1 ) ) AS tmp
        WHERE NOT EXISTS (
          SELECT stock.%s FROM %s AS stock
            LEFT JOIN %s AS market ON stock.%s = market.%s
          WHERE stock.%s = '%s' AND market.%s = '%s' LIMIT 1
        ) LIMIT 1
        """
    data = ( STOCKS, STOCK_CODE, STOCK_DESC, STOCK_MARKET, STOCK_INDUSTRY,
        stockCode, description,
        markets.MARKET_ID, markets.MARKETS, markets.MARKET_NAME, marketName,
        industries.INDUSTRY_ID, industries.INDUSTRIES, industries.INDUSTRY_NAME, industryName,
        STOCK_ID, STOCKS,
        markets.MARKETS, STOCK_MARKET, markets.MARKET_ID,
        STOCK_CODE, stockCode, markets.MARKET_NAME, marketName )

    try:
      cursor = db.cursor()
      cursor.execute(query % data)
    except Exception as err:
      if err.errno != errorcode.ER_DUP_ENTRY:
        print('ERR: Failed to insert stock = ' + str(err))
        raise RuntimeError('Failed to insert stock = ' + str(err))

    cursor.close()
    db.commit()

if __name__ == '__main__':
  from crawler.collector import Collector

  industry = 'Plantation'
  stock = 'AALI'
  Stocks.insertStock(Collector().db, idx.IDX, industry, stock)
  print(stock, 'id =', Stocks.getStockId(Collector().db, idx.IDX, stock))
  Collector().stop()
