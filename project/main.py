import webapp2
import jinja2
import os
from google.appengine.ext import ndb
from google.appengine.api import oauth

from basehandler import BaseHandler
       
from textbook import Textbook
from instructor import Instructor
from calendarClass import CalendarClass       

template_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.getcwd())
    )

class MainHandler(BaseHandler):
    def get(self):
        syllabusKey = self.session.get('syllabus')
        syllabus = ndb.Key(urlsafe = syllabusKey).get()

        template = template_env.get_template('main.html')
        context = {
            'books': Textbook.query(ancestor = syllabus.key).fetch(),
            'instructors': Instructor.query(ancestor = syllabus.key).fetch(),
            'ClassCalendar': CalendarClass.query(ancestor = syllabus.key).fetch() 
        }
        
        self.response.write(template.render(context))
               
import user    
import assessment
import instructor
import login
import calendarEdit
import policy
import preview
import scalesEdit
import textbook
import term
     
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
termRegex = '/([FfSsMmWw][0-9][0-9])'

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/login', login.LoginHandler),
    ('/signup', login.SignupHandler),
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
    ('/editassessment', assessment.EditHandler),
    ('/addassessment', assessment.AddHandler),
    ('/removeassessment', assessment.RemoveHandler),
    ('/editpolicy', policy.EditHandler),
    ('/addpolicy', policy.AddHandler),
    ('/removepolicy', policy.RemoveHandler),
    ('/preview', preview.PreviewHandler),
    (termRegex + '/*', term.WeeklyCalendarHandler),
    (termRegex + '/(.*)', preview.ViewHandler),
], debug=True, config=config)