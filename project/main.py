import webapp2
import jinja2
import os
from google.appengine.ext import ndb
from google.appengine.api import oauth

from basehandler import BaseHandler
    
template_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.getcwd())
    )
      
class MainHandler(BaseHandler):
    def get(self):
    
        template = template_env.get_template('main.html')
        context = {
            'books': textbook.Textbook.query().fetch(),
            'instructors': instructor.Instructor.query().fetch(),
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
config['webapp2_extras.sessions'] = {
    'secret_key': 'my-super-secret-key',
} 
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/login', login.LoginHandler),
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