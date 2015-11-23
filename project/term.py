import webapp2
import jinja2
import os

from google.appengine.ext import ndb

import syllabus
import calendars
import textbook

class Term(ndb.Model):
        semester = ndb.StringProperty()
        year = ndb.IntegerProperty()
        isSelected = ndb.BooleanProperty()
        @property
        def syllabi(self):
            return syllabus.Syllabus.query(ancestor = self.key).fetch()