import textbook
import calendars
import instructor
import policy
import assessment

from google.appengine.ext import ndb

class Syllabus(ndb.Model):
    @property
    def textbooks(self):
        return textbook.Textbook.query(ancestor = self.key).fetch()
    @property
    def calendars(self):
        return calendars.Calendar(ancestor = self.key).fetch()
    @property
    def instructors(self):
        return istructor.Instructor(ancestor = self.key).fetch()
    @property
    def policies(self):
        return policy.Policy(ancestor = self.key).fetch()
    @property
    def assessments(self):
        return assessment.Assessment(ancestor = self.key).fetch()