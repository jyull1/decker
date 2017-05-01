import math
import pickle

class CardMatrix:

    #Computes a matrix (or rather, a dictionary) of vectors for each card
    def __init__(self, deckdata):
        self.vectors = {}

        #if deckdata is a filename
        if isinstance(deckdata, str):

            try:
                deckdata = open(deckdata, 'rb')
                self.vectors = pickle.load(deckdata)
            except FileNotFoundError:
                print("Apologies, we couldn't find the file " + deckdata)
        #otherwise it is an Index data structure
        else:
            self.vectors = {}

            #for every deck recorded
            for deck in deckdata:
                #for every card in the deck
                for card1 in deckdata[deck][1]:
                    #Make a new vector for the card if the card is new
                    if not self.vectors.get(card1):
                        self.vectors[card1] = {card1 : 0}
                    #for every card in the deck of that card
                    for card2 in deckdata[deck][1]:
                        if not self.vectors[card1].get(card2):
                            self.vectors[card1][card2] = 1
                        else:
                            self.vectors[card1][card2] += 1
            savedata = open("matrix.pkl", "wb")
            pickle.dump(self.vectors, savedata)



    def distance(self, card1, card2):
        cards = set(list(self.vectors[card1].keys()) + list(self.vectors[card2].keys()))
        sum = 0
        for card in cards:
            p = self.vectors[card1].get(card) or 0
            q = self.vectors[card2].get(card) or 0

            sum += (p-q)**2

        return math.sqrt(sum)

    def cosine(self, card1, card2):
        cards = set(list(self.vectors[card1].keys()) + list(self.vectors[card2].keys()))
        dotproduct = 0
        card1length = 0
        card2length = 0

        for card in cards:
            p = self.vectors[card1].get(card) or 0
            q = self.vectors[card2].get(card) or 0

            dotproduct += p*q
            card1length += p**2
            card2length += p**2

        card1length = math.sqrt(card1length)
        card2length = math.sqrt(card1length)

        return dotproduct/(card1length*card2length)

    def toString(self):
        return str(self.vectors)

if __name__ == "__main__":
    pass