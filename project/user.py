import course
import policy
import scale
import Instructor

from google.appengine.ext import ndb

class User(ndb.Model):
        username = ndb.StringProperty()
        password = ndb.StringProperty()
        courses = ndb.LocalStructuredProperty(course, repeated=True)
        savedPolicies = ndb.LocalStructuredProperty(policy, repeated=True)
        savedScales = ndb.LocalStructuredProperty(scale, repeated=True)
        savedInstructors = ndb.LocalStructuredProperty(Instructor, repeated=True)
    
'''    
    def addCourse(self, Course):
        
        return Course
'''