import csv
import os

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
        cardName = item[0]
        quantity = item[1]
        if cardName not in collection:
            collection[cardName] = quantity
        else:
            collection[cardName] += quantity
    return collection

if __name__ == "__main__":
    path = os.path.abspath("test.csv").replace("/src", "")
    cardIdx = readIn(path)