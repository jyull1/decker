from bs4 import BeautifulSoup
from urllib import request
import pickle
from Database import db

import cardmanager

class deckscraper:

    def __init__(self, data='C:/Users/Joseph/Desktop/decks.db'):
        self.url = "http://sales.starcitygames.com//deckdatabase/displaydeck.php?DeckID="
        #self.database = db(data)
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
                decks[seed] = deckscraper.parse(url+str(seed))
                print(decks[seed])
                #self.database.insertFromScrape(deck, seed)
            seed += 1

        save = open(savefile, 'wb')
        pickle.dump(decks, save)
        return save

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
        if deckHTML:
            deckname = deckHTML.find("a").get_text()
            decklist = {}
            sideboard = {}
            decklistNF = {}
            sideboardNF = {}
            deckdivs = deckHTML.find_all("ul")
            for div in deckdivs:
                cards = div.find_all("li")
                #Writes to the sideboard dictionary if it is contained in the sideboard div.
                #Sideboards have less impact on the way the deck plays, so they are stored separately.
                if deckHTML.find("div", class_="deck_sideboard") in div.parents:
                    deckscraper.store(cards, sideboard)
                    deckscraper.store(cards, sideboardNF, False)
                else:
                    deckscraper.store(cards, decklist)
                    deckscraper.store(cards, decklistNF, False)

            return [deckname, decklist, sideboard]
        #, decklistNF, sideboardNF
        else:
            return None

    #Converts a list of <li> HTML tags into a dictionary of cards to frequency data (i.e. {cardname : x}).
    @staticmethod
    def store(cards, dict, formatted=True):
        for card in cards:
            card = card.get_text().split()
            numcopies = card[0]
            card = cardmanager.format(" ".join(card[1:]))

            if card != '':
                dict[card] = numcopies

if __name__ == "__main__":
    scraper = deckscraper()
    scraper.scrape(25000, quota=1, savefile="decks2.pkl")
