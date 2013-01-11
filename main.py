
import webapp2
import os
import logging

from google.appengine.ext.webapp import template

from goseethesun.service import GameService
from goseethesun.service import PlayerService

import json

from goseethesun.helper.gis import Vector

class WebGamesHandler(webapp2.RequestHandler):
    def get(self):
        games = GameService.allGames()
        template_values = {'games': games}
        path = os.path.join(os.path.dirname(__file__), 'web/listGames.html')
        self.response.out.write(template.render(path, template_values))
        v = Vector(1., 2., 3.)
        logging.info(v / 2.)
        logging.info(v.length())
        
    def post(self):
        
        if(self.request.get('deleteID')):
            self.delete()
            return
        
        gameId = self.request.get('id')
        game = GameService.getbyURLsafeKey(gameId)
        players = GameService.getPlayers(game)
        PlayerService.injectCachedPosition(players)
        template_values = {'game'    : game,
                           'players' : players}
        
        path = os.path.join(os.path.dirname(__file__), 'web/showGame.html')
        self.response.out.write(template.render(path, template_values))

    def delete(self):
        logging.info("delete stuff")
        gameId = self.request.get('deleteID')
        game = GameService.getbyURLsafeKey(gameId)
        players = GameService.getPlayers(game)
        for player in players:
            player.key.delete()
        game.key.delete()
        self.redirect('/')
        
class CreateGame(webapp2.RequestHandler):
    def get(self):
        self.redirect("/")
        
    def post(self):
        description = self.request.get("description")
        name = self.request.get("name")
        private = self.request.get("private") != ''
        GameService.createGame(name, description, private)
        self.redirect("/")


class JSONGamesHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        games = GameService.allGames()
        self.response.out.write(GameService.toJSON(games))  
        
    def post(self):  
        self.response.headers['Content-Type'] = 'application/json'
        args = json.loads(self.request.body)
        name = args['name']
        description = args['description']
        private = args['private'] != '';
        logging.info(name)
        logging.info(description)
        logging.info(private)
        game = GameService.createGame(name, description, private)
        games = [game];
        self.response.out.write(GameService.toJSON(games))  


class JSONPlayerHandler(webapp2.RequestHandler):
    def post(self):
        self.response.headers['Content-Type'] = 'application/json'
        args = json.loads(self.request.body)
        urlsafekey = args['urlsafekey']
        nickname = args['nickname']
        game = GameService.getbyURLsafeKey(urlsafekey)
        player = GameService.createPlayer(game, nickname)
        players = [player]
        self.response.out.write(PlayerService.toJSON(players))
        logging.info(PlayerService.toJSON(players))

class JSONResignHandler(webapp2.RequestHandler):
    def post(self):
        logging.info(self.request.body)
        args = json.loads(self.request.body)
        playerKey = args['playerKey']
        PlayerService.deletePlayer(playerKey)

                
class JSONPositionHandler(webapp2.RequestHandler):
    def post(self):
        args = json.loads(self.request.body)
        lat = args['lat']
        lon = args['lon']
        playerKey = args['playerKey']
        
        PlayerService.updateCachedPosition(playerKey, lat, lon)
        player = PlayerService.getbyURLsafeKey(playerKey)
        players = GameService.getBuddies(player)
        logging.info(len(players))
        #PlayerService.injectCachedPosition(players)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(PlayerService.toJSON(players))

class JSONStaticsHandler(webapp2.RequestHandler):
    pass

class JSONDynamicsHandler(webapp2.RequestHandler):
    pass
                

class UpdateHandler(webapp2.RequestHandler):
    def get(self):
        players = PlayerService.allPlayers()
        PlayerService.injectCachedPosition(players)
        
        template_values = {'players' : players}
        path = os.path.join(os.path.dirname(__file__), 'web/listPlayers.html')
        self.response.out.write(template.render(path, template_values))
        
    def post(self):
        logging.info(self.request)        
        playerID = self.request.get('playerID')
        lat = self.request.get('lat')
        lon = self.request.get('lon')
        player = PlayerService.getbyURLsafeKey(urlsafekey = playerID)
        player.updatePosition(lat, lon)
        self.redirect('/update')


class DeletePlayer(webapp2.RequestHandler):
    def post(self):
        thePlayerToDelete = PlayerService.getbyURLsafeKey(self.request.get('deleteID'))
        self.response.out.write("deleted! %s" % thePlayerToDelete.nickname )
        PlayerService.deletePlayer(thePlayerToDelete)
        self.redirect("/")
        
    def get(self):
        self.redirect("/")

class CreatePlayer(webapp2.RequestHandler):
    def get(self):
        self.redirect("/")

    def post(self):
        try:
            parentGame = GameService.getbyURLsafeKey(self.request.get("ancestor"))
            GameService.createPlayer(parentGame, self.request.get("nickname"))
        except TypeError:
            logging.info(self.request.get("ancestor"))


app = webapp2.WSGIApplication([
    ('/', WebGamesHandler),
    ('/createPlayer' , CreatePlayer       ),
    ('/deletePlayer' , DeletePlayer       ),
    ('/update'       , UpdateHandler      ),
    ('/createGame'   , CreateGame         ),
    ('/play.json'    , JSONPositionHandler),
    ('/games.json'   , JSONGamesHandler   ),
    ('/player.json'  , JSONPlayerHandler  ),
    ('/resign.json'  , JSONResignHandler  ),
    ('/statics.json' , JSONStaticsHandler ),
    ('/dynamics.json', JSONDynamicsHandler),
    ], debug=True)
