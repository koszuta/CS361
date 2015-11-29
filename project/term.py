import os
from google.appengine.ext import ndb
from jinja2 import Environment, FileSystemLoader
from basehandler import BaseHandler
from webapp2_extras.appengine.auth.models import User

jinja_env = Environment(
  loader=FileSystemLoader(os.path.dirname(__file__)),
  extensions=['jinja2.ext.autoescape'],
  autoescape=True)

class Term(ndb.Model):
    semester = ndb.StringProperty()
    year = ndb.IntegerProperty()
    
    @property
    def syllabi(self):
        from syllabus import Syllabus
        return Syllabus.query(ancestor = self.key).fetch()
        
class WeeklyCalendarHandler(BaseHandler):
    def get(self, username, term):
        # TODO: Render weekly calendar template
        
        term = term.upper()
        user = User.get_by_auth_id(username)
        
        if user:
            terms = Term.query(ancestor = user.key).fetch()
        
            for t in terms:
                if term[0] == t.semester and int('20' + term[1:3]) == t.year:
                    self.response.write('Valid term in datastore')
                    return

        # Raise HTTP 404 error for terms not yet available
        self.abort(404)
