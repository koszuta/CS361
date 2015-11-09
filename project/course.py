import syllabus
import calendar
import Textbook

from google.appengine.ext import ndb

class Course:
        name = ndb.StringProperty()
        number = ndb.StringProperty()
        syllabi = ndb.LocalStructuredProperty(syllabus, repeated=True)
        savedCalendars = ndb.LocalStructuredProperty(calendar, repeated=True)
        savedTextbooks = ndb.LocalStructuredProperty(Textbook, repeated=True)
    
'''    
    def addSyllabus(self, Syllabus):
        
        return Syllabus
'''