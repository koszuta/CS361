import syllabus
import calendar
import textbook

from google.appengine.ext import ndb

class Course:
        name = ndb.StringProperty()
        number = ndb.StringProperty()
        syllabi = ndb.LocalStructuredProperty(syllabus, repeated=True)
        savedCalendars = ndb.LocalStructuredProperty(calendar, repeated=True)
        savedTextbooks = ndb.LocalStructuredProperty(textbook, repeated=True)
    
'''    
    def addSyllabus(self, Syllabus):
        
        return Syllabus
'''