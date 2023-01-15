from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
database = client["worksheets"]


def insert_one(data, collection):
    c = database[collection]
    x = c.insert_one(data)
    return x
