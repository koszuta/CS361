from google.appengine.ext import ndb

class Textbook(ndb.Model):
	temp = ndb.StringProperty()