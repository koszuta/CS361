import webapp2
import jinja2
import os

from google.appengine.ext import ndb

import User
import Course
import Syllabus
import Instructor


scott = Instructor.Instructor('Scott', 'Ehlert', None, None, None, None, None)
dylan = Instructor.Instructor('Dylan', 'Harrison', None, None, None, None, None)
nathan = Instructor.Instructor('Nathan', 'Koszuta', 'nkoszuta@uwm.edu', '(414) 531-7488', 'CHEM', '147', None)
shane = Instructor.Instructor('Shane', 'Sedgwick', None, None, None, None, None) 

listoinstructors = {'Ehlert, Scott': scott, 'Harrison, Dylan': dylan, 'Koszuta, Nathan': nathan, 'Sedgwick, Shane': shane}
onSyllabus = {}

for key, value in listoinstructors.iteritems():
    onSyllabus[key] = value
template_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.getcwd())
    )
    
class MainHandler(webapp2.RequestHandler):
    def get(self):
        
        x = scott
        
        template = template_env.get_template('main.html')
        context = {
            'instructorsList': listoinstructors,
            'onSyllabus': onSyllabus,
            'sel_first': x.first,
            'sel_last': x.last,
            'sel_email': x.email,
            'sel_phone': x.phone,
            'sel_building': x.building,
            'sel_room': x.room,
            'sel_hours': x.hours,
        }
        
        self.response.write(template.render(context))
           
class EditHandler(webapp2.RequestHandler):
    def post(self):
        currentInstructor = self.request.get("availableInstructors")
        
        self.redirect('/')
        

class RemoveHandler(webapp2.RequestHandler):        
    def post(self):
        keyToRemove = self.request.get("selectedInstructors")
        if keyToRemove is not None and keyToRemove != '':
            del onSyllabus[keyToRemove]       
            
        self.redirect('/')
        
        
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/editinstructor', EditHandler),
    ('/removeinstructor', RemoveHandler),
], debug=True)