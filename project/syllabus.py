from google.appengine.ext import ndb

'''
from assessment import Assessment
from calendars import Calendar
from instructor import Instructor
from policy import Policy
from textbook import Textbook
'''

class Syllabus(ndb.Model):
    isSelected = ndb.BooleanProperty()
    @property
    def textbooks(self):
        return textbook.Textbook.query(ancestor = self.key).fetch()
    @property
    def calendars(self):
        return calendars.Calendar.query(ancestor = self.key).fetch()
    @property
    def instructors(self):
        return istructor.Instructor.query(ancestor = self.key).fetch()
    @property
    def policies(self):
        return policy.Policy.query(ancestor = self.key).fetch()
    @property
    def assessments(self):
        return assessment.Assessment.query(ancestor = self.key).fetch()