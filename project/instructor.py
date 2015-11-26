import webapp2
import jinja2
import os
from google.appengine.ext import ndb

template_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.getcwd())
    )          
            
class Instructor(ndb.Model):
    first = ndb.StringProperty()
    last = ndb.StringProperty()
    email = ndb.StringProperty()
    phone = ndb.StringProperty()
    building = ndb.StringProperty()
    room = ndb.StringProperty()
    hours = ndb.StringProperty()
    isSelected = ndb.BooleanProperty()
    
    def name(self):
        if self.last == "" or self.last is None or self.first == "" or self.last is None:
            return None
        return self.last + ", " + self.first
        
    def copy(self):
        return Instructor(first = self.first, last = self.last, email = self.email, phone = self.phone, building = self.building, room = self.room, isSelected = self.isSelected)
    
    
from basehandler import BaseHandler
from syllabus import Syllabus
from term import Term
from user import User  
      
class EditHandler(BaseHandler):
    def get(self):
        userKey = self.session.get('user')
        user = ndb.Key(urlsafe = userKey).get()
        syllabusKey = self.session.get('syllabus')
        syllabus = ndb.Key(urlsafe = syllabusKey).get()        
        
        selected = Instructor.query(ancestor = user.key).filter(Instructor.isSelected == True).get()
        if not selected:
            selected = Instructor(parent = user.key)
                
        template = template_env.get_template('instructorEdit.html')
        context = {
            'savedInstructors': Instructor().query(ancestor = user.key).fetch(),
            'syllabusInstructors': Instructor().query(ancestor = syllabus.key).fetch(),
            'selected': selected.name(),
            'sel_first': selected.first,
            'sel_last': selected.last,
            'sel_email': selected.email,
            'sel_phone': selected.phone,
            'sel_building': selected.building,
            'sel_room': selected.room,
            'sel_hours': selected.hours,
        }

        self.response.write(template.render(context))
        
    def post(self):
        userKey = self.session.get('user')
        user = ndb.Key(urlsafe = userKey).get()
        
        option = self.request.get("editInstructorSubmit")
        myfirst = self.request.get("instructorFirstName")
        mylast = self.request.get("instructorLastName")
        myemail = self.request.get("instructorEmail")
        myphone = self.request.get("instructorPhone")
        mybuilding = self.request.get("instructorBuildingSelect")
        myroom = self.request.get("instructorOfficeRoom")
                        
        if option == "Update Info":
            i = Instructor.query(ancestor = user.key).filter(Instructor.isSelected == True).get()
        elif option == "Create New":
            i = Instructor(parent = user.key)
        
        if i:    
            i.first = myfirst
            i.last = mylast
            i.email = myemail
            i.phone = myphone
            i.building = mybuilding
            i.room = myroom
            i.isSelected = True
            i.put()
            
        self.redirect('/editinstructor')
        
        
class AddHandler(BaseHandler):
    def post(self):
        userKey = self.session.get('user')
        user = ndb.Key(urlsafe = userKey).get()
        syllabusKey = self.session.get('syllabus')
        syllabus = ndb.Key(urlsafe = syllabusKey).get()
        
        option = self.request.get("instructorToAddButton")
        selected = self.request.get("availableInstructors")
        
        temp = Instructor()
        
        for before in Instructor.query(ancestor = user.key).filter().fetch():
            before.isSelected = False
            if before.name() == selected:
                before.isSelected = True
                temp = before
            before.put()
            
        if option == "Add":
            new = Instructor(parent = syllabus.key, first = temp.first, last = temp.last, email = temp.email, phone = temp.phone, building = temp.building, room = temp.room, isSelected = temp.isSelected)
            temp.key.delete()
            new.put()
            
        self.redirect('/editinstructor')
        

class RemoveHandler(BaseHandler):        
    def post(self):
        syllabusKey = self.session.get('syllabus')
        syllabus = ndb.Key(urlsafe = syllabusKey).get()
        
        selected = self.request.get("selectedInstructors")
        
        for i in Instructor.query(ancestor = syllabus.key).fetch():
            if i.name() == selected:
                chosen = i
                ndb.delete(chosen)
            i.isSelected = False
         
        self.redirect('/editinstructor')