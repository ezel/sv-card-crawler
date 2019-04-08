import requests
import os
from concurrent.futures import ThreadPoolExecutor
from model import Card

img_path = "images"

def updateCardImage(card):
    ### card parameter is a Card model

    def fetchImage(url):
        img_name = url[url.rfind('/'):url.rfind('?')]
        img_fname = img_path + img_name

        print('downloading %s...' % img_name)
        img = requests.get(url)

        with open(img_fname, 'wb') as f:
            f.write(img.content)
        return img_name

    card.imageLink1 = fetchImage(card.imageURL1)
    if card.imageURL2:
        card.imageLink2 = fetchImage(card.imageURL2)

    return card.save()

def downloadAllCardsImages(max_workers=10):
    # create default dir
    if not os.path.isdir(img_path):
        try:
            os.mkdir(img_path)
        except OSError:
            print ("Creation of the directory %s failed" % img_path)
        else:
            print ("Successfully created the directory %s " % img_path)

    # download images
    with ThreadPoolExecutor(max_workers) as executor:
         for c in Card.select().where( Card.imageLink1 == None ):
             future = executor.submit(updateCardImage, c)

if __name__ == "__main__":
    downloadAllCardsImages()
