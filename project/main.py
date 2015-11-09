import webapp2
import jinja2
import os
import time

from google.appengine.ext import ndb

import user
import course
import syllabus
import Instructor
import Hours

from Textbook import TextbookHandler, EditTextbookHandler

user = user.User()
user.put()
syl = syllabus.Syllabus()
syl.put()

scott = Instructor.Instructor(first='Scott', last='Ehlert', isSelected=False) 
dylan = Instructor.Instructor(first='Dylan', last='Harrison', isSelected=False) 
nathan = Instructor.Instructor(first='Nathan', last='Koszuta', email='nkoszuta@uwm.edu', phone='(414) 531-7488', building='CHEM', room='147', isSelected=False) 
shane = Instructor.Instructor(first='Shane', last='Sedgwick', isSelected=False)

user.savedInstructors.append(scott)
user.savedInstructors.append(nathan)
user.savedInstructors.append(dylan)
user.savedInstructors.append(shane)

'''
h = hours.Hours(day="Monday", start="9:00am", end="11:00am")
i = hours.Hours(day="Wednesday", start="1:00pm", end="2:00pm")
j = hours.Hours(day="Thursday", start="10:00am", end="11:00am")
'''
    
template_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.getcwd())
    )

class MainHandler(webapp2.RequestHandler):
    def get(self):
        x = Instructor.Instructor(first="Butts", last="Boner", email="fake@fake.com", phone="(555) 123-1234", isSelected=True)
        for item in user.savedInstructors:
            if item.isSelected:
                x = item
            item.isSelected = False
        
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
            #'sel_hours': x.hours,
        }
        
        self.response.write(template.render(context))

           
class AddHandler(webapp2.RequestHandler):
    def post(self):
        option = self.request.get("instructorToAddButton")
        selected = self.request.get("availableInstructors")
        chosen = Instructor.Instructor(first="Butts", last="Boner")
        
        for item in user.savedInstructors:
            if item.key() == selected:
                chosen = item
        
        if option == "Add":
            syl.instructors.append(chosen)
        
        chosen.isSelected = True        
        
        self.redirect('/#administratorViewInstructorInfoMain')
        

class RemoveHandler(webapp2.RequestHandler):        
    def post(self):
        selected = self.request.get("selectedInstructors")
        chosen = Instructor.Instructor(first="Butts", last="Boner")
        
        for item in syl.instructors:
            if item.key() == selected:
                chosen=item
                syl.instructors.remove(item) 
                
        chosen.isSelected = True  
           
        self.redirect('/#administratorViewInstructorInfoMain')
        
       
class EditHandler(webapp2.RequestHandler):
    def post(self):
        button = self.request.get("editInstructorSubmit")

        self.redirect('/#administratorViewInstructorInfoMain')
        
        
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/addinstructor', AddHandler),
    ('/removeinstructor', RemoveHandler),
    ('/editinstructor', EditHandler),
    ('/editbooks', TextbookHandler),
    ('/editbook', EditTextbookHandler),
], debug=True)