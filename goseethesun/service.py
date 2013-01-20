'''
        Created on 14.12.2012
        
        @author: tmaul
        '''
from google.appengine.ext import ndb
from google.appengine.api import memcache

from core import Game
from core import Player
from entities.BasicEntities import BasicEntity
from gamecontrollers.BasicGameController import BasicGameController

from datetime import datetime

import json
import logging


class GameService:
    @classmethod
    def allGames(cls):
        return Game.query()

    @classmethod
    def getById(cls, id):
        return Game.get_by_id(id, parent=None)

    @classmethod
    def createPlayer(cls, parentId, name):
        game = GameService.getById(parentId)
        player = Player(name = name,
                        position = ndb.GeoPt(0, 0),
                        parentId = parentId)
        player.put()
        game.playerIds.append(player.key.id())
        game.put()
        return player

    @classmethod
    def createGame(cls, name, description, private, lat, lon):
        game = Game()
        game.name = name
        game.description = description
        game.private = private
        game.center = ndb.GeoPt(lat, lon)

        gameController = BasicGameController()
        gameController.put()
        game.gameControllerId = gameController.key.id()

        game.put()
        return game

    @classmethod
    def getGameForPlayer(cls, playerId):
        player = Player.get_by_id(playerId, parent=None)
        return Game.get_by_id(player.parentId, parent=None)

    @classmethod
    def getBuddies(cls, playerId):
        player = Player.get_by_id(playerId, parent=None)
        return GameService.getPlayersForGame(player.parentId)

    @classmethod
    def getPlayersForGame(cls, gameId):
        game = Game.get_by_id(int(gameId));

        # Initialize string representations of player and entity IDs
        game.makeStringValuedIds()

        # Get all cached buddies
        buddyDictionary = memcache.get_multi( game.playerIdStrings, key_prefix='player' )

        # Go through all buddy-keys of the parent game
        for playerId in game.playerIdStrings:
            # if one is missing, reload from the database and add to the buddy dictionary
            if playerId not in buddyDictionary:
                buddyDictionary[playerId] = Player.get_by_id( int(playerId), parent=None )

        # Now we're sure everybody is there. No Child Left Behind.
        # Everybody is in the dictionary. A good time to write it to the cache again
        memcache.set_multi(buddyDictionary)

        # The caller is only interested in the values of the dictionary.
        return buddyDictionary.values()
        
        
    @classmethod
    def toJSON(cls, games):
        gamesList = [game.to_dict() for game in games]
        return json.dumps(gamesList, default=jsonHandler)
    
    @classmethod
    def singleGameToJSON(cls, game):
        return json.dumps(game.to_dict(), default=jsonHandler)

    @classmethod
    def executeGameLogicForPlayer(cls, player):
        game = GameService.getbyURLsafeKey(player.parentKey)

        # See if our game has a game controller. If not, lazily instantiate one. Don't forget to put the new
        # GameController into the gameControllerKey attribute of the corresponding game.
        if( game.gameControllerKey == ""):
            logging.info("Game didn't have a gamecontroller, creating one")
        #    gameController = BasicGameController(parentKey = player.parentKey)
         #   gameController.put()
          #  game.gameControllerKey = gameController.key.urlsafe()
           # game.put()

        # Now we're sure we have a game controller. Retrieve by its key and execute simulation step for
        # the current player
#        gameController = ndb.Key(urlsafe = game.gameControllerKey)

        #gameController.simulateStep()







    
class PlayerService:
    @classmethod
    def allPlayers(cls):
        return Player.query()

    @classmethod
    def deletePlayer(cls, playerId):
        player = Player.get_by_id(playerId, parent=None)
        parentGame = Game.get_by_id(player.parentId)
        parentGame.playerIds.remove(playerId)
        parentGame.put()
        memcache.delete(str(playerId), namespace='players')
        player.key.delete()
        
    @classmethod
    def toJSON(cls, players):
        playersList = [player.to_dict() for player in players]
        return json.dumps(playersList, default=jsonHandler)

    @classmethod
    def updatePosition(cls, player, lat, lon):
        player.position = ndb.GeoPt(lat, lon)
        player.lastHeartbeat = datetime.now()
        player.put()
        
    @classmethod
    def updateCachedPosition(cls, keyId, lat, lon):
        player = Player.get_by_id(keyId, parent = None)

        player.position = ndb.GeoPt(lat, lon)
        memcache.set(player.key.urlsafe(), player, 10)
        
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
            cachedPlayer = memcache.get(str(player.key.id()))
            if cachedPlayer is not None:
                player.position = cachedPlayer.position



def jsonHandler(obj):
    if hasattr(obj, 'strftime'):
        return obj.strftime('%H:%M:%S-%d-%m-%Y')
    elif isinstance(obj, ndb.GeoPt):
        return (obj.lat, obj.lon)
    else:
        raise TypeError, 'Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj))
