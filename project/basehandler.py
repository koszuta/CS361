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
        
    @webapp2.cached_property
    def auth(self):
        """
        Shortcut to access the auth instance as a property.
        """
        return auth.get_auth()
    
    @webapp2.cached_property
    def user_info(self):
        """
        Shortcut to access a subset of the user attributes that are stored
        in the session.
        
        The list of attributes to store in the session is specified in
        config['webapp2_extras.auth']['user_attributes'].
        :returns
        A dictionary with most user information
        """
        return self.auth.get_user_by_session()

    @webapp2.cached_property
    def user(self):
        """
        Shortcut to access the current logged in user.
        
        Unlike user_info, it fetches information from the persistence layer and
        returns an instance of the underlying model.
        
        :returns
        The instance of the user model associated to the logged in user.
        """
        u = self.user_info
        return self.user_model.get_by_id(u['user_id']) if u else None
        
    @webapp2.cached_property  
    def user_model(self):
        """
        Returns the implementation of the user model.
    
        It is consistent with config['webapp2_extras.auth']['user_model'], if set.
        """  
        return self.auth.store.user_model
      
    def render_template(self, view_filename, params = {}):
        user = self.user_info
        params['user'] = user
        path = os.path.join(os.path.dirname(__file__), 'views', view_filename)
        self.response.out.write(template.render(path, params))
    
    def display_message(self, message):
        """Utility function to display a template with a simple message."""
        params = {
        'message': message
        }
        self.render_template('message.html', params)
 
          