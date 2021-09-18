from peewee import *

db = SqliteDatabase('cards.db')

class Image(Model):
    #card = DeferredForeignKey('Card', null=True, field='card_id')
    filename = CharField(primary_key=True)
    imageURL = CharField() # save the URL of image
    imagePath = CharField(null=True) # save the local path of image
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
            fname = url.split('/')[-1].split('.')[0]
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
        aInfo.cardPackInfo = infoSoup[5][1]
        return aInfo


class CardWrapper():
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
        mainInfo = CardLanguageInfo.get_or_none(crawler.cid, language=crawler.lang)
        if None == mainInfo:
            mainInfo = CardLanguageInfo.fromCrawler(crawler)
            mainInfo.save()

        # sub cards
        for subCrawler in crawler.relativeSoup:
            CardWrapper.importFromCrawler(subCrawler, mainCard)


def init_tables():
    db.create_tables([Card, CardLanguageInfo, Image])
    #Image._schema.create_foreign_key(Image.card)
