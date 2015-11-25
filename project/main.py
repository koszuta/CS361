import webapp2
import jinja2
import os

from google.appengine.api import oauth
from google.appengine.ext import ndb

from basehandler import BaseHandler

import login
import user
import term
import syllabus
import instructor
import textbook
import calendarEdit
import scalesEdit
import assessment
import policy
import preview
    
template_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.getcwd())
    )
      
class MainHandler(BaseHandler):
    def get(self):
        currentUser = user.User() # User BaseHandler stuff for this eventually
        currentUser.put()
        
        t = term.Term(parent = currentUser.key, semester = "Spring", year = 2016, isSelected = False)
        t.put()
         
        if not currentUser:
            self.redirect("/login")
            
        template = template_env.get_template('main.html')
        context = {
            'books': textbook.Textbook.query(ancestor = currentUser.key).fetch(),
            'instructors': instructor.Instructor.query(ancestor = currentUser.key).fetch(),
        }
        
        self.response.write(template.render(context))
      
         
config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'my-super-secret-key',
} 
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/login', login.LoginHandler),
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