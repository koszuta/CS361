from google.appengine.ext import ndb

class Hours(ndb.Model):
	start = ndb.TimeProperty()
	stop = ndb.TimeProperty()