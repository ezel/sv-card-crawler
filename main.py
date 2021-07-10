from module.listCrawler import getCardList
from module.cardCrawler import fetchSingleCard
from module.imageCrawler import updateCardImage, init_directory
from module.model import Card, init_tables
from concurrent.futures import ThreadPoolExecutor

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("mode", type=int, choices=[1,3], default=3,
                    help="game mode of the card: 1=Rotation, 3=Unlimit")
parser.add_argument("language", type=str, choices=['en','ja','zh-tw'], default='en',
                    help="card language: en=english, ja=janpanse, zh-tw=traditional chinese")
parser.add_argument("-w","--maxWorkers", type=int, default=10,
                    help="the max concurrent workers when downling images")
parser.add_argument("-f","--forceFetch", action="store_true",
                    help="wheather fetch from web or use local temp file")
args = parser.parse_args()

if __name__ == "__main__":
    init_directory()
    init_tables()
    lang = args.language
    currentList = getCardList(args.mode, lang=lang, forceFetch=args.forceFetch)
    with ThreadPoolExecutor(max_workers=args.maxWorkers) as executor:
        for cid in currentList:
            if Card.checkNotExist(cid, lang):
                future = executor.submit(lambda c, l : Card.createFromCrawler(fetchSingleCard(c,l)), cid, lang)
                # newCard = future.result()
    print('Finish fetching Card; Start downloading images...')

    with ThreadPoolExecutor(max_workers=args.maxWorkers) as executor:
         for c in Card.select().where( Card.imageLink1 == None ):
             future = executor.submit(updateCardImage, c)
    print('Complete downloading images.')
