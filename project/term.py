import webapp2
import jinja2
import os
from google.appengine.ext import ndb

'''
from syllabus import Syllabus
'''

class Term(ndb.Model):
        semester = ndb.StringProperty()
        year = ndb.IntegerProperty()
        isSelected = ndb.BooleanProperty()
        @property
        def syllabi(self):
            return Syllabus.query(ancestor = self.key).fetch()