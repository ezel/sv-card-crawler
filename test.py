from module.cardCrawler import fetchSingleCard
from module.model import CardWrapper, Image

CardWrapper.init_tables()
for cid in ['707034010', "120631010"]:
    for lang in ['en', 'jp', 'zh-tw']:
        x1 = fetchSingleCard(cid, lang)
        CardWrapper.importFromCrawler(x1)

CardWrapper.init_directory()
img1 = Image.get_or_none(filename='C_109034010')
img1.fetchImageFile()
img2 = Image.get_or_none(filename='C_707034010')
img2.fetchImageData(1)
