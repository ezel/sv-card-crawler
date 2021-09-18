from module.cardCrawler import fetchSingleCard
from module.model import CardWrapper, init_tables

init_tables()
for cid in ['707034010', "120631010"]:
    x1 = fetchSingleCard(cid)
    CardWrapper.importFromCrawler(x1)
