import term
import policy
import scale
import instructor
import assessment
import calendars
import textbook

from google.appengine.ext import ndb

class User(ndb.Model):
    username = ndb.StringProperty()
    password = ndb.StringProperty()
    isSelected = ndb.BooleanProperty()
    @property
    def savedPolicies(self):
        return policy.Policy(ancestor = self.key).fetch()
    @property
    def savedScales(self):
        return scale.Scale(ancestor = self.key).fetch()
    @property
    def savedInstructors(self):
        return instructor.Instructor(ancestor = self.key).fetch()
    @property
    def savedAssessments(self):
        return assessment.Assessment(ancestor = self.key).fetch()
    @property
    def savedCalendars(self):
        return calendars.Calendar(ancestor = self.key).fetch()
    @property
    def savedTextbooks(self):
        return textbook.Textbook(ancestor = self.key).fetch()
    @property
    def terms(self):
        return term.Term.query(ancestor = self.key).fetch()