from mtgsdk import Card
import pickle

data = open("cards.pkl", 'rb')
allcards = pickle.load(data)

#Fetches card metadata by name, returns the latest printing of said card
def getCard(cardname):
    for cardobj in allcards:
        if format(cardobj.name) == cardname:
            return cardobj
    return None

#Formats a title of a card (list of words, or a string) to be lowercase and hyphenated(character can be set)
def format(title):
    title = title.lower()
    return title

#Splits a dictionary of card names and frequencies into one of 7 dictionaries, depending on card type
def typesplit(cards):
    cardnames = list(cards.keys())
    categories = {}
    types = ["Creature", "Enchantment", "Artifact", "Planeswalker", "Instant", "Sorcery", "Land"]
    for type in types:
        #Complicated list comprehension here.
        #Basically it filters out all cards that are not of the chosen type, leaving only the cards of the chosen type to
        #add to the dictionary.
        typecard = [card for card in cardnames if getCard(card) and type in getCard(card).type]
        categories[type] = {}
        for card in typecard:
            categories[type][card] = cards[card]

    return categories


if __name__ == "__main__":
    print(getCard("juzam djinn").name)