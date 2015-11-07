from google.appengine.ext import ndb

class Policy(ndb.Model):
	temp = ndb.StringProperty()