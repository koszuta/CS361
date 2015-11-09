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
        
'''       
    def setFirstName(self, str):
        self.first = str;
        
    def setLastName(self, str):
        self.last = str;
        
    def setEmail(self, str):
        self.email = str;
        
    def setPhone(self, str):
        self.phone = str;
        
    def setBuilding(self, str):
        self.building = str;
        
    def setRoom(self, str):
        self.room = str;
        
    def setHours(self, str):
        self.hours = str;
'''