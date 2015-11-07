import webapp2
import jinja2
import os

from google.appengine.ext import ndb

import User
import Course
import Syllabus
import Instructor


scott = Instructor.Instructor(first='Scott', last='Ehlert', email=None, phone=None, building=None, room=None, hours=None)
dylan = Instructor.Instructor(first='Dylan', last='Harrison', email=None, phone=None, building=None, room=None, hours=None)
nathan = Instructor.Instructor(first='Nathan', last='Koszuta', email='nkoszuta@uwm.edu', phone='(414) 531-7488', building='CHEM', room='147', hours=None)
shane = Instructor.Instructor(first='Shane', last='Sedgwick', email=None, phone=None, building=None, room=None, hours=None) 

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