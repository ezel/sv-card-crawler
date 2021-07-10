import requests
import os
from module.model import Card

img_path = "images"

def updateCardImage(card):
    ### card parameter is a Card model

    def fetchImage(url, linkNumber=1):
        img_name = url[url.rfind('/'):url.rfind('?')]
        img_fname = img_path + img_name

        if (linkNumber == 1) and Card.get_or_none(Card.imageLink1 == img_name):
            # copy from local
            pass
        elif (linkNumber == 2 ) and Card.get_or_none(Card.imageLink2 == img_name):
            pass
        else:
            # download from web
            print('downloading %s...' % img_name)
            img = requests.get(url)

            with open(img_fname, 'wb') as f:
                f.write(img.content)

        return img_name

    card.imageLink1 = fetchImage(card.imageURL1)
    if card.imageURL2:
        card.imageLink2 = fetchImage(card.imageURL2, 2)

    return card.save()

def init_directory():
    # create default dir
    if not os.path.isdir(img_path):
        try:
            os.mkdir(img_path)
        except OSError:
            print ("Creation of the directory %s failed" % img_path)
        else:
            print ("Successfully created the directory %s " % img_path)

if __name__ == "__main__":
    c = Card.get(Card.imageLink1 == None)
    updateCardImage(c)
    print(c.id)
