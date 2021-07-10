import requests
from bs4 import BeautifulSoup

urls = {
    "main": "https://shadowverse-portal.com/",
    "card": "https://shadowverse-portal.com/card/%s?lang=%s"
};

class CardCrawler:
    def __init__(self, cid, lang):
        self.cid = cid
        self.lang = lang
        self.relativeCards = []

    @property
    def mainSoup(self):
        return [self.title, self.mainImages, self.mainAbilities, self.mainSkill, self.mainDesp]

    @mainSoup.setter
    def mainSoup(self, soup):
        self.title = soup.find('h1').text.strip()
        images1 = soup.find_all("div", class_='card-main-image')
        self.mainImages = [i.img['src'] for i in images1]
        contents = soup.find_all("li", class_='card-content')
        if contents[0].find('p', class_='is-atk'):
            self.mainAbilities = [ (c.find('p', class_='is-atk').text.strip(),
                                    c.find('p', class_='is-life').text.strip()) for c in contents]
        else:
            self.mainAbilities = None

        self.mainSkill = [c.find('p', class_='card-content-skill').text.strip() for c in contents]
        self.mainDesp = [c.find('p', class_='card-content-description').text.strip() for c in contents]

    @property
    def infoSoup(self):
        return self.info;

    @infoSoup.setter
    def infoSoup(self, soup):
        self.info = {'labels':[], 'values':[]}
        contents = [li.text.replace('\r','').replace('\n','') for li in soup.ul.find_all('li')]
        self.info = [c.split(':') for c in contents ]

    @property
    def relativeSoup(self):
        #return [(card.mainSoup, card.infoSoup) for card in self.relativeCards]
        return self.relativeCards

    @relativeSoup.setter
    def relativeSoup(self, soup):
        self.relativeCards = []
        atags = soup.find_all("a", class_="el-card-detail");
        # parse <a> href
        rCard_ids = [atag['href'][6:] for atag in atags]
        # call fetchSingleCard rescurively
        for cid in rCard_ids:
            self.relativeCards.append(fetchSingleCard(cid, self.lang, isSubCard=True));

    def exportCard(self):
        return self;

def fetchSingleCard(card_id, lang='en', isSubCard=False):
    ### return the Card obj which generator by the CardCrawler::exportCard
    ###

    # init
    c = CardCrawler(card_id, lang)
    print("downloading card %s ..." % card_id)
    r = requests.get(urls['card'] % (card_id, lang))
    soup = BeautifulSoup(r.text, 'lxml')

    cardSoup = soup.find("div", class_="card")
    # fetch Main Card
    c.mainSoup = cardSoup.find("div", class_="card-main")

    # fetch Card Info
    c.infoSoup = cardSoup.find("div", class_="card-info")

    # fetch Relative Cards
    if not isSubCard:
        relativeSoup = soup.find("div", class_="card-relative")
        if relativeSoup:
            c.relativeSoup = relativeSoup

    return c

# test the Satan card
if __name__ == "__main__":
    testCard1 = fetchSingleCard(111041010);
    print(testCard1.mainSoup);
    print("--"* 20)
    print(testCard1.infoSoup);
    print("--"* 20)
    print(testCard1.relativeSoup);
