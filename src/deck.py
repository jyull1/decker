

class deck:

    def __init__(self):
        self.mainboard = {}
        self.sideboard = {}

    #Adds a card entry to the deck of the following format:
        #"Serra Angel": (<Serra Angel Card Object>, 4)
    def addtodeck(self, count, cardobj, mainboard=True):
        if mainboard:
            self.mainboard[cardobj.name] = (cardobj, count)

if __name__ == "__main__":
    test = deck()