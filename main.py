from listCrawler import getCardList
from cardCrawler import fetchSingleCard
from model import Card

if __name__ == "__main__":
    lang = 'en'
    currentList = getCardList(3, forceFetch=True)
    for cid in currentList:
        if Card.checkNotExist(cid, lang):
            currentCard = fetchSingleCard(cid)
            newCard = Card.createFromCrawler(currentCard)
