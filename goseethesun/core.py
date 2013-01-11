'''
Created on 14.12.2012

@author: tmaul
'''
from google.appengine.ext import ndb

class Game(ndb.Model):
    birthdate = ndb.DateTimeProperty(auto_now_add=True)
    lastHeartbeat = ndb.DateTimeProperty(auto_now=True)
    name = ndb.StringProperty()
    private = ndb.BooleanProperty()
    description = ndb.StringProperty()
    maxPlayers = ndb.IntegerProperty()
    playerKeys = ndb.StringProperty(repeated=True)
    entityKeys = ndb.StringProperty(repeated=True)
    gameControllerKey = ndb.StringProperty()
    adminKey = ndb.StringProperty()
    center = ndb.GeoPtProperty()

    def to_dict(self):
        dictionary = super(Game, self).to_dict()
        dictionary['urlsafekey'] = self.key.urlsafe();
        return dictionary;
    
class Player(ndb.Model):
    birthdate = ndb.DateTimeProperty(auto_now_add=True)
    lastHeartbeat = ndb.DateTimeProperty()
    nickname = ndb.StringProperty()
    position = ndb.GeoPtProperty()
    parentKey = ndb.StringProperty()
    
    def to_dict(self):
        dictionary = super(Player, self).to_dict()
        dictionary['urlsafekey'] = self.key.urlsafe();
        return dictionary;


class Account(ndb.Model):
    birthdate = ndb.DateTimeProperty(auto_now_add=True)
    email = ndb.StringProperty();
    nickname = ndb.StringProperty();
    