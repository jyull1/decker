from bs4 import BeautifulSoup
from urllib import request

class Scraper:

    def __init__(self):
        self.url = "http://sales.starcitygames.com//deckdatabase/displaydeck.php?DeckID=112239"
        pass

    #Returns an array of arrays of card names (tokens) from a "seed" integer
    def scrape(self, seed):
        pass

    #Returns HTML element that contains the deck's data; makes sure HTML is valid for parsing.
    def checkURL(self, url, agent='Google Chrome'):
        #Prepare request to prevent 403 errors
        req = request.Request(url)
        req.add_header('User-Agent', agent)

        #Attempts to download webpage; if it fails, it will return None
        html = BeautifulSoup(request.urlopen(req).read(), "html.parser")
        deck = html.find("div", class_="deck_listing2")
        return deck

    #Returns a list of touples with card names (tokens) and frequencies from a StarcityGames URL.
    def parse(self, url):
        deckHTML = self.checkURL(url)
        #print(deckHTML.prettify())
        if deckHTML:
            deckname = deckHTML.find("a").get_text()
            decklist = {}
            deckdivs = deckHTML.find_all("ul")
            for div in deckdivs:
                cards = div.find_all("li")
                for card in cards:
                    card = card.get_text().split()
                    numcopies = card[0]
                    card = card[1:]
                    card = self.format(card)

                    decklist[card] = numcopies
            return decklist
        else:
            return False

    #Formats a title of a card (list of words) to be lowercase and hyphenated
    def format(self, title, char='-'):
        title = char.join(title).lower()
        return title

if __name__ == "__main__":
    scraper = Scraper()
    print(scraper.parse(scraper.url))
