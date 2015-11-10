import hours

from google.appengine.ext import ndb

class Instructor(ndb.Model):
    first = ndb.StringProperty(required=True)
    last = ndb.StringProperty(required=True)
    email = ndb.StringProperty()
    phone = ndb.StringProperty()
    building = ndb.StringProperty()
    room = ndb.StringProperty()
    #hours = ndb.LocalStructuredProperty(hours.Hours, repeated=True)
    isSelected = ndb.BooleanProperty()
    
    def key(self):
        return str(self.last + ", " + self.first);