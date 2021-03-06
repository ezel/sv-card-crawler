import requests
from bs4 import BeautifulSoup
import pickle

urls = {
    "main" : 'https://shadowverse-portal.com',
    "home" : 'https://shadowverse-portal.com/',
    "list" : 'https://shadowverse-portal.com/cards?format=%s&lang=%s',
}
cardsFileName = 'list.tmp'

def fetchAndSaveCardList(format=1, lang='en'):
    ### fetch Card List from Homepage
    # use the next page, so this function should be IO blocking
    ### format: 1: Rotation, 3: Unlimited
    ### lang: same as card
    cardIDList = []

    firstURL = urls['list'] %(format, lang)
    cardIDList, nextURL = fetchCardListOfURL(firstURL)
    while(nextURL):
        curList, nextURL = fetchCardListOfURL(nextURL)
        cardIDList.extend(curList);

    with open(cardsFileName, 'wb') as f:
        pickle.dump(cardIDList, f)

    return cardIDList

def getCardList(format=1, lang='en', forceFetch=False):
    # force fetch the latest from web
    if forceFetch:
        return fetchAndSaveCardList(format, lang)

    # fetch from local first, more for testing
    cards = [];
    try:
        with open(cardsFileName, 'rb') as f:
            cards = pickle.load(f)
    except FileNotFoundError:
        pass

    if len(cards) < 1:
        cards = fetchAndSaveCardList(format, lang)

    return cards

def fetchCardListOfURL(url):
    ### parameter: current URL
    ### return: ( card_list, next_page_url )
    r = requests.get(url)
    print("Downloading... %s" % url)
    soup = BeautifulSoup(r.text, 'lxml')

    # get card id list of current page
    cardsVisualSoup = soup.find(id="displayVisual")
    cardsSoup = cardsVisualSoup.find_all("a", class_="el-card-visual-content")
    cardList = [ cardATag['href'][6:] for cardATag in cardsSoup ]

    # find next
    paginationSoup = soup.find("div", class_="bl-pagination")
    nextHref = [ span.a['href'] for span in paginationSoup.find_all('span') if 'is-next' in span['class']]
    if len(nextHref) > 0:
        nextURL = urls['main'] + nextHref[0]
    else:
        nextURL = None
    return cardList, nextURL

if __name__ == "__main__":
    cards = getCardList(1)
    print(len(cards))
