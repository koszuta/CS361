import course
import policy
import scale
import instructor
import assessment

from google.appengine.ext import ndb

class User(ndb.Model):
        username = ndb.StringProperty()
        password = ndb.StringProperty()
        courses = ndb.LocalStructuredProperty(course.Course, repeated=True)
        savedPolicies = ndb.LocalStructuredProperty(policy.Policy, repeated=True)
        savedScales = ndb.LocalStructuredProperty(scale.Scale, repeated=True)
        savedInstructors = ndb.LocalStructuredProperty(instructor.Instructor, repeated=True)
        savedAssessments = ndb.LocalStructuredProperty(assessment.Assessment, repeated=True)