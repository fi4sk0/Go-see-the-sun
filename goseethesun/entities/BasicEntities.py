__author__ = 'tmaul'

from google.appengine.ext import ndb

class BasicEntity(ndb.Model):
    position = ndb.GeoPtProperty()
    name = ndb.StringProperty()
    parentKey = ndb.StringProperty()

class BallEntity(BasicEntity):
    m = 10
    d = 1
    v = ()