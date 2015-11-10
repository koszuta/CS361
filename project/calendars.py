from google.appengine.ext import ndb

class Calendar(ndb.Model):
	temp = ndb.StringProperty()