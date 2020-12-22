import crawler.helper.config as config
import mysql.connector as mysql

from crawler.helper.singleton import Singleton

DB_CONFIG = '.config'
DB_NAME = 'stocks_crawler'

INIT_SQL = 'db.sql'

class Analyzer(metaclass=Singleton):

  def __init__(self, dropDb=False):
    print('Analyzer __init__')

    # read config
    dbConfig = config.readDbConfig(DB_CONFIG)

    # initialize database
    self.db = mysql.connect(
        host=dbConfig['dbHost'],
        port=int(dbConfig['dbPort']),
        user=dbConfig['dbUser'],
        password=dbConfig['dbPassword']
    )
    if dropDb:
      self.__initDatabase()
    self.db.close()

    # reconnect to database
    self.db = mysql.connect(
        host=dbConfig['dbHost'],
        port=int(dbConfig['dbPort']),
        user=dbConfig['dbUser'],
        password=dbConfig['dbPassword'],
        database=DB_NAME
    )

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

    self.db.commit()

if __name__ == '__main__':
  Analyzer(True)
