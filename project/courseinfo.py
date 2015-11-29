import webapp2
import jinja2
import os
from google.appengine.ext import ndb

class Info(ndb.Model):
	title = ndb.StringProperty()
	subject = ndb.StringProperty()
	course = ndb.IntegerProperty()
	section = ndb.IntegerProperty()
	building = ndb.StringProperty()
	room = ndb.StringProperty()
	days = ndb.StringProperty(repeated = True)
	start = ndb.TimeProperty()
	end = ndb.TimeProperty() 