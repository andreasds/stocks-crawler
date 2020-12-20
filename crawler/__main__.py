from crawler.poems import Poems
from crawler.poems.chart import PoemsChart

if __name__ == '__main__':
#  Poems().init()
#  Poems().login()
  PoemsChart.history('BBRI', '1D', 10)
  PoemsChart.marks('BBRI', '1D', 10)
