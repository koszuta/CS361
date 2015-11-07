from google.appengine.ext import ndb

class Hours(ndb.Model):
	monday = ndb.TimeProperty()
	tuesday = ndb.TimeProperty()
	wednesday = ndb.TimeProperty()
	thursday = ndb.TimeProperty()
	friday = ndb.TimeProperty()