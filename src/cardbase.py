from mtgsdk import Card
import pickle

class cardbase:

    def __init__(self, cache=None, savefile="pkl/cards.pkl"):
        self.cards = {}
        if cache:
            cache = open(cache, "rb")
            self.cards = pickle.load(cache)
        else:
            print("No card cache found. Fetching data online. This may take a while.")
            allcards = Card.all()
            for card in allcards:
                self.cards[card.name] = card
            newcache = open(savefile, "wb")
            pickle.dump(self.cards, newcache)

    def getcard(self, cardname):
        card = self.cards.get(cardname)
        if card:
            return card
        else:
            print("Card not found: " + cardname)
            return None


if __name__ == "__main__":
    test = cardbase("pkl/cards.pkl")
    print(test.getcard("Lightning Bolt").type)