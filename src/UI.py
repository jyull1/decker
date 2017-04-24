import Index
from FileImporter import importer

def welcome():
    print("Hello, and welcome to Decker, the world's best (and only) Magic: the Gathering recommender system!")
    print("First, we need to know what you've already collected.")
    collection = importer.readIn(importer.findFile())
    return