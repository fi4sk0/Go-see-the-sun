from google.appengine.ext import ndb
#from goseethesun.helper.gis import geodetic2ecef, ecef2geodetic
from goseethesun.entities.BasicEntities import BallEntity

import logging


class BasicGameController(ndb.Model):
    typeInfo = {'title' : 'Basic Game', 
                'description' : 'Fight for your right to pordi'}

    parentKey = ndb.StringProperty()
    entityKeys = ndb.StringProperty(repeated=True)

    def initStep(self):
        pass

    def createBall(self, target, player):
        logging.info('yeaaa who!! player is {}, target is {}'.format(player, target))


    def simulateStep(self, players, entities, game, dt):
        self.initStep()

        if len(self.entities) == 0:
            ball = BallEntity(position = game.center)
            ball.put()
            self.entities = [ball]

        for player in players:
            pass



    def getStaticEntities(self):
        pass

