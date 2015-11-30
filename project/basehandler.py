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
    def user(self):
        return self.auth.get_user_by_session()

def login_required(handler):
    def check_login(self, *args, **kwargs):
        auth = self.auth
        if not self.session['user']:
            return self.redirect('/login')
        else:
            return handler(self, *args, **kwargs)
            
    return check_login