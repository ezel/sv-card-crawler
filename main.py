from module.listCrawler import getCardList
from module.cardCrawler import fetchSingleCard
from module.model import CardWrapper
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
                    help="if set, always fetch the whole list from web")
parser.add_argument("-s", "--save", type=int, choices=[1,2], default=1,
                    help="save images in: 1=database, 2=the image directory")
args = parser.parse_args()

if __name__ == "__main__":
    # load metadata
    lang = args.language
    currentList = getCardList(args.mode, lang=lang, forceFetch=args.forceFetch)

    # fetch data by multi-threads
    # fetch card data
    CardWrapper.init_tables()
    download_count = 0
    with ThreadPoolExecutor(max_workers=args.maxWorkers) as executor:
        for cid in currentList:
            if CardWrapper.checkNotExist(cid, lang):
                download_count += 1
                future = executor.submit(lambda c, l : CardWrapper.importFromCrawler(fetchSingleCard(c,l)), cid, lang)
                # newCard = future.result()

    # download images
    print('Finish fetching %n Card info, check the images need to download.' % download_count)
    print('Start downloading images...')

    if (args.save == 2):
        CardWrapper.init_directory()

    with ThreadPoolExecutor(max_workers=args.maxWorkers) as executor:
         for img in CardWrapper.ImagesWithoutData():
             future = executor.submit(CardWrapper.updateImage, img, args.save)
    print('Complete downloading images.')
