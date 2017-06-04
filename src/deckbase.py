import pickle
from deck import deck

class deckbase:

    def __init__(self):
        self.alldecks = {}

    #Creates a pickle file version of the current set of decks in alldecks.
    #'filename' is a String that will function as the name of the save file.
    #'path' not currently implemented, however it would indicate where the file is to be saved.
    def save(self, filename="deckbase.pkl", path="pkl/"):
        savefile = open(path+filename, "wb")
        pickle.dump(self.alldecks, savefile)

        return savefile

    #Loads a saved deckbase
    def load(self, path):
        loadfile = open(path, 'rb')
        self.alldecks = pickle.load(loadfile)

        return loadfile

    #Adds a deck object to the deckbase, using its url as a key
    #CAUTION! - Overwrites the deck that was there previously, if at all.
    def add(self, url, deckobj):
        self.alldecks[url] = deckobj

