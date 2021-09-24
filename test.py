from module.cardCrawler import fetchSingleCard
from module.model import CardWrapper, Image

CardWrapper.init_tables()
for cid in ['707034010', "120631010"]:
    for lang in ['en', 'jp', 'zh-tw']:
        x1 = fetchSingleCard(cid, lang)
        CardWrapper.importFromCrawler(x1)

CardWrapper.init_directory()

for i in CardWrapper.ImagesWithoutData():
    CardWrapper.updateImage(i)
