import crawler.helper.db.sectors as sectors
import mysql.connector.errorcode as errorcode

from crawler.collector import Collector

INDUSTRIES = 'industries'
INDUSTRY_ID = 'id'
INDUSTRY_PARENT = 'parent'
INDUSTRY_SECTOR = 'sector_id'
INDUSTRY_NAME = 'industry_name'

class Industries(object):

  @staticmethod
  def getIndustryId(db, industryName):
    query = """
        SELECT %s FROM %s
        WHERE %s = '%s'
        LIMIT 1
        """
    data = ( INDUSTRY_ID, INDUSTRIES,
        INDUSTRY_NAME, industryName )

    try:
      cursor = db.cursor()
      cursor.execute(query % data)
    except Exception as err:
      print('ERR: Failed to get industry id = ' + str(err))
      raise RuntimeError('Failed to get industry id = ' + str(err))

    id = cursor.fetchone()[0]
    cursor.close()

    return id

  @staticmethod
  def insertIndustry(db, sectorName, industryName, parent=None):
    query = """
        INSERT INTO %s ( %s, %s, %s )
        SELECT * FROM ( SELECT %s, '%s',
          ( SELECT %s FROM %s WHERE %s = '%s' LIMIT 1 ) ) AS tmp
        WHERE NOT EXISTS (
          SELECT %s FROM %s
          WHERE %s = '%s' LIMIT 1
        ) LIMIT 1
        """
    data = ( INDUSTRIES, INDUSTRY_PARENT, INDUSTRY_NAME, INDUSTRY_SECTOR,
        'NULL' if parent == None else parent, industryName,
        sectors.SECTOR_ID, sectors.SECTORS, sectors.SECTOR_NAME, sectorName,
        INDUSTRY_ID, INDUSTRIES,
        INDUSTRY_NAME, industryName )

    try:
      cursor = db.cursor()
      cursor.execute(query % data)
    except Exception as err:
      if err.errno != errorcode.ER_DUP_ENTRY:
        print('ERR: Failed to insert industry = ' + str(err))
        raise RuntimeError('Failed to insert industry = ' + str(err))

    cursor.close()
    db.commit()

if __name__ == '__main__':
  sector = 'Agriculture'
  industry = 'Plantation'
  Industries.insertIndustry(Collector().db, sector, industry)
  print(industry, 'id =', Industries.getIndustryId(Collector().db, industry))
  Collector().stop()
