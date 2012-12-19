'''
Created on 14.12.2012

@author: tmaul
'''
from google.appengine.ext import ndb
from datetime import datetime

class Game(ndb.Model):
    birthdate = ndb.DateTimeProperty(auto_now_add=True)
    lastHeartbeat = ndb.DateTimeProperty(auto_now=True)
    name = ndb.StringProperty()
    private = ndb.BooleanProperty()
    description = ndb.StringProperty()

    
class Player(ndb.Model):
    birthdate = ndb.DateTimeProperty(auto_now_add=True)
    lastHeartbeat = ndb.DateTimeProperty()
    nickname = ndb.StringProperty()
    position = ndb.GeoPtProperty()

    @classmethod
    def query_player(cls, ancestor_key):
        return cls.query(ancestor=ancestor_key).order(cls.nickname)
    
    def updatePosition(self, lat, lon):
        self.position = ndb.GeoPt(lat, lon)
        self.lastHeartbeat = datetime.now()
        self.put()
    