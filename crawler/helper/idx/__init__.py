import requests

from crawler.helper.db.histories import Histories
from crawler.helper.db.industries import Industries
from crawler.helper.db.markets import Markets
from crawler.helper.db.sectors import Sectors
from crawler.helper.db.stocks import Stocks
from crawler.helper.idx.poems.chart import PoemsChart
from crawler.helper.yahoo import Yahoo
from http import HTTPStatus

IDX = 'IDX'
IDX_DESC = 'Indonesia Stock Exchange'

IDX_URL = 'https://www.idx.co.id/umbraco/Surface'
EMITEN_API = '/Helper/GetEmiten'
COMPANY_PROFILE_API = '/ListedCompany/GetCompanyProfiles'

class Idx(object):

  @classmethod
  def storeStocks(cls, db):
    print('Collect IDX stocks')

    # get market id
    marketId = cls().__createMarket(db)

    # get emitens size
    emitenSize = cls().__getEmitenSize()

    # get list emitens
    emitens = cls().__getListEmitens(emitenSize)

    # store emiten
    for emiten in emitens:
      sector = " ".join([ word.capitalize()  for word in emiten['Sektor'].split(' ') if word != '' ])
      Sectors.insertSector(db, sector)

      industry = " ".join([ word.capitalize()  for word in emiten['SubSektor'].split(' ') if word != '' ])
      Industries.insertIndustry(db, sector, industry)

      Stocks.insertStock(db, IDX, industry, emiten['KodeEmiten'], emiten['NamaEmiten'])

  def __getEmitenSize(self):
    # request list emitens
    response = requests.get(
        url = IDX_URL + EMITEN_API
    )

    if response.status_code != HTTPStatus.OK:
      raise RuntimeError('Response status ' + str(response.status_code) +
          ' = ' + str(response.reason))

    return len(response.json())

  def __getListEmitens(self, size):
    # request list emitens
    response = requests.get(
        url = IDX_URL + COMPANY_PROFILE_API,
        params = {
            'length': size
        }
    )

    if response.status_code != HTTPStatus.OK:
      raise RuntimeError('Response status ' + str(response.status_code) +
          ' = ' + str(response.reason))

    return response.json()['data']

  def __createMarket(self, db):
    return Markets.insertMarket(db, IDX, IDX_DESC)

  @classmethod
  def updateStock(cls, db, stockId, stockCode, startDate):
    histories = PoemsChart.history(stockCode, '1D', startDate)

    for history in histories:
      Histories.insertHistory(db, stockId, history['history_date'],
          history['open'], history['high'], history['low'],
          history['close'], history['volume'])

    events = Yahoo.event(stockCode + '.JK', '1D', startDate)

if __name__ == '__main__':
  from crawler.collector import Collector

  stock = 'BBCA'
  stockId = Stocks.getStockId(Collector().db, IDX, stock)
  historyDate = '1990-01-01'

  Idx.storeStocks(Collector().db)
  Idx.updateStock(Collector().db, stockId, stock, historyDate)

  Collector().stop()
