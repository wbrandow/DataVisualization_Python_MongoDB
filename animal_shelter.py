# Author: William Brandow
# Date: 2023-02-09

from pymongo import MongoClient
from bson.objectid import ObjectId

class AnimalShelter:
    """ CRUD operations in MongoDB """

    def __init__(self, username, password):
        # initialize the MongoClient
        self.client = MongoClient('mongodb://%s:%s@localhost:27115/AAC' % (username, password))
        self.database = self.client['AAC']

    def create(self, data):
        if data is not None:
            self.database.animals.insert(data)  # data must be a dictionary
            return True

        else:
            raise Exception('Nothing to save, because data parameter is empty')
            return False

    def read(self, data={}):
        return self.database.animals.find(data, {"_id": False})

    def update(self, data, newData, upsertValue=False):
        if data is not None:

            if upsertValue == True:
                result = self.database.animals.update_one(data, {'$set': newData}, upsert=True)
            else:
                result = self.database.animals.update_one(data, {'$set': newData}, upsert=False)

            return result.raw_result

        else:
            raise Exception('Missing data argument')

    def delete(self, data):
        if data is not None:
            result = self.database.animals.delete_one(data)
            return result.raw_result
        else:
            raise Exception('Missing data argument')
