import Syllabus

from google.appengine.ext import ndb

class Course:
    def __init__(self, name='', number='', syllabi={}, calendars={}, textbooks={}):
        self.name = name
        self.number = number
        self.syllabi = syllabi
        self.calendars = calendars
        self.textbooks = textbooks
        
    def addSyllabus(self, Syllabus):
        
        return Syllabus