from mtgsdk import Card

#Fetches card metadata by name, returns the latest printing of said card
def getCard(cardname):
    allprints = Card.where(name=cardname).all()
    return allprints[len(allprints)-1]

if __name__ == "__main__":
    print(getCard('serra angel').type)