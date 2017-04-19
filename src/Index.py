from Scraper import deckscraper
import FileImporter
import pickle

class Index:

    def __init__(self, data='Decks.pkl', collection='myCollection.csv'):
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
        self.collection = FileImporter.readIn(collection)

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


if __name__ == "__main__":
    index = Index(collection='myCollection.csv')
    # print("Deck 111239:")
    # print(index.deckdata[111239])
    # index.compare(index.deckdata[111239][1])
    index.find(quota=200)

