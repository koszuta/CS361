from google.appengine.ext import ndb

class Assessment(ndb.Model):
	title = ndb.StringProperty()
	description = ndb.TextProperty()
	percentage = ndb.IntegerProperty()
	isSelected = ndb.BooleanProperty()
	
	def copy(self):
		return Assessment(title=self.title, description=self.description, percentage=self.percentage, isSelected=self.isSelected)
		
	def key(self):
		if self.title == "" or self.title is None:
			return "none"
			
		return self.title + ": " + str(self.percentage) + "%"