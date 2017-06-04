import math
import operator
import pickle

from CardMatrix import CardMatrix
from FileImporter import importer
from Scraper import deckscraper

from unused import cardmanager


#Data structure containing deck metadata and frequencies, personal collections, and the associated methods required to
#make determinations on that data.
#See Index.txt for object template examples.
class Index:

    #Constructor
    #data (String) -> Pickle file created by Scraper.py, containing deck names, included cards, and card frequencies.
    #collection (String) -> CSV file containing cards and card counts from a user's collection.
    def __init__(self, data='pkl/Decks.pkl', collection='myCollection.csv'):
        imp = importer()
        #Loads deck database info
        try:
            deckdata = open(data, 'rb')
            self.deckdata = pickle.load(deckdata)
        except FileNotFoundError as e:
            print(e)
            #A seed of 55000 is chosen because it begins in mid-2014, a relative turning point in MTG
            deckdata = deckscraper.scrape(55000, quota=500, savefile='DecksImprov.pkl')
            self.deckdata = pickle.load(deckdata)

        #Loads personal collection info
        self.collection = importer().readIn(collection)

        print("Calculating card vectors...")
        self.matrix = CardMatrix("pkl/matrix.pkl")
        print("Matrix calculated.")

    #Calculates IDF scores for all cards in all decks.
    #This goes unused because incredibly common cards are arguably *more* important than cards with few uses.
    #Returns a dictionary of {cardname : idf score}

    #decks (Dict) -> Dictionary of {deckIDs : deckdata(see Data Structure Docs.txt)}
    def idf(self, decks):
        print("Calculating card IDFs")
        inversedf = {}
        numdecks = len(decks)
        for deck in decks:
            for card in decks[deck][1]:
                if not inversedf.get(card):
                    inversedf[card] = 1
                else:
                    inversedf[card] += 1
        for card in inversedf:
            inversedf[card] = math.log10(numdecks/inversedf[card])

        return inversedf

    #Finds all decks in the index that match the uploaded collection.
    #Returns nothing, prints results directly to console.

    #quota (Int) -> The number of decks to be found before find quits out.
    def find(self, quota=10):
        # print(self.collection)
        # print(len(self.deckdata))
        results = 1
        for deck in self.deckdata:
            if self.compare(self.deckdata[deck][1]):
                print(Index.format(self.deckdata[deck][1], deck, self.deckdata[deck][0], numbering=results))
                results += 1
                quota -= 1
                if quota == 0:
                    return

        # print(iterations)

    #Determines if a deck is a subset of a player's collection, i.e. buildable from what is already owned.
    #Returns a Boolean

    #deck(Dict) -> Dictionary of {deckID : deckdata(see Data Structure Docs.txt)}
    def compare(self, deck):
        for card in deck:
            if not self.collection.get(card):
                #print("Card missing: ", card)
                return False
            if int(self.collection[card]) < int(deck[card]):
                #print("Not enough of card: ", card, self.collection[card], deck[card])
                return False
        return True

    #Basically a toString for a deck
    #Returns a string formatted to be displayed to a user.

    #deck(Dict) -> Dictionary of {deckID : deckdata(see Data Structure Docs.txt)}
    #id(Int) -> id of the deck in its url listing at Starcitygames
    #title(String) -> Title of the deck, as scraped.
    @staticmethod
    def format(deck, id, title, numbering=0):
        head = str(numbering) + ".)\nMatch found: " + title + "(" + deckscraper().url + str(id) + ")\n\n"
        list = ""
        # print(deck)
        for card in deck:
            list += card + "\t" + deck[card] + "\n"

        return head+list+"________________________________________"

    #Takes a cardname and returns a subset of all decks containing that card.
    #Returned deck is a deck index (see Data Structure Docs.txt)
    def subset(self, card):
        containscard = {}
        for deck in self.deckdata:
            if card in self.deckdata[deck][1]:
                containscard[deck] = self.deckdata[deck]

        return containscard

    #Takes a cardname and returns a dictionary of cards with relevance scores.
    #Bases scores on co-occurrence with supplied card.
    #board indicates whether it is in the mainboard or sideboard; 1 is mainboard, 2 is sideboard
    def rank(self, card, board=1, onlycollection=False):
        print("Rankings results for " + card)
        card = cardmanager.format(card)
        #contains card names to card appearances
        cardrankings = {}
        for deck in self.subset(card):
            for card in self.deckdata[deck][board]:
                if card in cardrankings:
                    cardrankings[card] += 1
                else:
                    cardrankings[card] = 1

        if onlycollection:
            listdel = []
            for card in cardrankings:
                if card not in self.collection:
                    listdel.append(card)
            for card in listdel:
                del cardrankings[card]

        return cardrankings

    # Takes a cardname and returns a dictionary of cards with relevance scores.
    #Bases scores on cosine similarity of cards to other cards
        #Calls CardMatrix to determine card vectors & cosine similarity.
    def cosinerank(self, searchcard, board=1, onlycollection=False):

        cardidfs = self.idf(self.deckdata)

        searchcard = cardmanager.format(searchcard)
        cardrankings = {}
        print("Determining Cosine Similarity Scores for " + searchcard)
        for deck in self.deckdata:
            for card in self.deckdata[deck][board]:
                if card not in cardrankings:
                    cardrankings[card] = self.matrix.cosine(searchcard, card, idf1=cardidfs[searchcard], idf2=cardidfs[card])

        if onlycollection:
            listdel = []
            for card in cardrankings:
                if card not in self.collection:
                    listdel.append(card)
            for card in listdel:
                del cardrankings[card]

        return cardrankings

    #Orders a dictionary of cards by their relevancy scores.
    #Returns a list of tuples of (cardname : card relevancy) sorted by card relevancy

    #cards(Dict) -> dictionary of {card names : relevancy score}
    @staticmethod
    def order(cards):
        print("Sorting results...")
        sortedcards = sorted(cards.items(), key=operator.itemgetter(1), reverse=True)
        return sortedcards

    #Takes dictionary of 7 dictionaries (one for each card type) and returns a formatted string for user results
    @staticmethod
    def formatcards(cardrankings, splittype=True):
        output = ""
        #Chooses 200 most "relevant' cards
        cardrankings = dict(Index.order(cardrankings)[0:201])
        if splittype:
            cardrankings = cardmanager.typesplit(cardrankings)
            types = ["Creature", "Enchantment", "Artifact", "Planeswalker", "Instant", "Sorcery", "Land"]
            for type in types:
                ranking = 1
                output += type + ":\n###############################################\n"
                for card in Index.order(cardrankings[type]):
                    output += str(ranking) + ". " + card[0] + "\n\n"
                    ranking += 1

        else:
            ranking = 1
            for card in Index.order(cardrankings):
                output += str(ranking) + ". " + card[0] + "\n\n"
                ranking += 1

        return output


if __name__ == "__main__":
    index = Index(collection='myCollection.csv')
    #print(Index.formatcards(index.rank("jace, the living guildpact", onlycollection=True), splittype=True))
    index.find(quota=1000)

