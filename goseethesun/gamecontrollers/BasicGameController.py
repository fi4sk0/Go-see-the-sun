from google.appengine.ext import ndb
from goseethesun.helper.gis import geodetic2ecef, ecef2geodetic
from goseethesun.entities.BasicEntities import BallEntity

class BasicGameController(ndb.Model):
    typeInfo = {'title' : 'Basic Game', 
                'description' : 'Fight for your right to pordi'}

    entityList = ndb.StringProperty(repeated=True)

    def beginGame(self):
        pass

    def simulateStep(self, players, entities, game, dt):

        
        if len(self.entityList) == 0:
            ball = BallEntity(position = )

        for player in players:
            pass



    def getStaticEntities(self):
        pass

