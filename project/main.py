import webapp2
import jinja2
import os

from google.appengine.ext import ndb

import user
import course
import syllabus
import instructor
import hours

h = hours.Hours(day="Monday", start="9:00am", end="11:00am")
i = hours.Hours(day="Wednesday", start="1:00pm", end="2:00pm")
j = hours.Hours(day="Thursday", start="10:00am", end="11:00am")

scott = instructor.Instructor(first='Scott', last='Ehlert', hours=[h, i]) 
dylan = instructor.Instructor(first='Dylan', last='Harrison', hours=[h, i, j]) 
nathan = instructor.Instructor(first='Nathan', last='Koszuta', email='nkoszuta@uwm.edu', phone='(414) 531-7488', building='CHEM', room='147', hours=[h, i, j]) 
shane = instructor.Instructor(first='Shane', last='Sedgwick', hours=[h]) 

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