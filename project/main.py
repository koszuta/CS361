import webapp2
import jinja2
import os
from google.appengine.ext import ndb

from basehandler import BaseHandler, login_required
       
from textbook import Textbook
from instructor import Instructor
from calendarClass import CalendarClass       

template_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.getcwd())
    )

class MainHandler(BaseHandler):
    @login_required
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
            'scale': syllabus.scale,
            'calendar': syllabus.calendars,
            'assessments': syllabus.assessments,
            'info': syllabus.info
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
import term
import courseinfo
     
config = {}
config['webapp2_extras.auth'] = {
    'user_model': user.User,
}
config['webapp2_extras.sessions'] = {
    'secret_key': 'secret_key',
}

# Regular expression to match a URL starting with a term name
# [FfSsMmWw] - any one these characters may appear (case insensitive)
#              F (Fall), S (Spring), M (Summer), W (Winterim)
# [0-9][0-9] - two digit number for the year
termRegex = '/(.+)/([FfSsMmWw][0-9][0-9])'

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/login', login.LoginHandler),
    ('/signup', signup.SignupHandler),
    ('/logout', logout.LogoutHandler),
    ('/list', lister.ListerHandler),
    ('/createsyllabus', lister.CreateSyllabusHandler),
    ('/selectsyllabus', lister.SelectSyllabusHandler),
    ('/termselect', lister.TermSelectHandler),
    ('/addinstructor', instructor.AddHandler),
    ('/removeinstructor', instructor.RemoveHandler),
    ('/editinstructor', instructor.EditHandler),
    ('/addbooks', textbook.AddTextbookHandler),
    ('/editbooks', textbook.TextbookHandler),
    ('/editbook', textbook.EditTextbookHandler),
    ('/findbook', textbook.FindTextbookHandler),
    ('/removebooks', textbook.RemoveTextbookHandler),
    ('/editcalendar', calendarEdit.CalendarHandler),
    ('/editscales', scalesEdit.ScalesHandler),
    #('/addscale', scalesEdit.AddScalesHandler),
    ('/editassessment', assessment.EditHandler),
    ('/addassessment', assessment.AddHandler),
    ('/removeassessment', assessment.RemoveHandler),
    ('/editpolicy', policy.EditHandler),
    ('/addpolicy', policy.AddHandler),
    ('/removepolicy', policy.RemoveHandler),
    ('/preview', preview.PreviewHandler),
    ('/editinfo', courseinfo.InfoEditHandler),
    (termRegex + '/*', term.WeeklyCalendarHandler),
    (termRegex + '/(.*)', preview.ViewHandler),
], debug=True, config=config)