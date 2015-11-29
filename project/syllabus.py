from google.appengine.ext import ndb
from scale import Scale
from calendarClass import CalendarClass

class Syllabus(ndb.Model):
    isActive = ndb.BooleanProperty()
    title = ndb.StringProperty()
    scale = ndb.StructuredProperty(Scale)
    calendar = ndb.StructuredProperty(CalendarClass)
    
    @property
    def textbooks(self):
        from textbook import Textbook
        return Textbook.query(ancestor = self.key).fetch()
        
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
        
    @property
    def calendars(self):
        return CalendarClass.query(ancestor = self.key).fetch()