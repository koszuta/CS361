import Syllabus
import Calendar
import Textbook

from google.appengine.ext import ndb

class Course:
        name = ndb.StringProperty()
        number = ndb.StringProperty()
        syllabi = ndb.StructuredProperty(Syllabus, repeated=True)
        SavedCalendars = ndb.StructuredProperty(Calendar, repeated=True)
        SavedTextbooks = ndb.StructuredProperty(Textbook, repeated=True)
    
'''    
    def addSyllabus(self, Syllabus):
        
        return Syllabus
'''