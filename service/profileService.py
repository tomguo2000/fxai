from dbconfig import db
from common.timeUtils import Timeutils
from common.setlog2 import logger
import time
import pymongo
from bson import ObjectId
import json

class ProfileService(object):
    def __init__(self, profileName,
                 author=None,
                 description=None,
                 content=None):
        "......"

        self.profileName = profileName
        self.author = author
        self.description = description
        self.content = content

    def checkConflict(self):
        "check if the Object's name conflict with DB data"
        dbResponseR = list(db.profiles.find({"$and": [{"author": self.author},
                                                      {"profileName": self.profileName}
                                                      ]
                                             }, sort=[('_id', pymongo.DESCENDING)]))
        if len(dbResponseR) > 1:
            raise Exception("00000")
        elif len(dbResponseR) == 1 and dbResponseR[0].get('author') != self.author:
            return "188004"
        elif len(dbResponseR) == 1 and dbResponseR[0].get('author') == self.author:
            return "188003"
        else:
            return "188002"


    @classmethod
    def getProfile(self, name):
        "calc timeCost"
        dbResponse = list(db.profiles.find({"profileName": name}))
        if len(dbResponse) != 1:
            return None
        else:
            # self._id = str(dbResponse[0]['_id'])
            # self.profileName = dbResponse[0]['profileName']
            # self.author = dbResponse[0]['author']
            # self.description = dbResponse[0].get('description')
            # self.content = dbResponse[0].get('content')
            resp = {
                "_id" : str(dbResponse[0]['_id']),
                "profileName": dbResponse[0]['profileName'],
                "author": dbResponse[0]['author'],
                "description": dbResponse[0].get('description'),
                "content": dbResponse[0].get('content')
            }
            return resp


    @classmethod
    def getProfiles(self):
        "get all profiles in DB"
        dbResponse = list(db.profiles.find())
        resp = []
        for _item in dbResponse:
            _item['_id'] = str(_item['_id'])
            resp.append(_item)
        return resp

    def finish(self):
        "calc timeCost"
        self.timeCost = int(time.time()*1000) - self.beginTime
        self.request = str(self.request)
        self.response = str(self.response)

    def save2db(self, overwrite):
        checkConflictResult = self.checkConflict()
        if checkConflictResult == "188002":
            return db.profiles.insert_one(self.__dict__)
        elif checkConflictResult == "188003" and overwrite:
            p = self.getProfile(self.profileName)
            return db.profiles.update_one({'_id': ObjectId(p['_id'])}, {"$set": self.__dict__})
        else:
            return None
