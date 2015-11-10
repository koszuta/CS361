import syllabus
import calendars
import textbook

from google.appengine.ext import ndb

class Course:
        name = ndb.StringProperty()
        number = ndb.StringProperty()
        savedSyllabi = ndb.LocalStructuredProperty(syllabus.Syllabus, repeated=True)
        savedCalendars = ndb.LocalStructuredProperty(calendars.Calendar, repeated=True)
        savedTextbooks = ndb.LocalStructuredProperty(textbook.Textbook, repeated=True)