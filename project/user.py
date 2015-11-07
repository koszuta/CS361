import Course
import Policy
import Scale
import Instructor

from google.appengine.ext import ndb

class User(ndb.Model):
        username = ndb.StringProperty()
        password = ndb.StringProperty()
        courses = ndb.StructuredProperty(Course, repeated=True)
        savedPolicies = ndb.StructuredProperty(Policy, repeated=True)
        savedScales = ndb.StructuredProperty(Scale, repeated=True)
        savedInstructors = ndb.StructuredProperty(Instructor, repeated=True)
    
'''    
    def addCourse(self, Course):
        
        return Course
'''