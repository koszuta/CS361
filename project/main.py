import webapp2
import jinja2
import os
import time

from google.appengine.ext import ndb

import user
import course
import syllabus
import instructor
import hours

user = user.User()
user.put()
syl = syllabus.Syllabus()
syl.put()

scott = instructor.Instructor(first='Scott', last='Ehlert') 
dylan = instructor.Instructor(first='Dylan', last='Harrison') 
nathan = instructor.Instructor(first='Nathan', last='Koszuta', email='nkoszuta@uwm.edu', phone='(414) 531-7488', building='CHEM', room='147') 
shane = instructor.Instructor(first='Shane', last='Sedgwick')

user.savedInstructors.append(scott)
user.savedInstructors.append(nathan)
user.savedInstructors.append(dylan)
user.savedInstructors.append(shane)

h = hours.Hours(day="Monday", start="9:00am", end="11:00am")
i = hours.Hours(day="Wednesday", start="1:00pm", end="2:00pm")
j = hours.Hours(day="Thursday", start="10:00am", end="11:00am")

    
template_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.getcwd())
    )
    
class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('''user.savedInstructors = ''')
        self.response.write(user.savedInstructors)
        self.response.write('''<br><br>''')
        self.response.write('''syl.instructors = ''')
        self.response.write(syl.instructors)
        self.response.write('''<br><br>''')
        
        x = scott
        
        template = template_env.get_template('main.html')
        context = {
            'savedInstructors': user.savedInstructors,
            'syllabusInstructors': syl.instructors,
            'sel_first': x.first,
            'sel_last': x.last,
            'sel_email': x.email,
            'sel_phone': x.phone,
            'sel_building': x.building,
            'sel_room': x.room,
            'sel_hours': x.hours,
        }
        
        self.response.write(template.render(context))

           
class AddHandler(webapp2.RequestHandler):
    def post(self):
        option = self.request.get("instructorToAddButton")
        chosen = self.request.get("availableInstructors")
        
        user.savedInstructors.append(instructor.Instructor(first="test2", last="test1"))
        
        if option == "Add":
            syl.instructors.append(chosen)
        elif option == "Edit":
            syl.instructors.remove(chosen)
        
        syl.put()
        self.redirect('/')
        

class RemoveHandler(webapp2.RequestHandler):        
    def post(self):
        keyToRemove = self.request.get("selectedInstructors")
        if keyToRemove is not None and keyToRemove != '':
            del onSyllabus[keyToRemove]       
            
        self.redirect('/')
        
       
class EditHandler(webapp2.RequestHandler):
    def post(self):
        
        self.redirect('/')
        
        
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/addinstructor', AddHandler),
    ('/removeinstructor', RemoveHandler),
    ('/editinstructor', EditHandler),
], debug=True)