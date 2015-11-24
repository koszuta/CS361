import webapp2
import jinja2
import os

from google.appengine.api import oauth
from google.appengine.ext import ndb

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

def getCurrentUser():
    for u in user.User.query().fetch():
        return u
            
            
class MainHandler(webapp2.RequestHandler):
    def get(self):
        currentUser = getCurrentUser()
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
], debug=True)