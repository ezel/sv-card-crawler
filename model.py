from peewee import *

db = SqliteDatabase('cards.db')

class Card(Model):
    cid = CharField()
    language = CharField()

    title = CharField()

    imageURL1 = CharField() # save the URL of image
    imageURL2 = CharField(null=True)

    imageLink1 = CharField(null=True) # save the local link of image
    imageLink2 = CharField(null=True)

    # main abilities
    Atk1 = IntegerField(null=True)
    HP1 = IntegerField(null=True)
    Atk2 = IntegerField(null=True)
    HP2 = IntegerField(null=True)

    # cost not on page
    minCost = IntegerField(null=True)

    skill1 = TextField()
    skill2 = TextField(null=True)
    desp1 = TextField()
    desp2 = TextField(null=True)

    # info
    traitInfo = CharField()
    classInfo = CharField()
    rarityInfo = CharField()
    createInfo = CharField()
    liquefyInfo = CharField()
    cardPackInfo = CharField()

    # the relative card have a main card (parent)
    mainCard = ForeignKeyField('self', backref='subCards', null=True)

    class Meta:
        database = db
        indexes = (
            (('cid', 'language'), True),
        )

    @staticmethod
    def checkNotExist(cid, lang='en'):
        if None == Card.get_or_none(cid=cid, language=lang):
            return True
        return False

    @classmethod
    def createFromCrawler(cls, crawler, parent=None):
        # inner function to match card data from crawler warpper
        def newMainCard(cls, crawler):
            # get card soup
            mainSoup = crawler.mainSoup
            infoSoup = crawler.infoSoup

            # init main card
            mainCard = cls(cid=crawler.cid, language=crawler.lang)
            mainCard.title = mainSoup[0]
            mainCard.imageURL1 = mainSoup[1][0]
            if mainSoup[2]:
                mainCard.Atk1, mainCard.HP1 = mainSoup[2][0]
            mainCard.skill1 = mainSoup[3][0]
            mainCard.desp1 = mainSoup[4][0]

            # evlove card
            if len(mainSoup[1]) > 1:
                mainCard.imageURL2 = mainSoup[1][1]
                mainCard.Atk2, mainCard.HP2 = mainSoup[2][1]
                mainCard.skill2 = mainSoup[3][1]
                mainCard.desp2 = mainSoup[4][1]

            mainCard.traitInfo = infoSoup[0][1]
            mainCard.classInfo = infoSoup[1][1]
            mainCard.rarityInfo = infoSoup[2][1]
            mainCard.createInfo = infoSoup[3][1]
            mainCard.liquefyInfo = infoSoup[4][1]
            mainCard.cardPackInfo = infoSoup[5][1]
            return mainCard;

        # new main card
        mainCard = newMainCard(cls, crawler)
        mainCard.mainCard = parent

        # if not exist , create mainCard
        if None == Card.get_or_none(cid=mainCard.cid, language=mainCard.language):
            mainCard.save()

            # sub cards
            for subCrawler in crawler.relativeSoup:
                Card.createFromCrawler(subCrawler, mainCard)

        return mainCard

def init_tables():
    db.create_tables([Card])

# main test
if __name__ == "__main__":
    SqliteDatabase('cards.db').create_tables([Card])
