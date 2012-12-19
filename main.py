
import webapp2
import os
import logging

from google.appengine.ext.webapp import template

from goseethesun.core import Game
from goseethesun.core import Player
from goseethesun.service import GameService
from goseethesun.service import PlayerService


class WebGamesHandler(webapp2.RequestHandler):
    def get(self):
        games = GameService.allGames()
        template_values = {'games': games}
        path = os.path.join(os.path.dirname(__file__), 'web/listGames.html')
        self.response.out.write(template.render(path, template_values))
        
    def post(self):
        
        if(self.request.get('deleteID')):
            self.delete()
            return
        
        gameId = self.request.get('id')
        game = GameService.getbyURLsafeKey(gameId)
        players = GameService.getPlayers(game)
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
        
class CreateGame(webapp2.RequestHandler):
    def get(self):
        self.redirect("/")
        
    def post(self):
        game = Game()
        game.description = self.request.get("description")
        game.name = self.request.get("name")
        game.private = self.request.get("private") != ''
        game.put()
        self.redirect("/")
        
class XMLGamesHandler(webapp2.RequestHandler):
    def get(self):
        games = GameService.allGames()
        
        
class UpdateHandler(webapp2.RequestHandler):
    def get(self):
        players = PlayerService.allPlayers()
        template_values = {'players' : players}
        path = os.path.join(os.path.dirname(__file__), 'web/listPlayers.html')
        self.response.out.write(template.render(path, template_values))
        
    def post(self):
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
    ('/createPlayer', CreatePlayer ),
    ('/deletePlayer', DeletePlayer ),
    ('/update'      , UpdateHandler),
    ('/createGame'  , CreateGame   ),
    ], debug=True)
