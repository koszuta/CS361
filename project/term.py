import webapp2
import jinja2
import os

from google.appengine.ext import ndb

from jinja2 import Environment, FileSystemLoader
from basehandler import BaseHandler
from webapp2_extras.appengine.auth.models import User

jinja_env = Environment(
  loader=FileSystemLoader(os.path.dirname(__file__)),
  extensions=['jinja2.ext.autoescape', 'jinja2.ext.with_'],
  autoescape=True)

class Term(ndb.Model):
    semester = ndb.StringProperty()
    year = ndb.IntegerProperty()
    
    @property
    def syllabi(self):
        from syllabus import Syllabus
        return Syllabus.query(ancestor = self.key).fetch()
    
    @webapp2.cached_property
    def url(self):
        return self.semester + str(self.year % 100)

    @property
    def fullName(self):
        # Convert semester letter to name
        if self.semester == 'F':
            string = 'Fall '
        elif self.semester == 'S':
            string = 'Spring '
        elif self.semester == 'M':
            string = 'Summer '
        elif self.semester == 'W':
            string = 'Winterim '
        else:
            string = ""

        string += str(self.year)

        return string
        
class WeeklyCalendarHandler(BaseHandler):
    def render(self, user, term):            
        template = jinja_env.get_template('term.html')
        context = {}
        if term:
            context = {
                'semester': term.semester,
                'year': term.year,
                'term': term,
                'username': user.auth_ids[0],
                'term_abbr': term.url
            }
        
        self.response.write(template.render(context))

    def get(self, username, term):
        # TODO: Render weekly calendar template
        
        term = term.upper()
        user = User.get_by_auth_id(username)
        
        if user:
            terms = Term.query(ancestor = user.key).fetch()
        
            for t in terms:
                if t.url == term:
                    return self.render(user, t)

        # Raise HTTP 404 error for terms not yet available
        self.abort(404)
