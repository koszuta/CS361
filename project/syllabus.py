import Textbook
import calendar
import Instructor
import policy
import assessment

from google.appengine.ext import ndb

class Syllabus(ndb.Model):
        textbooks = ndb.LocalStructuredProperty(Textbook.Textbook, repeated=True)
        calendars = ndb.LocalStructuredProperty(calendar.Calendar, repeated=True)
        instructors = ndb.LocalStructuredProperty(Instructor.Instructor, repeated=True)
        policies = ndb.LocalStructuredProperty(policy.Policy, repeated=True)
        assessments = ndb.LocalStructuredProperty(assessment.Assessment, repeated=True)