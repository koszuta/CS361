import webapp2
import jinja2
import os

from google.appengine.ext import ndb

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
        syl.put()
        self.redirect('/editinstructor')
        
        
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
        syl.put()
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
        
        syl.put()   
        self.redirect('/editinstructor')