from google.appengine.ext import ndb

class User(ndb.Model):
    username = ndb.StringProperty()
    password = ndb.StringProperty()
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
