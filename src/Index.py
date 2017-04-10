from Scraper import deckscraper
import FileImporter
import pickle

class Index:

    def __init__(self, data='Decks.pkl'):
        #Loads deck database info
        try:
            deckdata = open('Decks.pkl', 'rb')
            self.deckdata = pickle.load(deckdata)
        except FileNotFoundError as e:
            print(e)
            #A seed of 55000 is chosen because it begins in mid-2014, a relative turning point in MTG
            deckdata = deckscraper.scrape(55000, quota=500, savefile='DecksImprov.pkl')
            self.deckdata = pickle.load(deckdata)

        #Loads personal collection info
        self.collection = FileImporter.readIn('myCollection.csv')



    def find(self, quota=10):
        print(self.collection)
        for deck in self.deckdata:
            if self.compare(self.deckdata[deck][1]):
                print(self.deckdata[deck])
                quota -= 1
                if quota == 0:
                    return


    def compare(self, deck):
        for card in deck:
            if not self.collection.get(card):
                return False
            if int(self.collection[card]) < int(deck[card]):
                print("You don't have enough of this card:")
                print(card)
                print(str(self.collection[card]) + str(deck[card]))
                return False
        return True


if __name__ == "__main__":
    index = Index()
    index.find(quota=20)

