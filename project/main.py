import webapp2
import jinja2
import os
from google.appengine.ext import ndb
from google.appengine.api import oauth

from basehandler import BaseHandler
       
from textbook import Textbook
from instructor import Instructor       

template_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.getcwd())
    )
      
class MainHandler(BaseHandler):
    def get(self):
        syllabusKey = self.session.get('syllabus')
        syllabus = ndb.Key(urlsafe = syllabusKey).get()
    
        template = template_env.get_template('main.html')
        context = {
            'books': Textbook.query(ancestor = syllabus.key).fetch(),
            'instructors': Instructor.query(ancestor = syllabus.key).fetch(),
        }
        
        self.response.write(template.render(context))
               
import user    
import assessment
import instructor
import login
import calendarEdit
import policy
import preview
import scalesEdit
import textbook    
     
config = {}
config['webapp2_extras.auth'] = {
    'user_model': user.User,
}
config['webapp2_extras.sessions'] = {
    'secret_key': 'secret_key',
} 
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/login', login.LoginHandler),
    ('/signup', login.SignupHandler),
    ('/addinstructor', instructor.AddHandler),
    ('/removeinstructor', instructor.RemoveHandler),
    ('/editinstructor', instructor.EditHandler),
    ('/editbooks', textbook.TextbookHandler),
    ('/editbook', textbook.EditTextbookHandler),
    ('/removebooks', textbook.RemoveTextbookHandler),
    ('/editcalendar', calendarEdit.CalendarHandler),
    ('/editscales', scalesEdit.ScalesHandler),
    ('/editassessment', assessment.EditHandler),
    ('/addassessment', assessment.AddHandler),
    ('/removeassessment', assessment.RemoveHandler),
    ('/editpolicy', policy.EditHandler),
    ('/addpolicy', policy.AddHandler),
    ('/removepolicy', policy.RemoveHandler),
    ('/preview', preview.PreviewHandler),
], debug=True, config=config)