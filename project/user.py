from google.appengine.ext import ndb

import webapp2_extras.appengine.auth.models

#import time

class User(webapp2_extras.appengine.auth.models.User):
    isSelected = ndb.BooleanProperty()
    @property
    def savedPolicies(self):
        from policy import Policy
        return Policy.query(ancestor = self.key).fetch()
    @property
    def savedScales(self):
        from scale import Scale
        return Scale.query(ancestor = self.key).fetch()
    @property
    def savedInstructors(self):
        from instructor import Instructor
        return Instructor.query(ancestor = self.key).fetch()
    @property
    def savedAssessments(self):
        from assessment import Assessment
        return Assessment.query(ancestor = self.key).fetch()
    @property
    def savedCalendars(self):
        from calendars import Calendar
        return Calendar.query(ancestor = self.key).fetch()
    @property
    def savedTextbooks(self):
        from textbook import Textbook
        return Textbook.query(ancestor = self.key).fetch()
    @property
    def terms(self):
        from term import Term
        return Term.query(ancestor = self.key).fetch()
        
    def set_password(self, raw_password):
        self.password = security.generate_password_hash(raw_password, length = 12)
      
    '''
    @classmethod
    def get_by_auth_token(cls, user_id, token, subject = 'auth'):
        token_key = cls.token_model.get_key(user_id, subject, token)
        user_key = ndb.Key(cls, user_id)
        
        valid_token, user = ndb.get_multi([token_key, user_key])
        if valid_token and user:
            timestamp = int(time.mktime(valid_token.created.timetuple()))
            return user, timestamp
            
        return None, None
    '''