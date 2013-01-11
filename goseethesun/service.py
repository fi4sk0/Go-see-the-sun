'''
        Created on 14.12.2012
        
        @author: tmaul
        '''
from google.appengine.ext import ndb
from google.appengine.api import memcache

from core import Game
from core import Player

from datetime import datetime

import json
import logging


class GameService:
    
    @classmethod
    def getPlayers(cls, game):
        return Player.query(ancestor=game.key) 
    
    @classmethod
    def allGames(cls):
        return Game.query()
    
    @classmethod
    def getbyURLsafeKey(cls, urlsafekey):
        key = ndb.Key(urlsafe = urlsafekey)
        return key.get()

    @classmethod
    def createPlayer(cls, parentGame, _nickname):
        parentKey = parentGame.key;
        player = Player(parent = parentKey,
                        nickname = _nickname,
                        position = ndb.GeoPt(0, 0),
                        parentKey = parentKey.urlsafe())
        player.put()
        logging.info(parentGame.playerKeys)
        parentGame.playerKeys.append(player.key.urlsafe())
        memcache.set(parentGame.key.urlsafe(), parentGame)
        parentGame.put()
        return player
            
    @classmethod
    def createGame(cls, name, description, private):
        game = Game()
        game.name = name
        game.description = description
        game.private = private
        game.put()
        return game
    
    @classmethod
    def getBuddies(cls, player):
        parentGameKey = player.parentKey
        parentGame = GameService.getbyURLsafeKey(parentGameKey)

        # Get all cached buddies
        buddyDictionary = memcache.get_multi(parentGame.playerKeys)

        # Go through all buddy-keys of the parent game
        for playerKey in parentGame.playerKeys:
            # if one is missing, reload from the database and add to the buddy dictionary
            if playerKey not in buddyDictionary:
                buddyDictionary[playerKey] = PlayerService.getbyURLsafeKey(playerKey)

        # Now we're sure everybody is there. No Child Left Behind.
        # Everybody is in the dictionary. A good time to write it to the cache again
        memcache.set_multi(buddyDictionary)

        # The caller is only interested in the values of the dictionary.
        return buddyDictionary.values()
        
        
        
    @classmethod
    def toJSON(cls, games):
        gamesList = [game.to_dict() for game in games]
        return json.dumps(gamesList, default=jsonhandler)
    
    @classmethod
    def singleGameToJSON(cls, game):
        return json.dumps(game.to_dict(), default=jsonhandler)
    
    
class PlayerService:
    @classmethod
    def allPlayers(cls):
        return Player.query()
    
    @classmethod
    def getbyURLsafeKey(cls, urlsafekey):
        key = ndb.Key(urlsafe = urlsafekey)
        return key.get()
    
    @classmethod
    def deletePlayer(cls, playerKey):
        player = PlayerService.getbyURLsafeKey(playerKey)
        parentGame = GameService.getbyURLsafeKey(player.parentKey)
        parentGame.playerKeys.remove(playerKey)
        parentGame.put()
        memcache.delete(playerKey)
        player.key.delete()
        
    @classmethod
    def toJSON(cls, players):
        playersList = [player.to_dict() for player in players]
        return json.dumps(playersList, default=jsonhandler)

    @classmethod
    def updatePosition(cls, player, lat, lon):
        player.position = ndb.GeoPt(lat, lon)
        player.lastHeartbeat = datetime.now()
        player.put()
        
    @classmethod
    def updateCachedPosition(cls, urlsafekey, lat, lon):
        player = PlayerService.getbyURLsafeKey(urlsafekey)
        player.position = ndb.GeoPt(lat, lon)
        memcache.set(urlsafekey, player, 10)
        
    @classmethod
    def getCachedPosition(cls, urlsafekey):
        player = memcache.get(urlsafekey)
        if player is not None:
            return player
        else:
            return None
        
    @classmethod
    def injectCachedPosition(cls, players):
        for player in players:
            cachedPlayer = memcache.get(player.key.urlsafe())
            if cachedPlayer is not None:
                player.position = cachedPlayer.position

def jsonhandler(obj):
    if hasattr(obj, 'strftime'):
        return obj.strftime('%H:%M:%S-%d-%m-%Y')
    elif isinstance(obj, ndb.GeoPt):
        return (obj.lat, obj.lon)
    else:
        raise TypeError, 'Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj))
