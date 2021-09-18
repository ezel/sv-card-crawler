from module.listCrawler import getCardList
from module.cardCrawler import fetchSingleCard
from module.imageCrawler import updateCardImage, init_directory
from module.model import CardWrapper, init_tables
from concurrent.futures import ThreadPoolExecutor

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--mode", type=int, choices=[1,3], default=1,
                    help="game mode: 1=Rotation, 3=Unlimit, default=1")
parser.add_argument("-l", "--language", type=str, choices=['en','ja','zh-tw'], default='zh-tw',
                    help="card language: default=zh-tw")
parser.add_argument("-w","--maxWorkers", type=int, default=20,
                    help="the max concurrent workers when downling images, default=20")
parser.add_argument("-f","--forceFetch", action="store_true",
                    help="if set, will fetch a list from web")
args = parser.parse_args()

if __name__ == "__main__":
    # load metadata
    lang = args.language
    currentList = getCardList(args.mode, lang=lang, forceFetch=args.forceFetch)

    # fetch data by multi-threads
    # fetch card data
    init_tables()
    download_count = 0
    with ThreadPoolExecutor(max_workers=args.maxWorkers) as executor:
        for cid in currentList:
            if CardWrapper.checkNotExist(cid, lang):
                download_count += 1
                future = executor.submit(lambda c, l : CardWrapper.importFromCrawler(fetchSingleCard(c,l)), cid, lang)
                # newCard = future.result()

    # download images
    print('Finish fetching Card, %d images need to download.' % download_count)
    print('Start downloading images...')

    init_directory()
    exit()
    with ThreadPoolExecutor(max_workers=args.maxWorkers) as executor:
         for c in Card.select().where( Card.imageLink1 == None ):
             future = executor.submit(updateCardImage, c)
    print('Complete downloading images.')
