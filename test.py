from module.cardCrawler import fetchSingleCard
from module.model import CardWrapper, init_tables

init_tables()
x1 = fetchSingleCard("120631010")
CardWrapper.importFromCrawler(x1)
