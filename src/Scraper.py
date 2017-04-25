from bs4 import BeautifulSoup
from urllib import request
import pickle
from Database import db
import cardmanager

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
                db.insertFromScrape(deck, seed, False)
                db.insertFromScrape(deck[2], seed, True)
            seed += 1

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
            sideboard = {}
            deckdivs = deckHTML.find_all("ul")
            for div in deckdivs:
                cards = div.find_all("li")
                #Writes to the sideboard dictionary if it is contained in the sideboard div.
                #Sideboards have less impact on the way the deck plays, so they are stored separately.
                if deckHTML.find("div", class_="deck_sideboard") in div.parents:
                    deckscraper.store(cards, sideboard)
                else:
                    deckscraper.store(cards, decklist)

            return [deckname, decklist, sideboard]
        else:
            return None

    #Converts a list of <li> HTML tags into a dictionary of cards to frequency data (i.e. {cardname : x}).
    @staticmethod
    def store(cards, dict):
        for card in cards:
            card = card.get_text().split()
            numcopies = card[0]
            card = card[1:]
            card = cardmanager.makeslug(card)
            if card != '':
                dict[card] = numcopies

if __name__ == "__main__":
    deckscraper.scrape(50000, quota=10, savefile="decks2.pkl")
