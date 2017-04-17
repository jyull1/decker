import csv
import os
from os.path import join, expanduser
from Scraper import deckscraper

'''
searches all directories on hard drive for a given file
:return: full file path to the given file
'''
def findFile():
    foundFiles = []
    file = input("Name of collection file: ")
    print('searching...')
    for root, dirs, files in os.walk(expanduser("~/")):
        # print(dirs)
        if file in files:
            print('found file')
            path = join(root, file)
            foundFiles.append(path)
    if len(foundFiles) == 0:
        print("No files found.")
        filepath = findFile()
    elif len(foundFiles) > 1:
        print(str(len(foundFiles))+" files found.")
        for x in range(len(foundFiles)):
            print(str(x+1)+": "+foundFiles[x])
        choice = int(input("Choose a file: ")) - 1
        filepath = foundFiles[choice]
    else:
        filepath = foundFiles[0]
        print("Using "+filepath)
    return filepath

'''
reads a csv given csv file and writes contents to a dictionary, accounting for multiple entries of the same card
:param filename: filepath to a csv file
:return: collection: dictionary of {cardName:quantity} pairs
'''
def readIn(filename):
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
    cardIdx = readIn(findFile())
    print(cardIdx)