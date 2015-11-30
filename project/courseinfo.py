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
    days = ndb.StringProperty(repeated = True)
    start = ndb.TimeProperty()
    end = ndb.TimeProperty()
    
    
from basehandler import BaseHandler, login_required

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
        
        title = str(self.request.get('courseTitle'))
        
        syllabus.info.title = title
        syllabus.put()
        
        self.redirect('/editinfo')
      