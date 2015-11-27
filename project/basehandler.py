import jinja2
import webapp2
import os
import urllib
from google.appengine.ext import ndb
from webapp2_extras import sessions, auth

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
        
    @webapp2.cached_property
    def auth(self):
        return auth.get_auth()
    
    @webapp2.cached_property
    def user(self):
        return self.auth.get_user_by_session()
  
    @webapp2.cached_property  
    def user_model(self):
        user_model, timestamp =
            self.auth.store.user_model.get_by_auth_token(
                self.user['user_id'],
                self.user['token']) if self.user else (None, None)
        return user_model
        
    '''
    def render_template(self, view_filename, params = {}):
        user = self.user_info
        params['user'] = user
        path = os.path.join(os.path.dirname(__file__), 'views', view_filename)
        self.response.write(template.render(path, params))
    
    def display_message(self, message):
        """ Utility function to display a template with a simple message. """
        params = {
        'message': message
        }
        self.render_template('message.html', params)
    '''