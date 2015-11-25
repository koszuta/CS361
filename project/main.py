import webapp2
import jinja2
import os
from google.appengine.ext import ndb
from google.appengine.api import oauth

from basehandler import BaseHandler
       
from textbook import Textbook
from instructor import Instructor       

template_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.getcwd())
    )
      
class MainHandler(BaseHandler):
    def get(self):
        template = template_env.get_template('main.html')
        context = {
            'books': Textbook.query(ancestor = self.session['syllabus'].key).fetch(),
            'instructors': Instructor.query(ancestor = self.session['syllabus'].key).fetch(),
        }
        
        self.response.write(template.render(context))