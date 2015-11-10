import webapp2
import jinja2
import os
import time

from google.appengine.ext import ndb

import user
import course
import syllabus
import instructor
import textbook
import calendarEdit
import scalesEdit
import assessment

user = user.User()
user.put()
syl = syllabus.Syllabus()
syl.put()

scott = instructor.Instructor(first='Scott', last='Ehlert', email='scott@uwm.edu', phone='(414) 555-1234', building='PHY', room='333', hours='MW 11am', isSelected=False) 
dylan = instructor.Instructor(first='Dylan', last='Harrison', email='dylan@uwm.edu', phone='(414) 555-9999', building='LAPH', room='150', hours='MWF 2pm', isSelected=False) 
nathan = instructor.Instructor(first='Nathan', last='Koszuta', email='nkoszuta@uwm.edu', phone='(414) 531-7488', building='CHEM', room='147', hours='MWR 10am', isSelected=False) 
shane = instructor.Instructor(first='Shane', last='Sedgwick', email='shane@uwm.edu', phone='(262) 555-0101', building='EMS', room='E190', hours='TR 12pm', isSelected=False)

p = assessment.Assessment(title="Project", percentage=40, description="The course project is implemented in phases by small groups of students. There are several phases of creating and refining deliverables such as requirements specifications, design documents, etc.")

user.savedAssessments.append(p)

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
                
        ilist = []
        for i in syl.instructors:
            ilist.append(i)
            
        alist = []
        for i in syl.assessments:
            alist.append(i)
            
        template = template_env.get_template('main.html')
        context = {
            'books': textbook.Textbook.query().fetch(),
            'instructors': ilist,
            'assessments': alist,
        }
        
        self.response.write(template.render(context))

           
class AddHandler(webapp2.RequestHandler):
    def post(self):
        option = self.request.get("instructorToAddButton")
        selected = self.request.get("availableInstructors")
        chosen = instructor.Instructor()
        
        for item in user.savedInstructors:
            if item.key() == selected:
                chosen = item
            item.isSelected = False
        
        if option == "Add":
            syl.instructors.append(chosen)
        
        chosen.isSelected = True
        
        chosen.put()
        self.redirect('/editinstructor')
        

class RemoveHandler(webapp2.RequestHandler):        
    def post(self):
        selected = self.request.get("selectedInstructors")
        chosen = instructor.Instructor()
        
        for item in syl.instructors:
            if item.key() == selected:
                chosen=item
                syl.instructors.remove(item) 
            item.isSelected = False
                
        chosen.isSelected = True  
           
        self.redirect('/editinstructor')
        
       
class EditHandler(webapp2.RequestHandler):
    def get(self):
        x = instructor.Instructor()
        for item in user.savedInstructors:
            if item.isSelected:
                x = item.copy()
            
        template = template_env.get_template('instructorEdit.html')
        
        context = {
            'savedInstructors': user.savedInstructors,
            'syllabusInstructors': syl.instructors,
            'selected': x.key(),
            'sel_first': x.first,
            'sel_last': x.last,
            'sel_email': x.email,
            'sel_phone': x.phone,
            'sel_building': x.building,
            'sel_room': x.room,
            'sel_hours': x.hours,
        }

        self.response.write(template.render(context))
        
    def post(self):
        option = self.request.get("editInstructorSubmit")
        
        myfirst = self.request.get("instructorFirstName")
        mylast = self.request.get("instructorLastName")
        myemail = self.request.get("instructorEmail")
        myphone = self.request.get("instructorPhone")
        mybuilding = self.request.get("instructorBuildingSelect")
        myroom = self.request.get("instructorOfficeRoom")
        
        chosen = instructor.Instructor()
                
        if option == "Update Info":
            for item in user.savedInstructors:
                if item.isSelected:
                    item.first = myfirst
                    item.last = mylast
                    item.email = myemail
                    item.phone = myphone
                    item.building = mybuilding
                    item.room = myroom
        
        elif option == "Create New":
            chosen.first = myfirst
            chosen.last = mylast
            chosen.email = myemail
            chosen.phone = myphone
            chosen.building = mybuilding
            chosen.room = myroom
            
            user.savedInstructors.append(chosen) 

        chosen.put()
        self.redirect('/editinstructor')
        
    
class AssessmentHandler(webapp2.RequestHandler):
    def get(self):
        x = assessment.Assessment()
        for item in user.savedAssessments:
            if item.isSelected:
                x = item.copy()
            
        template = template_env.get_template('assessmentEdit.html')
        
        context = {
            'savedAssessments': user.savedAssessments,
            'selected': x.key(),
            'assessments': syl.assessments,
            'title': x.title,
            'description': x.description,
            'percentage': x.percentage,
        }

        self.response.write(template.render(context))
        
    def post(self):
        
        self.redirect('/editassessments')
        
        
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/addinstructor', AddHandler),
    ('/removeinstructor', RemoveHandler),
    ('/editinstructor', EditHandler),
    ('/editbooks', textbook.TextbookHandler),
    ('/editbook', textbook.EditTextbookHandler),
    ('/removebooks', textbook.RemoveTextbookHandler),
    ('/editcalendar', calendarEdit.CalendarHandler),
    ('/editscales', scalesEdit.ScalesHandler),
    ('/editassessments', AssessmentHandler),
], debug=True)