from mtgsdk import Card

#Fetches card metadata by name, returns the latest printing of said card
def getCard(cardname):
    allprints = Card.where(name=cardname).all()
    return allprints[len(allprints)-1]

#Formats a title of a card (list of words, or a string) to be lowercase and hyphenated(character can be set)
def makeslug(title, char='-'):
    if type(title) is str:
        title = title.split()
    title = char.join(title).lower()
    return title

if __name__ == "__main__":
    print(getCard('serra angel').type)