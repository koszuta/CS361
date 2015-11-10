import Course

class User:
    def __init__(self, username='', password='', courses={}, policies={}, scales={}, instructors={}):
        self.username = username
        self.password = password
        self.courses = courses
        self.policies = policies
        self.scales = scales
        self.instructors = instructors
        
    def addCourse(self, Course):
        
        return Course