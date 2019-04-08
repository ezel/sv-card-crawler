from listCrawler import getCardList
from cardCrawler import fetchSingleCard
from imageCrawler import downloadAllCardsImages
from model import Card, init_tables

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
    init_tables()
    lang = args.language
    currentList = getCardList(args.mode, forceFetch=args.forceFetch)
    for cid in currentList:
        if Card.checkNotExist(cid, lang):
            currentCard = fetchSingleCard(cid)
            newCard = Card.createFromCrawler(currentCard)

    downloadAllCardsImages(args.maxWorkers)
