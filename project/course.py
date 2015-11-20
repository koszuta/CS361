import webapp2
import jinja2
import os

from google.appengine.ext import ndb

import syllabus
import calendars
import textbook

class Course:
        name = ndb.StringProperty()
        number = ndb.StringProperty()
        savedSyllabi = ndb.LocalStructuredProperty(syllabus.Syllabus, repeated=True)
        savedCalendars = ndb.LocalStructuredProperty(calendars.Calendar, repeated=True)
        savedTextbooks = ndb.LocalStructuredProperty(textbook.Textbook, repeated=True)