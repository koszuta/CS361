from google.appengine.ext import ndb

'''
from assessment import Assessment
from calendars import Calendar
from instructor import Instructor
from policy import Policy
from scale import Scale
from term import Term
from textbook import Textbook
'''

class User(ndb.Model):
    username = ndb.StringProperty()
    password = ndb.StringProperty()
    isSelected = ndb.BooleanProperty()
    @property
    def savedPolicies(self):
        return Policy.query(ancestor = self.key).fetch()
    @property
    def savedScales(self):
        return Scale.query(ancestor = self.key).fetch()
    @property
    def savedInstructors(self):
        return Instructor.query(ancestor = self.key).fetch()
    @property
    def savedAssessments(self):
        return Assessment.query(ancestor = self.key).fetch()
    @property
    def savedCalendars(self):
        return Calendar.query(ancestor = self.key).fetch()
    @property
    def savedTextbooks(self):
        return Textbook.query(ancestor = self.key).fetch()
    @property
    def terms(self):
        return Term.query(ancestor = self.key).fetch()