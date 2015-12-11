import jinja2
import webapp2
import os
import urllib
from google.appengine.ext import ndb
from webapp2_extras import sessions, auth

class BaseHandler(webapp2.RequestHandler):
    def dispatch(self):
        self.session_store = sessions.get_store(request = self.request)
        
        try:
            webapp2.RequestHandler.dispatch(self)
        finally:
            self.session_store.save_sessions(self.response)
          
    @webapp2.cached_property
    def session(self):
        from user import User
        from syllabus import Syllabus
        from term import Term

        session = self.session_store.get_session()
        return session
       
    @webapp2.cached_property
    def auth(self):
        return auth.get_auth()
    
    @webapp2.cached_property
    def current_user(self):
        return self.auth.get_user_by_session()
        
    @webapp2.cached_property
    def current_term(self):
        key = self.session.get('term')
        return ndb.Key(urlsafe = key).get() if key else None
        
    @webapp2.cached_property
    def current_syllabus(self):
        key = self.session.get('syllabus')
        return ndb.Key(urlsafe = key).get() if key else None

def login_required(handler):
    def check_login(self, *args, **kwargs):
        if not self.current_user:
            return self.redirect('/login')
        else:
            return handler(self, *args, **kwargs)
            
    return check_login