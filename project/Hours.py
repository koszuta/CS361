from google.appengine.ext import ndb

class Hours(ndb.Model):
	day = ndb.StringProperty()
	start = ndb.StringProperty()
	end = ndb.StringProperty()