import os
import webapp2
import urllib
from jinja2 import Environment, FileSystemLoader
from google.appengine.ext import ndb

import hours
import syllabus
import user

class Instructor(ndb.Model):
    first = ndb.StringProperty(required=True)
    last = ndb.StringProperty(required=True)
    email = ndb.StringProperty()
    phone = ndb.StringProperty()
    building = ndb.StringProperty()
    room = ndb.StringProperty()
    #hours = ndb.LocalStructuredProperty(hours.Hours, repeated=True)
    isSelected = ndb.BooleanProperty()
    
    def key(self):
        return str(self.last + ", " + self.first);

           
class AddHandler(webapp2.RequestHandler):
    def post(self):
        option = self.request.get("instructorToAddButton")
        selected = self.request.get("availableInstructors")
        chosen = Instructor(first="Boner", last="Butts")
        
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
        chosen = instructor.Instructor(first="Butts", last="Boner")
        
        for item in syl.instructors:
            if item.key() == selected:
                chosen=item
                syl.instructors.remove(item) 
                
        chosen.isSelected = True  
           
        self.redirect('/#administratorViewInstructorInfoMain')
        
       
class EditHandler(webapp2.RequestHandler):
    def post(self):
        option = self.request.get("editInstructorSubmit")
        myfirst = self.request.get("instructorFirstName")
        mylast = self.request.get("instrcutorLastName")
        myemail = self.request.get("instructorEmail")
        myphone = self.request.get("instructorPhone")
        mybuilding = self.request.get("instructorBuildingSelect")
        myroom = self.request.get("instructorOfficeRoom")
        
        chosen = instructor.Instructor(first="Boner", last="Butts")
        
        for item in syl.instructors:
            if item.isSelected:
                chosen=item
                
        if option == "Update Info":
            chosen.first = myfirst
            chosen.last = mylast
            chosen.email = myemail
            chosen.phone = myphone
            chosen.building = mybuilding
            chosen.room = myroom
            
        elif option == "Create New":
            user.savedInstructors.append(instructor.Instructor(first = myfirst, last = mylast, email = myemail, phone = myphone, building = mybuilding, room = myroom))

        self.redirect('/#administratorViewInstructorInfoMain')