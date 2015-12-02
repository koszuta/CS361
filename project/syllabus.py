from google.appengine.ext import ndb
from courseinfo import Info

class Syllabus(ndb.Model):
    isActive = ndb.BooleanProperty(default = True)
    info = ndb.StructuredProperty(Info)
	
    @property
    def scale(self):
        from scalesEdit import GradeScale
        return GradeScale.query(ancestor = self.key).get()
    
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
        from calendarClass import CalendarClass
        return CalendarClass.query(ancestor = self.key).fetch()
        