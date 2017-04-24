from bs4 import BeautifulSoup
from urllib import request
import pickle
from Database import db

class deckscraper:

    def __init__(self):
        self.url = "http://sales.starcitygames.com//deckdatabase/displaydeck.php?DeckID="
        pass

    #Creates a dictionary of dictionaries of tuples (deck title & dictionary of card names : counts.
    #Uses dictionary to insert cards and deck into database
    @staticmethod
    def scrape(seed, url="http://sales.starcitygames.com//deckdatabase/displaydeck.php?DeckID=", quota=100, savefile='Decks.pkl'):
        decks = {}
        while len(decks) < quota and seed < 112595:
            deck = deckscraper.parse(url+str(seed))
            #Have to check if deck was parsed correctly; if not, deck will be None
            if deck:
                db.insertDeck(seed)
                for card in deck:
                    db.insertCard(card[0])
                    newCardID = db.lookupCard(card[0])[0]
                    deckID = db.lookupDeck_byDeckNumber(seed)[0]
                    db.insertCardToDeck(newCardID, deckID, card[1])
            seed += 1
        """
        REPLACED BY DATABASE
        save = open(savefile, 'wb')
        pickle.dump(decks, save)
        return save
        """

    #Returns HTML element that contains the deck's data; makes sure HTML is valid for parsing.
    @staticmethod
    def checkURL(url, agent='Google Chrome'):
        #Prepare request to prevent 403 errors
        req = request.Request(url)
        req.add_header('User-Agent', agent)

        #Attempts to download webpage; if it fails, it will return None
        html = BeautifulSoup(request.urlopen(req).read(), "html.parser")
        deck = html.find("div", class_="deck_listing2")
        return deck

    #Returns a list of touples with card names (tokens) and frequencies from a StarcityGames URL.
    @staticmethod
    def parse(url):
        deckHTML = deckscraper.checkURL(url)
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
                    card = deckscraper.format(card)
                    if card != '':
                        decklist[card] = numcopies

            return [deckname, decklist]
        else:
            return None

    #Formats a title of a card (list of words, or a string) to be lowercase and hyphenated(character can be set)
    @staticmethod
    def format(title, char='-'):
        if type(title) is str:
            title = title.split()
        title = char.join(title).lower()
        return title

if __name__ == "__main__":
    deckscraper.scrape(50000, quota=100)
