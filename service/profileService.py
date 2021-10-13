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
                 content=None,
                 public=None):
        "......"

        self.profileName = profileName
        self.author = author
        self.description = description
        self.content = content
        self.public = public

    def checkConflict(self):
        "check if the Object's name conflict with DB data"
        dbResponseR = list(db.profiles.find({"profileName": self.profileName},
                                            sort=[('_id', pymongo.DESCENDING)]))
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
                "content": dbResponse[0].get('content'),
                "public": dbResponse[0].get('public'),
                "downloadTimes": dbResponse[0].get('downloadTimes')
            }
            return resp

    @classmethod
    def downloadTimesIncrease(self,profileName):
        db.profiles.update_one({'profileName': profileName}, {"$inc": {"downloadTimes": 1}})

    @classmethod
    def downloadProfile(self, name):
        "calc timeCost"
        dbResponse = list(db.profiles.find({"profileName": name}))
        if len(dbResponse) != 1:
            return None
        else:
            self.downloadTimesIncrease(name)
            resp = {
                "_id" : str(dbResponse[0]['_id']),
                "profileName": dbResponse[0]['profileName'],
                "author": dbResponse[0]['author'],
                "description": dbResponse[0].get('description'),
                "content": dbResponse[0].get('content'),
                "public": dbResponse[0].get('public'),
                "downloadTimes": dbResponse[0].get('downloadTimes') + 1
            }
            return resp

    @classmethod
    def getProfiles(self, author):
        "get all profiles in DB"
        dbResponse = list(db.profiles.find({"$or": [{"author": author}, {"public": True}]}))
        resp = []
        for _item in dbResponse:
            _item['_id'] = str(_item['_id'])
            resp.append(_item)
        return resp

    @classmethod
    def deleteProfile(self, profileName, author):
        "calc timeCost"
        p = self.getProfile(name=profileName)
        if p:
            if p.get('author') == author:
                db.profiles.delete_one({"profileName": profileName})
                return True
            else:
                return "188011"
        return "188012"

    def save2db(self, overwrite):
        checkConflictResult = self.checkConflict()
        self.downloadTimes = 0
        if checkConflictResult == "188002":
            return db.profiles.insert_one(self.__dict__,)
        elif checkConflictResult == "188003" and overwrite:
            p = self.getProfile(self.profileName)
            return db.profiles.update_one({'_id': ObjectId(p['_id'])}, {"$set": self.__dict__})
        else:
            return None
