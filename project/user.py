import time
import webapp2_extras.appengine.auth.models
from google.appengine.ext import ndb
from webapp2_extras import security

class User(webapp2_extras.appengine.auth.models.User):
    @property
    def savedPolicies(self):
        from policy import Policy
        return Policy.query(ancestor = self.key).filter(Policy.onSyllabus == False).fetch()
        
    @property
    def savedScales(self):
        from scalesEdit import GradeScale
        return GradeScale.query(ancestor = self.key).filter(GradeScale.onSyllabus == False).fetch()
        
    @property
    def savedInstructors(self):
        from instructor import Instructor
        return Instructor.query(ancestor = self.key).filter(Instructor.onSyllabus == False).order(Instructor.last).fetch()
        
    @property
    def savedAssessments(self):
        from assessment import Assessment
        return Assessment.query(ancestor = self.key).filter(Assessment.onSyllabus == False).fetch()
        
    @property
    def savedCalendars(self):
        from calendarClass import CalendarClass
        return CalendarClass.query(ancestor = self.key).filter(CalendarClass.onSyllabus == False).fetch()
        
    @property
    def savedTextbooks(self):
        from textbook import Textbook
        return Textbook.query(ancestor = self.key).filter(Textbook.onSyllabus == False).fetch()
        
    @property
    def terms(self):
        from term import Term
        return Term.query(ancestor = self.key).fetch()
        
    '''    
    def set_password(self, raw_password):
        self.password = security.generate_password_hash(raw_password, length = 12)
    '''
