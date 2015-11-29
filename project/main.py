import webapp2
import jinja2
import os
from google.appengine.ext import ndb

from basehandler import BaseHandler
from webapp2_extras.appengine.users import login_required
       
from textbook import Textbook
from instructor import Instructor       

template_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.getcwd())
    )
    
#@login_required
class MainHandler(BaseHandler):
    def get(self):
        syllabusKey = self.session.get('syllabus')
        syllabus = ndb.Key(urlsafe = syllabusKey).get()

        if not syllabus:   
            return self.redirect('/list') 
            
        template = template_env.get_template('main.html')
        context = {
            'books': syllabus.textbooks,
            'instructors': syllabus.instructors,
            'policies': syllabus.policies,
            'scales': syllabus.scales,
            'calendars': syllabus.calendars,
            'assessments': syllabus.assessments,
        }
        
        self.response.write(template.render(context))
        
               
import user  
import signup 
import login 
import logout
import lister
import assessment
import instructor
import calendarEdit
import policy
import preview
import scalesEdit
import textbook    
     
config = {}
config['webapp2_extras.auth'] = {
    'user_model': user.User,
}
config['webapp2_extras.sessions'] = {
    'secret_key': 'secret_key',
} 
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/login', login.LoginHandler),
    ('/signup', signup.SignupHandler),
    ('/logout', logout.LogoutHandler),
    ('/list', lister.ListerHandler),
    ('/termselect', lister.TermSelectHandler),
    ('/addinstructor', instructor.AddHandler),
    ('/removeinstructor', instructor.RemoveHandler),
    ('/editinstructor', instructor.EditHandler),
    ('/editbooks', textbook.TextbookHandler),
    ('/editbook', textbook.EditTextbookHandler),
    ('/removebooks', textbook.RemoveTextbookHandler),
    ('/editcalendar', calendarEdit.CalendarHandler),
    ('/editscales', scalesEdit.ScalesHandler),
    ('/editassessment', assessment.EditHandler),
    ('/addassessment', assessment.AddHandler),
    ('/removeassessment', assessment.RemoveHandler),
    ('/editpolicy', policy.EditHandler),
    ('/addpolicy', policy.AddHandler),
    ('/removepolicy', policy.RemoveHandler),
    ('/preview', preview.PreviewHandler),
], debug=True, config=config)