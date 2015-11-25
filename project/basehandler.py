import jinja2
import webapp2
import os

from google.appengine.ext import ndb
from webapp2_extras import sessions

class BaseHandler(webapp2.RequestHandler):
    def dispatch(self):
        self.session_store = sessions.get_store(request = self.request)
        
        try:
            self.session_store.save_sessions(self.response)
        finally:
            self.session_store.save_sessions(self.response)
            
    @webapp2.cached_property
    def session(self):
        return self.session_store.get_session()