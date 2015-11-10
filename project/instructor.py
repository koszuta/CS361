from google.appengine.ext import ndb

class Instructor(ndb.Model):
    first = ndb.StringProperty()
    last = ndb.StringProperty()
    email = ndb.StringProperty()
    phone = ndb.StringProperty()
    building = ndb.StringProperty()
    room = ndb.StringProperty()
    hours = ndb.StringProperty()
    isSelected = ndb.BooleanProperty()
    
    def key(self):
        if self.last == "" or self.last is None or self.first == "" or self.last is None:
            return "nobody"
        '''    
        if self.isSelected:
            return str(self.last + ", " + self.first + " (True)")
        else:
            return str(self.last + ", " + self.first + " (False)")
        '''
        return self.last + ", " + self.first
        
    def copy(self):
        return Instructor(first=self.first, last=self.last, email=self.email, phone=self.phone, building=self.building, room=self.room, isSelected=self.isSelected)
