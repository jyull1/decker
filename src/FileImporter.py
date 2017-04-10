import csv
import os
from Scraper import deckscraper

def readIn(filename):
    '''
    reads a csv given csv file and writes contents to a dictionary, accounting for multiple entries of the same card
    :param filename: filepath to a csv file
    :return: collection: dictionary of {cardName:quantity} pairs
    '''
    collection = dict()
    f = csv.reader(open(filename, 'r'), delimiter=',')
    place = 0
    for item in f:
        cardName = deckscraper.format(item[0])
        quantity = item[1]
        #Checks if the quantity read is null
        if quantity:
            if cardName not in collection:
                collection[cardName] = int(quantity)
            else:
                collection[cardName] += int(quantity)
    return collection

if __name__ == "__main__":
    path = os.path.abspath("test.csv").replace("/src", "")
    cardIdx = print(readIn(path))