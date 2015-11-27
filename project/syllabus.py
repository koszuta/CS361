from google.appengine.ext import ndb

class Syllabus(ndb.Model):
    isSelected = ndb.BooleanProperty()
    
    @property
    def textbooks(self):
        from textbook import Textbook
        return Textbook.query(ancestor = self.key).fetch()
        
    @property
    def calendars(self):
        from calendars import Calendar
        return Calendar.query(ancestor = self.key).fetch()
        
    @property
    def instructors(self):
        from instructor import Instructor
        return Instructor.query(ancestor = self.key).fetch()
        
    @property
    def policies(self):
        from policy import Policy
        return Policy.query(ancestor = self.key).fetch()
        
    @property
    def assessments(self):
        from assessment import Assessment
        return Assessment.query(ancestor = self.key).fetch()