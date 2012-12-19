'''
        Created on 14.12.2012
        
        @author: tmaul
        '''
from google.appengine.ext import ndb

from core import Game
from core import Player

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
    def createPlayer(clf, parentGame, _nickname):
        parentKey = parentGame.key;
        player = Player(parent = parentKey,
                        nickname = _nickname,
                        position = ndb.GeoPt(0, 0))
        player.put()
        return player 
            

    
class PlayerService:
    @classmethod
    def allPlayers(cls):
        return Player.query()
    
    @classmethod
    def getbyURLsafeKey(cls, urlsafekey):
        key = ndb.Key(urlsafe = urlsafekey)
        return key.get()
    
    @classmethod
    def deletePlayer(cls, player):
        player.key().delete()