import jinja2
import webapp2
import os
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
        session['user'] = User.query(User.isSelected == True).get()
        session['term'] = Term.query(ancestor = user.key).filter(Term.isSelected == True).get()
        session['syllabus'] = Syllabus.query(ancestor = user.key).filter(Syllabus.isSelected == True).get()
        
        return session