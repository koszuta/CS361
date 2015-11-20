import webapp2
import jinja2
import os

from google.appengine.ext import ndb

import login
import user
import course
import syllabus
import instructor
import textbook
import calendarEdit
import scalesEdit
import assessment
import policy

    
template_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.getcwd())
    )

def getCurrent():
    for u in user.User.query().fetch():
        if u.isActive:
            return u

class MainHandler(webapp2.RequestHandler):
    def get(self):
        
        currentUser = None
        users = user.User.query().fetch()
        for u in users:
            if u.isActive:
                currentUser = u
            
        if not currentUser:
            self.redirect("/login")
            
        template = template_env.get_template('main.html')
        context = {
            'books': textbook.Textbook.query().fetch(),
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
], debug=True)