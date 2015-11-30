import webapp2
import jinja2
import os
from google.appengine.ext import ndb

class Info(ndb.Model):
    title = ndb.StringProperty()
    subject = ndb.StringProperty()
    number = ndb.IntegerProperty()
    section = ndb.IntegerProperty()
    building = ndb.StringProperty()
    room = ndb.StringProperty()
    days = ndb.StringProperty()
    start = ndb.StringProperty()
    end = ndb.StringProperty()
    
    
from basehandler import BaseHandler, login_required

template_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.getcwd())
    )  
    
class InfoEditHandler(BaseHandler):
    @login_required
    def get(self):
        syllabusKey = self.session.get('syllabus')
        syllabus = ndb.Key(urlsafe = syllabusKey).get()
        
        template = template_env.get_template('courseInfoEdit.html')
        context = {
            'info': syllabus.info
        }

        self.response.write(template.render(context))
        
    @login_required
    def post(self):
        syllabusKey = self.session.get('syllabus')
        syllabus = ndb.Key(urlsafe = syllabusKey).get()
        
        subject = str(self.request.get('subjectSelect'))
        syllabus.info.subject = subject
        
        number = int(self.request.get('courseNumber'))
        syllabus.info.number = number
        
        section = int(self.request.get('sectionNumber'))
        syllabus.info.section = section
        
        title = str(self.request.get('courseTitle'))
        syllabus.info.title = title
        
        days = ""
        monday = str(self.request.get('mondayCheck'))
        days = days + monday
        tuesday = str(self.request.get('tuesdayCheck'))
        days = days + tuesday
        wednesday = str(self.request.get('wednesdayCheck'))
        days = days + wednesday
        thursday = str(self.request.get('thursdayCheck'))
        days = days + thursday
        friday = str(self.request.get('fridayCheck'))
        days = days + friday
        syllabus.info.days = days
        
        start = str(self.request.get('startTime'))
        syllabus.info.start = start
        
        end = str(self.request.get('endTime'))
        syllabus.info.end = end
        
        building = str(self.request.get('meetingBuilding'))
        syllabus.info.building = building
        
        room = str(self.request.get('meetingRoom'))
        syllabus.info.room = room
        
        syllabus.put()
        
        self.redirect('/editinfo')
      