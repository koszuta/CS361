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
    isSelected = ndb.BooleanProperty()
    onSyllabus = ndb.BooleanProperty(default = False)
    @property
    def hours(self):
        return Hours.query(ancestor = self.key).fetch()
    
    def hours_start(self, day):
        hour = Hours.query(ancestor = self.key).filter(Hours.day == day).get()
        if hour:
            return hour.start
        return None
    
    def hours_end(self, day):
        hour = Hours.query(ancestor = self.key).filter(Hours.day == day).get()
        if hour:
            return hour.end
        return None
    
    def name(self):
        return self.last + ', ' + self.first if (self.first and self.last) else None
        
    def copy(self):
        return Instructor(first = self.first, last = self.last, email = self.email, phone = self.phone, building = self.building, room = self.room, hours = self.hours, isSelected = self.isSelected)
   
class Hours(ndb.Model):
    day = ndb.StringProperty()
    start = ndb.StringProperty()
    end = ndb.StringProperty()
     
    
from basehandler import BaseHandler, login_required
from syllabus import Syllabus
from term import Term
from user import User 

template_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.getcwd())
    )  
  
      
class EditHandler(BaseHandler):
    @login_required	 
    def get(self):
        user = self.current_user
        syllabus = self.current_syllabus        
        
        selected = Instructor.query(ancestor = user.key).filter(Instructor.isSelected == True).get()
                        
        template = template_env.get_template('instructor.html')
        context = {
            'savedInstructors': user.savedInstructors,
            'syllabusInstructors': syllabus.instructors,
        }
        
        if selected:
            context['selected'] = selected.name()
            context['sel_first'] = selected.first
            context['sel_last'] = selected.last
            context['sel_email'] = selected.email
            context['sel_phone'] = selected.phone
            context['sel_building'] = selected.building
            context['sel_room'] = selected.room
            context['monday'] = Hours.query(ancestor = selected.key).filter(Hours.day == 'Monday').get()
            context['tuesday'] = Hours.query(ancestor = selected.key).filter(Hours.day == 'Tuesday').get()
            context['wednesday'] = Hours.query(ancestor = selected.key).filter(Hours.day == 'Wednesday').get()
            context['thursday'] = Hours.query(ancestor = selected.key).filter(Hours.day == 'Thursday').get()
            context['friday'] = Hours.query(ancestor = selected.key).filter(Hours.day == 'Friday').get()
            

        self.response.write(template.render(context))
        
    @login_required	 
    def post(self):
        user = self.current_user
        
        option = self.request.get('editInstructorSubmit')
        myfirst = self.request.get('instructorFirstName')
        mylast = self.request.get('instructorLastName')
        myemail = self.request.get('instructorEmail')
        myphone = self.request.get('instructorPhone')
        mybuilding = self.request.get('instructorBuildingSelect')
        myroom = self.request.get('instructorOfficeRoom')
                        
        if option == 'Update Info':
            i = Instructor.query(ancestor = user.key).filter(Instructor.isSelected == True).get()
        elif option == 'Create New':
            i = Instructor(parent = user.key)
            
        i.put()
            
        if self.request.get('mondayCheck'):
            start = self.request.get('mondayStartTime')
            end = self.request.get('mondayEndTime')
            old = Hours.query(ancestor = i.key).filter(Hours.day == "Monday").get()
            if old:
                old.key.delete()
            new = Hours(parent = i.key, day = "Monday", start = start, end = end)
            new.put()
        else:
            old = Hours.query(ancestor = i.key).filter(Hours.day == "Monday").get()
            if old:
                old.key.delete()            
        if self.request.get('tuesdayCheck'):
            start = self.request.get('tuesdayStartTime')
            end = self.request.get('tuesdayEndTime')
            old = Hours.query(ancestor = i.key).filter(Hours.day == "Tuesday").get()
            if old:
                old.key.delete()
            new = Hours(parent = i.key, day = "Tuesday", start = start, end = end)
            new.put()
        else:
            old = Hours.query(ancestor = i.key).filter(Hours.day == "Tuesday").get()
            if old:
                old.key.delete()
        if self.request.get('wednesdayCheck'):
            start = self.request.get('wednesdayStartTime')
            end = self.request.get('wednesdayEndTime')
            old = Hours.query(ancestor = i.key).filter(Hours.day == "Wednesday").get()
            if old:
                old.key.delete()
            new = Hours(parent = i.key, day = "Wednesday", start = start, end = end)
            new.put()   
        else:
            old = Hours.query(ancestor = i.key).filter(Hours.day == "Wednesday").get()
            if old:
                old.key.delete()
        if self.request.get('thursdayCheck'):
            start = self.request.get('thursdayStartTime')
            end = self.request.get('thursdayEndTime')
            old = Hours.query(ancestor = i.key).filter(Hours.day == "Thursday").get()
            if old:
                old.key.delete()
            new = Hours(parent = i.key, day = "Thursday", start = start, end = end)
            new.put()
        else:
            old = Hours.query(ancestor = i.key).filter(Hours.day == "Thursday").get()
            if old:
                old.key.delete()
        if self.request.get('fridayCheck'):
            start = self.request.get('fridayStartTime')
            end = self.request.get('fridayEndTime')
            old = Hours.query(ancestor = i.key).filter(Hours.day == "Friday").get()
            if old:
                old.key.delete()
            new = Hours(parent = i.key, day = "Friday", start = start, end = end)
            new.put()
        else:
            old = Hours.query(ancestor = i.key).filter(Hours.day == "Friday").get()
            if old:
                old.key.delete()
            
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
    @login_required	 
    def post(self):
        user = self.current_user
        syllabus = self.current_syllabus
        
        option = self.request.get('instructorToAddButton')
        selected = self.request.get('availableInstructors')
        
        temp = Instructor()
        
        for before in user.savedInstructors:
            before.isSelected = False
            if before.name() == selected:
                before.isSelected = True
                temp = before
            before.put()
            
        if option == 'Add':
            new = Instructor(parent = syllabus.key, first = temp.first, last = temp.last, email = temp.email, phone = temp.phone, building = temp.building, room = temp.room, isSelected = temp.isSelected, onSyllabus = True)
            new.put()
            for h in temp.hours:
                hour = Hours(parent = new.key, day = h.day, start = h.start, end = h.end)
                hour.put()
            
        self.redirect('/editinstructor')
        

class RemoveHandler(BaseHandler):    
    @login_required	     
    def post(self):
        syllabus = self.current_syllabus
        
        selected = self.request.get('selectedInstructors')
        
        for i in syllabus.instructors:
            if i.name() == selected:
                chosen = i
                chosen.key.delete()
            i.isSelected = False
         
        self.redirect('/editinstructor')