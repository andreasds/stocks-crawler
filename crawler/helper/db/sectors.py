import mysql.connector.errorcode as errorcode

from crawler.collector import Collector

SECTORS = 'sectors'
SECTOR_ID = 'id'
SECTOR_PARENT = 'parent'
SECTOR_NAME = 'sector_name'

class Sectors(object):

  @staticmethod
  def getSectorId(db, sectorName):
    query = """
        SELECT %s FROM %s
        WHERE %s = '%s'
        LIMIT 1
        """
    data = ( SECTOR_ID, SECTORS,
        SECTOR_NAME, sectorName )

    try:
      cursor = db.cursor()
      cursor.execute(query % data)
    except Exception as err:
      print('ERR: Failed to get sector id = ' + str(err))
      raise RuntimeError('Failed to get sector id = ' + str(err))

    id = cursor.fetchone()[0]
    cursor.close()

    return id

  @staticmethod
  def insertSector(db, sectorName, parent=None):
    query = """
        INSERT INTO %s ( %s, %s )
        SELECT * FROM ( SELECT %s, '%s' ) AS tmp
        WHERE NOT EXISTS (
          SELECT %s FROM %s
          WHERE %s = '%s' LIMIT 1
        ) LIMIT 1
        """
    data = ( SECTORS, SECTOR_PARENT, SECTOR_NAME,
        'NULL' if parent == None else parent, sectorName,
        SECTOR_ID, SECTORS,
        SECTOR_NAME, sectorName )

    try:
      cursor = db.cursor()
      cursor.execute(query % data)
    except Exception as err:
      if err.errno != errorcode.ER_DUP_ENTRY:
        print('ERR: Failed to insert sector = ' + str(err))
        raise RuntimeError('Failed to insert sector = ' + str(err))

    cursor.close()
    db.commit()

if __name__ == '__main__':
  sector = 'Agriculture'
  Sectors.insertSector(Collector().db, sector)
  print(sector, 'id =', Sectors.getSectorId(Collector().db, sector))
  Collector().stop()
