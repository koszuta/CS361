
class Instructor:
    def __init__(self, first='', last='', email='', phone='', building='', room='', hours=''):
		self.first = first
		self.last = last
		self.email = email
		self.phone = phone
		self.building = building
		self.room = room
		self.hours = hours
        
    def getKey(self):
        return str(self.last + ", " + self.first);
        
        
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