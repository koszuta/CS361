import webapp2
import jinja2
import os

from google.appengine.api import oauth
from google.appengine.ext import ndb

from basehandler import BaseHandler

    
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