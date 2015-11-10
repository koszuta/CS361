from google.appengine.ext import ndb

class Policy(ndb.Model):
	title = ndb.StringProperty()
	description = ndb.TextProperty()
	isSelected = ndb.BooleanProperty()
	
	def copy(self):
		return Policy(title=self.title, description=self.description, isSelected=self.isSelected)
		
	def key(self):
		if self.title == "" or self.title is None:
			return "none"
			
		return self.title