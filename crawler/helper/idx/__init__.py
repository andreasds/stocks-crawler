import requests

from crawler.collector import Collector
from crawler.helper.db.industries import Industries
from crawler.helper.db.markets import Markets
from crawler.helper.db.sectors import Sectors
from crawler.helper.db.stocks import Stocks
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
    marketId = cls().createMarket(db)

    # get emitens size
    emitenSize = cls().getEmitenSize()

    # get list emitens
    emitens = cls().getListEmitens(emitenSize)

    # store emiten
    print('Storing stocks data...')
    for emiten in emitens:
      sector = " ".join([ word.capitalize()  for word in emiten['Sektor'].split(' ') if word != '' ])
      Sectors.insertSector(db, sector)

      industry = " ".join([ word.capitalize()  for word in emiten['SubSektor'].split(' ') if word != '' ])
      Industries.insertIndustry(db, sector, industry)

      Stocks.insertStock(db, IDX, industry, emiten['KodeEmiten'], emiten['NamaEmiten'])

  def getEmitenSize(self):
    # request list emitens
    response = requests.get(
        url = IDX_URL + EMITEN_API
    )

    if response.status_code != HTTPStatus.OK:
      raise RuntimeError('Response status ' + str(response.status_code) +
          ' = ' + str(response.reason))

    return len(response.json())

  def getListEmitens(self, size):
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

  def createMarket(self, db):
    return Markets.insertMarket(db, IDX, IDX_DESC)

if __name__ == '__main__':
  Idx.storeStocks(Collector().db)
  Collector().stop()
