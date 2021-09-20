from peewee import *
import os
import requests

db = SqliteDatabase('cards.db')

class Image(Model):
    #card = DeferredForeignKey('Card', null=True, field='card_id')
    filename = CharField(primary_key=True)
    imageURL = CharField() # save the origin URL of image
    imagePath = CharField(null=True) # the path of image file, or image name if data save in db blob
    data = BlobField(null=True)
    compressed = BooleanField(default=False)

    class Meta:
        database = db

    @staticmethod
    def checkNotExist(fname):
        if None == Image.get_or_none(filename=filename):
            return True
        return False

    @classmethod
    def fromCrawler(cls, crawler):
        def createImage(url):
            fname = url[url.rfind('/')+1:url.rfind('.')]
            aImg = Image.get_or_none(filename=fname)
            if aImg == None:
                aImg = Image()
                aImg.imageURL = url
                aImg.filename = fname
                aImg.save(force_insert=True)
            return aImg

        aImg1 = createImage(crawler.mainSoup[1][0])

        if len(crawler.mainSoup[1]) > 1:
            aImg2 = createImage(crawler.mainSoup[1][1])
        else:
            aImg2 = None

        return aImg1, aImg2

    def fetchImageFile(self, image_dir="images/"):
        url = self.imageURL
        save_name = url[url.rfind('/')+1:url.rfind('?')]
        save_path = image_dir + save_name

        # download from web
        print('downloading %s...' % save_name)
        img = requests.get(url)

        with open(save_path, 'wb') as f:
            f.write(img.content)
        self.imagePath = save_path
        return self.save()

    def fetchImageData(self, compress):
        url = self.imageURL
        self.imagePath = url[url.rfind('/')+1:url.rfind('?')]
        print('downloading %s...' % self.filename)
        img = requests.get(self.imageURL)
        self.data = img.content
        return self.save()

class Card(Model):
    card_id = CharField(primary_key=True)
    img1 = ForeignKeyField(Image, null=True)
    img2 = ForeignKeyField(Image, null=True)

    Atk1 = IntegerField(null=True)
    HP1 = IntegerField(null=True)
    Atk2 = IntegerField(null=True)
    HP2 = IntegerField(null=True)

    minCost = IntegerField(null=True)
    mainCard = ForeignKeyField('self', backref='subCards', null=True)

    class Meta:
        database = db

    @classmethod
    def fromCrawler(cls, crawler):
        aCard = Card(card_id=crawler.cid)

        # divide soup
        mainSoup = crawler.mainSoup
        infoSoup = crawler.infoSoup

        # for image object
        aCard.img1, aCard.img2 = Image.fromCrawler(crawler)

        if len(mainSoup[1]) > 1:
            aCard.Atk2, aCard.HP2 = mainSoup[2][1]
        if mainSoup[2]:
            aCard.Atk1, aCard.HP1 = mainSoup[2][0]
        return aCard


class CardLanguageInfo(Model):
    card = ForeignKeyField(Card, null=True, field='card_id')
    language = CharField()
    title = CharField()

    skill1 = TextField()
    skill2 = TextField(null=True)
    desp1 = TextField()
    desp2 = TextField(null=True)

    # info
    traitInfo = CharField()
    classInfo = CharField()
    rarityInfo = CharField()
    createInfo = IntegerField()
    liquefyInfo = CharField()
    cardPackInfo = CharField()

    class Meta:
        database = db

    @classmethod
    def fromCrawler(cls, crawler):
        aInfo = CardLanguageInfo(card=crawler.cid)
        # divide soup
        mainSoup = crawler.mainSoup
        infoSoup = crawler.infoSoup
        # setter
        aInfo.language = crawler.lang
        aInfo.title = mainSoup[0]
        aInfo.skill1 = mainSoup[3][0]
        aInfo.desp1 = mainSoup[4][0]

        # evlove
        if len(mainSoup[1]) > 1:
            aInfo.skill2 = mainSoup[3][1]
            aInfo.desp2 = mainSoup[4][1]

        aInfo.traitInfo = infoSoup[0][1]
        aInfo.classInfo = infoSoup[1][1]
        aInfo.rarityInfo = infoSoup[2][1]
        if infoSoup[3][1] == '-':
            aInfo.createInfo = 0
        else:
            aInfo.createInfo = int(infoSoup[3][1].replace(',',''))
        aInfo.liquefyInfo = infoSoup[4][1]
        if len(infoSoup) > 6:
            aInfo.cardPackInfo = infoSoup[6][1]
        else:
            aInfo.cardPackInfo = infoSoup[5][1]
        return aInfo


class CardWrapper():
    @staticmethod
    def init_tables():
        db.create_tables([Card, CardLanguageInfo, Image])
        #Image._schema.create_foreign_key(Image.card)

    @staticmethod
    def init_directory(img_path="images"):
        # create default dir
        if not os.path.isdir(img_path):
            try:
                os.mkdir(img_path)
            except OSError:
                print ("Creation of the directory %s failed" % img_path)
            else:
                print ("Successfully created the directory %s " % img_path)


    @staticmethod
    def checkNotExist(cid, lang='en'):
        if None == Card.get_or_none(card_id=cid):
            return True
        elif None == CardLanguageInfo.get_or_none(card_id=cid, language=lang):
            return True
        return False

    @classmethod
    def importFromCrawler(cls, crawler, parent=None):
        cid = crawler.cid
        # new main card
        mainCard = Card.get_or_none(card_id=crawler.cid)
        if None == mainCard:
            mainCard = Card.fromCrawler(crawler)
            mainCard.mainCard = parent
            mainCard.save(force_insert=True)

        # new lang info
        mainInfo = CardLanguageInfo.get_or_none(card_id=crawler.cid, language=crawler.lang)
        if None == mainInfo:
            mainInfo = CardLanguageInfo.fromCrawler(crawler)
            mainInfo.save(force_insert=True)

        # sub cards
        for subCrawler in crawler.relativeSoup:
            CardWrapper.importFromCrawler(subCrawler, mainCard)

