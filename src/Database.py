import sqlite3
import cardmanager

class db(object):
    def __init__(self, dbfile):
        self.dbfile = dbfile
        self.connection = sqlite3.connect(dbfile)
        self.cursor = self.connection.cursor()

        self.execute("""CREATE TABLE IF NOT EXISTS Deck (
                                 id  INTEGER PRIMARY KEY,
                                 deckNumber INTEGER,
                                 name VARCHAR, 
                                 isSideboard INTEGER,
                                 sideboardID INTEGER
                            );""")

        self.execute("""CREATE TABLE IF NOT EXISTS Card (
                                 id  INTEGER PRIMARY KEY,
                                 formattedName VARCHAR,
                                 name VARCHAR
                            );""")

        self.execute("""CREATE TABLE IF NOT EXISTS CardToDeck (
                                 id  INTEGER PRIMARY KEY,
                                 cardID INTEGER,
                                 deckID INTEGER,
                                 quantity INTEGER
                            );""")

    def execute(self, sql):
        res = self.cursor.execute(sql)
        self.connection.commit()

        return res

    def insertDeck(self, deckNumber, name=""):
        duplicate = self.lookupDeck_byDeckNumber(deckNumber)
        if duplicate is not None:
            return duplicate

        sql = """INSERT INTO Deck (deckNumber, name, isSideboard, sideboardID) VALUES ('%d','%s', 0, -1)""" % (deckNumber, name)

        res = self.execute(sql)
        self.insertSideboard(deckNumber)
        return self.cursor.lastrowid

    def insertSideboard(self, deckNo):
        deckInfo = self.lookupDeck_byDeckNumber(deckNo)

        sql = """INSERT INTO Deck (deckNumber, name, isSideboard, sideboardID) VALUES ('%d','%s',1, -1)""" % (deckNo, deckInfo[1])
        res = self.execute(sql)

        sql = """UPDATE Deck SET sideboardID='%d' WHERE deckNumber='%d' AND isSideboard=0""" % (self.lookupSideboardID_byDeckNumber(deckNo)[0], deckNo)
        res = self.execute(sql)

        return self.cursor.lastrowid

    def lookupDeck_byID(self, id):
        sql = "SELECT * FROM Deck WHERE id='%d'" % (id)
        res = self.execute(sql)
        reslist = res.fetchall()
        if not reslist:
            return None
        else:
            return reslist[0]

    def lookupDeck_byDeckNumber(self, deckNumber):
        sql = "SELECT id from Deck WHERE deckNumber='%d' AND isSideboard=0" % (deckNumber)
        res = self.execute(sql)
        reslist = res.fetchall()
        if not reslist:
            return None
        elif len(reslist > 1):
            raise RuntimeError('DB: constraint failure on Deck')
        else:
            return reslist[0]

    def lookupSideboardID_byDeckNumber(self, deckNumber):
        sql = """SELECT id from Deck WHERE deckNumber='%d' AND isSideboard=1""" % (deckNumber)
        res = self.execute(sql)
        reslist = res.fetchall()
        if not reslist:
            return None
        elif len(reslist > 1):
            raise RuntimeError('DB: constraint failure on Deck')
        else:
            return reslist[0]

    def insertCard(self, name):
        card_id = self.lookupCard(name)
        if card_id is not None:
            return card_id

        sql = """INSERT INTO Card (formattedName, name) VALUES ('%s','%s')""" % (cardmanager.makeslug(name), name)

        res = self.execute(sql)
        return self.cursor.lastrowid

    def lookupCard(self, name):
        sql = "SELECT id FROM Card WHERE name='%s'" % (name)
        res = self.execute(sql)
        reslist = res.fetchall()
        if not reslist:
            return None
        elif len(reslist > 1):
            raise RuntimeError('DB: constraint failure on Card')
        else:
            return reslist[0]

    def insertCardToDeck(self, cardID, deckID, quantity):
        c2dID = self.lookupCardToDeck(cardID, deckID)
        if c2dID is not None:
            currQuantity = self.lookupQuantity(cardID, deckID)
            sql = """UPDATE CardToDeck SET quantity='%d' WHERE cardID='%d' AND deckID='%d'""" % (currQuantity+quantity, cardID, deckID)
        else:
            sql = """INSERT INTO CardToDeck (cardID, deckID, quantity) VALUES ('%d', '%d', '%d')""" % (cardID, deckID, quantity)

        res = self.execute(sql)
        return self.cursor.lastrowid

    def lookupCardToDeck(self, cardID, deckID):
        sql = "SELECT * FROM CardToDeck WHERE cardID='%d' AND deckID='%d'" % (cardID, deckID)
        res = self.execute(sql)
        reslist = res.fetchall()
        if not reslist:
            return None
        elif len(reslist > 1):
            raise RuntimeError('DB: constraint failure on Card')
        else:
            return reslist[0]

    def lookupQuantity(self, cardID, deckID):
        sql = """SELECT quantity from CardToDeck WHERE cardID='%d' AND deckID='%d'""" % (cardID, deckID)
        res = self.execute(sql)
        reslist = res.fetchall()
        if not reslist:
            return None
        elif len(reslist > 1):
            raise RuntimeError('DB: constraint failure on CardToDeck')
        else:
            return reslist[0][0]

    @staticmethod
    def insertFromScrape(deck, deckNo, isSideboard):
        if isSideboard:
            db.insertSideboard(deckNo)
        else:
            db.insertDeck(deckNo)
        for card in deck:
            db.insertCard(card[0])
            newCardID = db.lookupCard(card[0])[0]
            deckID = db.lookupDeck_byDeckNumber(deckNo)[0]
            db.insertCardToDeck(newCardID, deckID, card[1])

if __name__ == '__main__':
    db = db('test.db')