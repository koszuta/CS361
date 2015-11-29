import os
from google.appengine.ext import ndb
from jinja2 import Environment, FileSystemLoader
from basehandler import BaseHandler

jinja_env = Environment(
  loader=FileSystemLoader(os.path.dirname(__file__)),
  extensions=['jinja2.ext.autoescape'],
  autoescape=True)

class Term(ndb.Model):
    semester = ndb.StringProperty()
    year = ndb.IntegerProperty()
    isSelected = ndb.BooleanProperty()
    
    @property
    def syllabi(self):
        from syllabus import Syllabus
        return Syllabus.query(ancestor = self.key).fetch()
        
class WeeklyCalendarHandler(BaseHandler):
    def get(self, term):
        # TODO: Render weekly calendar template
        
        term = term.upper()
        userKey = self.session.get('user')
        user = ndb.Key(urlsafe = userKey).get()
        terms = Term.query(ancestor = user.key).fetch()
        
        for t in terms:
            if term[0] == t.semester and int('20' + term[1:3]) == t.year:
                self.response.write('Valid term in datastore')
                return
        
        # Raise HTTP 404 error for terms not yet available
        self.abort(404)
