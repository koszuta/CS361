import jinja2
import webapp2
import os

from google.appengine.ext import ndb
from webapp2_extras import sessions


class BaseHandler(webapp2.RequestHandler):
    def dispatch(self):
        self.session_store = sessions.get_store(request = self.request)
        
        try:
            webapp2.RequestHandler.dispatch(self)
        finally:
            self.session_store.save_sessions(self.response)
            
    @webapp2.cached_property
    def session(self):
        return self.session_store.get_session()
        
        
import main
import login
import user
import term
import syllabus
import instructor
import textbook
import calendarEdit
import scalesEdit
import assessment
import policy
import preview 
         
config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'my-super-secret-key',
} 
app = webapp2.WSGIApplication([
    ('/', main.MainHandler),
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