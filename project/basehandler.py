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
        session['user'] = user.User.query(user.User.isSelected).get()
        session['syllabus'] = syllabus.Syllabus.query(ndb.AND(ancestor == session['term'].key, Syllabus.isSelected == True)).get()
        session['term'] = term.Term.query(ndb.AND(ancestor == session['user'].key, Term.isSelected == True))
        
        return session