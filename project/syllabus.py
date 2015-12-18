from google.appengine.ext import ndb
from courseinfo import Info

class Syllabus(ndb.Model):
    isActive = ndb.BooleanProperty(default = True)
    prime = ndb.StringProperty(default = '')
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
        last = self.prime.split(',')[0]
        first = self.prime.split()
        if len(first) > 1:
            first = first[1]
        else:
            first = None
            
        prime = Instructor.query(ancestor = self.key).filter(ndb.AND(Instructor.last == last, Instructor.first == first)).get()
        ret = []
        if prime:
            ret.append(prime)
        instructors_list = Instructor.query(ancestor = self.key).order(Instructor.last).fetch()
        for i in instructors_list:
            if i != prime:
                ret.append(i)
                
        return ret
        
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
        