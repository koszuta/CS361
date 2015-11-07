import Textbook
import Calendar
import Instructor
import Policy
import Assessment

from google.appengine.ext import ndb

class Syllabus(ndb.Model):
        textbooks = ndb.StructuredProperty(Textbook, repeated=True)
        calendars = ndb.StructuredProperty(Calendar, repeated=True)
        instructors = ndb.StructuredProperty(Instructor, repeated=True)
        policies = ndb.StructuredProperty(Policy, repeated=True)
        assessments = ndb.StructuredProperty(Assessment, repeated=True)