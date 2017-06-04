from mtgsdk import Card
import pickle

data = open("pkl/cards.pkl", 'rb')
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
        categories[type] = {}

    for card in cards:
        #the card object is pulled down separately in case the card to be fetched has no associated data
        truecard = getCard(card)
        if truecard:
            cardtype = truecard.type
            for type in types:
                if type in cardtype:
                    categories[type].update({card : cards[card]})

    return categories


if __name__ == "__main__":
    print(getCard("ajani steadfast").name)