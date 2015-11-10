import textbook
import calendars
import instructor
import policy
import assessment

from google.appengine.ext import ndb

class Syllabus(ndb.Model):
        textbooks = ndb.LocalStructuredProperty(textbook.Textbook, repeated=True)
        calendars = ndb.LocalStructuredProperty(calendars.Calendar, repeated=True)
        instructors = ndb.LocalStructuredProperty(instructor.Instructor, repeated=True)
        policies = ndb.LocalStructuredProperty(policy.Policy, repeated=True)
        assessments = ndb.LocalStructuredProperty(assessment.Assessment, repeated=True)