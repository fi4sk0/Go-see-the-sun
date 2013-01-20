
import webapp2
import os
import logging

from google.appengine.ext.webapp import template
from google.appengine.ext import ndb
from google.appengine.api import memcache

from goseethesun.service import GameService
from goseethesun.service import PlayerService
from goseethesun.core import Game
from goseethesun.core import Entity
from goseethesun.core import Player
from goseethesun.gamecontrollers.BasicGameController import BasicGameController

import json


class WebGamesHandler(webapp2.RequestHandler):
    def get(self):
        games = GameService.allGames()
        template_values = {'games': games}
        path = os.path.join(os.path.dirname(__file__), 'web/listGames.html')
        self.response.out.write(template.render(path, template_values))

    def post(self):
        games = Game.query()
        for game in games:
            game.key.delete()

        entities = Entity.query()
        for entity in entities:
            entity.key.delete()

        self.redirect('/')


class JSONGamesHandler(webapp2.RequestHandler):
    def get(self):
        logging.info(self.request)
        self.response.headers['Content-Type'] = 'application/json'
        games = GameService.allGames()
        self.response.out.write(GameService.toJSON(games))
        logging.info(self.response)
        
    def post(self):
        self.response.headers['Content-Type'] = 'application/json'
        args = json.loads(self.request.body)
        name = args['name']
        description = args['description']
        private = args['private'] != '';
        lat = args['lat']
        lon = args['lon']
        logging.info(name)
        logging.info(description)
        logging.info(private)
        game = GameService.createGame(name, description, private, lat, lon)
        games = [game]
        self.response.out.write(GameService.toJSON(games))  


class JSONPlayerHandler(webapp2.RequestHandler):
    def post(self):
        self.response.headers['Content-Type'] = 'application/json'
        args = json.loads(self.request.body)
        gameId = args['gameKeyId']
        nickname = args['nickname']
        player = GameService.createPlayer(gameId, nickname)
        players = [player]

        self.response.out.write(PlayerService.toJSON(players))
        logging.info(PlayerService.toJSON(players))


class JSONResignHandler(webapp2.RequestHandler):
    def post(self):
        logging.info(self.request.body)
        args = json.loads(self.request.body)
        playerKey = args['id']
        PlayerService.deletePlayer(playerKey)

                
class JSONPositionHandler(webapp2.RequestHandler):
    def post(self):
        args = json.loads(self.request.body)
        lat = args['lat']
        lon = args['lon']
        playerId = int(args['id'])

        PlayerService.updateCachedPosition(playerId, lat, lon)

        players = GameService.getBuddies(playerId)

        #GameService.executeGameLogicForPlayer(player)

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(PlayerService.toJSON(players))
        logging.info(self.response)

class JSONActionHandler(webapp2.RequestHandler):
    def post(self):
        args = json.loads(self.request.body)
        playerId = int(args['id'])
        action = args['action']
        target = args['target']
        game = GameService.getGameForPlayer(playerId)
        controller = BasicGameController.get_by_id(game.gameControllerId, parent=None)
        getattr(controller, action)(target, playerId)


class JSONStaticsHandler(webapp2.RequestHandler):
    pass

class JSONDynamicsHandler(webapp2.RequestHandler):
    pass


app = webapp2.WSGIApplication([
    ('/', WebGamesHandler),
    ('/play.json'    , JSONPositionHandler),
    ('/games.json'   , JSONGamesHandler   ),
    ('/player.json'  , JSONPlayerHandler  ),
    ('/resign.json'  , JSONResignHandler  ),
    ('/statics.json' , JSONStaticsHandler ),
    ('/dynamics.json', JSONDynamicsHandler),
    ('/action.json'  , JSONActionHandler),
    ], debug=True)
