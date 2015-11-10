import hours

from google.appengine.ext import ndb

class Instructor(ndb.Model):
    first = ndb.StringProperty()
    last = ndb.StringProperty()
    email = ndb.StringProperty()
    phone = ndb.StringProperty()
    building = ndb.StringProperty()
    room = ndb.StringProperty()
    #hours = ndb.LocalStructuredProperty(hours.Hours, repeated=True)
    isSelected = ndb.BooleanProperty()
    
    def key(self):
        return str(self.last + ", " + self.first);