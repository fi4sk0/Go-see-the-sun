'''
Created on 14.12.2012

@author: tmaul
'''
import logging
from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel


class Game(ndb.Model):
    birthdate = ndb.DateTimeProperty(auto_now_add=True)
    lastHeartbeat = ndb.DateTimeProperty(auto_now=True)
    name = ndb.StringProperty()
    private = ndb.BooleanProperty()
    description = ndb.StringProperty()
    maxPlayers = ndb.IntegerProperty()
    playerIds = ndb.IntegerProperty(repeated=True)
    entityIds = ndb.IntegerProperty(repeated=True)
    gameControllerId = ndb.IntegerProperty()
    adminId = ndb.StringProperty()
    center = ndb.GeoPtProperty()

    def makeStringValuedIds(self):
        self.playerIdStrings = map(str, self.playerIds)
        self.entityIdStrings = map(str, self.entityIds)

    def to_dict(self):
        return {'name': self.name,
                'id': self.key.id(),
                'private': self.private,
                'description': self.description,
                'maxPlayers': self.maxPlayers,
                'center': self.center,
                'currentPlayers': len(self.playerIds)}

class Entity(polymodel.PolyModel):
    name = ndb.StringProperty()
    position = ndb.GeoPtProperty()
    parentId = ndb.IntegerProperty()
    lastHeartbeat = ndb.DateTimeProperty(auto_now=True)
    memcache_prefix = 'entity'

    def to_dict(self):
        return {'name': self.name,
                'position': self.position,
                'id': self.key.id(),
                'class': str(self.__class__.__name__)}

class Player(Entity):
    pass

class Account(ndb.Model):
    email = ndb.StringProperty();
    nickname = ndb.StringProperty();
    