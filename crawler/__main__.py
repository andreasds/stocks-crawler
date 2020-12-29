import crawler.helper.idx as idx
import sys

from crawler.collector import Collector

if __name__ == '__main__':
  collector = Collector()

  if len(sys.argv[1:]):
    for market in sys.argv[1:]:
      # add market stocks database
      collector.addMarketDb(market)

  # close db
  collector.stop()
