from google.appengine.ext import ndb

class Assessment(ndb.Model):
	title = ndb.StringProperty()
	description = ndb.TextProperty()
	percentage = ndb.IntegerProperty()