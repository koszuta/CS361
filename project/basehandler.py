import jinja2
import webapp2
import os
import urllib
from google.appengine.ext import ndb
from webapp2_extras import sessions

from user import User
from syllabus import Syllabus
from term import Term

class BaseHandler(webapp2.RequestHandler):
    def dispatch(self):
        self.session_store = sessions.get_store(request = self.request)
        
        try:
            webapp2.RequestHandler.dispatch(self)
        finally:
            self.session_store.save_sessions(self.response)
            
    @webapp2.cached_property
    def session(self):
        session = self.session_store.get_session()
        
        user = User.query(User.isSelected == True).get()
        if user:
            session['user'] = user.key.urlsafe()    
              
            term = Term.query(ancestor = user.key).filter(Term.isSelected == True).get()
            if term:
                session['term'] = term.key.urlsafe()
                
                syllabus = Syllabus.query(ancestor = term.key).filter(Syllabus.isSelected == True).get()
                if syllabus:
                    session['syllabus'] = syllabus.key.urlsafe()
                else:
                    s = Syllabus(parent = term.key, isSelected = True)
                    s.put()
                    session['syllabus'] = s.key.urlsafe()
            else:
                t = Term(parent = user.key, isSelected = True)
                t.put()
                s = Syllabus(parent = t.key, isSelected = True)
                s.put()
                session['term'] = t.key.urlsafe()
                session['syllabus'] = s.key.urlsafe()
        else:
            u = User(isSelected = True)
            u.put()
            t = Term(parent = user.key, isSelected = True)
            t.put()
            s = Syllabus(parent = t.key, isSelected = True)
            s.put()
            session['user'] = u.key.urlsafe()
            session['term'] = t.key.urlsafe()
            session['syllabus'] = s.key.urlsafe()
                    
        return session
       
        
import main        
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
    'secret_key': 'secret_key',
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