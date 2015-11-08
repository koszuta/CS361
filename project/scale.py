from google.appengine.ext import ndb

class Scale(ndb.Model):
	letter = ndb.StringProperty()
	percent = ndb.IntegerProperty()