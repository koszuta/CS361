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
    
    def key(self):
        if self.last == "" or self.last is None or self.first == "" or self.last is None:
            return "nobody"
        return self.last + ", " + self.first
        
    def copy(self):
        return Instructor(first=self.first, last=self.last, email=self.email, phone=self.phone, building=self.building, room=self.room, isSelected=self.isSelected)
    
    
from basehandler import BaseHandler
from syllabus import Syllabus
from term import Term
from user import User  
      
class EditHandler(BaseHandler):
    def get(self):
        selected = Instructor()
        u = getUser()
        i = Instructor().query(ancestor = u.key).get()
                
        syl = syllabus.Syllabus()
        for t in term.Term().query(ancestor = u.key).fetch():
            if t.isSelected:
                syl = syllabus.Syllabus().query(ancestor = t.key).fetch()
            
        template = template_env.get_template('instructorEdit.html')
        context = {
            'savedInstructors': Instructor().query(ancestor = u.key).fetch(),
            'syllabusInstructors': Instructor().query(ancestor = syl.key).fetch(),
            'selected': selected.key(),
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
        option = self.request.get("editInstructorSubmit")
        
        myfirst = self.request.get("instructorFirstName")
        mylast = self.request.get("instructorLastName")
        myemail = self.request.get("instructorEmail")
        myphone = self.request.get("instructorPhone")
        mybuilding = self.request.get("instructorBuildingSelect")
        myroom = self.request.get("instructorOfficeRoom")
        
        chosen = Instructor()
                
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
        syl.put()
        self.redirect('/editinstructor')
        
        
class AddHandler(BaseHandler):
    def post(self):
        option = self.request.get("instructorToAddButton")
        selected = self.request.get("availableInstructors")
        chosen = Instructor()
        
        u = getCurrentUser()
        for i in Instructor.query(ancestor = u.key).fetch():
            if i.key() == selected:
                chosen = i
            i.isSelected = False
        
        if option == "Add":
            chosen.parent = syl.key
        
        chosen.isSelected = True
        
        chosen.put()
        syl.put()
        self.redirect('/editinstructor')
        

class RemoveHandler(BaseHandler):        
    def post(self):
        selected = self.request.get("selectedInstructors")
        chosen = instructor.Instructor()
        
        for item in syl.instructors:
            if item.key() == selected:
                chosen=item
                syl.instructors.remove(item) 
            item.isSelected = False
                
        chosen.isSelected = True  
        
        syl.put()   
        self.redirect('/editinstructor')