import cardmanager
from CardMatrix import CardMatrix
from Scraper import deckscraper
from FileImporter import importer
import pickle
import operator
import cardmanager

class Index:

    def __init__(self, data='Decks.pkl', collection='myCollection.csv'):
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
        self.matrix = CardMatrix("matrix.pkl")
        print("Matrix calculated.")

    def idf(self, decks):
        inversedf = {}
        for deck in decks:
            for card in decks[deck][1]:
                if not inversedf.get(card):
                    inversedf[card] = 1
                else:
                    inversedf[card] += 1
        for card in inversedf:
            inversedf[card] = 1/inversedf[card]

        return inversedf

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

    def compare(self, deck):
        for card in deck:
            if not self.collection.get(card):
                #print("Card missing: ", card)
                return False
            if int(self.collection[card]) < int(deck[card]):
                #print("Not enough of card: ", card, self.collection[card], deck[card])
                return False
        return True

    @staticmethod
    def format(deck, id, title, numbering=0):
        head = str(numbering) + ".)\nMatch found: " + title + "(" + deckscraper().url + str(id) + ")\n\n"
        list = ""
        # print(deck)
        for card in deck:
            list += card + "\t" + deck[card] + "\n"

        return head+list+"________________________________________"

    def subset(self, card):
        containscard = {}
        for deck in self.deckdata:
            if card in self.deckdata[deck][1]:
                containscard[deck] = self.deckdata[deck]

        return containscard

    #board indicates whether it is in the mainboard or sideboard; 1 is mainboard, 2 is sideboard
    def rank(self, card, board=1, onlycollection=False):
        print("Rankings results for " + card)
        card = cardmanager.format(card)
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

    def rank2(self, searchcard, board=1, onlycollection=False):
        print("Rankings results for " + searchcard)
        searchcard = cardmanager.format(searchcard)
        cardrankings = {}
        for deck in self.deckdata:
            for card in self.deckdata[deck][board]:
                if card not in cardrankings:
                    cardrankings[card] = self.matrix.cosine(searchcard, card)

        if onlycollection:
            listdel = []
            for card in cardrankings:
                if card not in self.collection:
                    listdel.append(card)
            for card in listdel:
                del cardrankings[card]

        return cardrankings


    @staticmethod
    def order(cards):
        print("Sorting results...")
        sortedcards = sorted(cards.items(), key=operator.itemgetter(1), reverse=True)
        return sortedcards

    #Takes dictionary of 7 dictionaries (one for each card type) and prints a formatted string
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
    print(Index.formatcards(index.rank2("Ajani Steadfast", onlycollection=True), splittype=True))

