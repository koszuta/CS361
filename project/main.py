import webapp2
import jinja2
import os

from google.appengine.ext import ndb


template_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.getcwd())
    )
    
class MainHandler(webapp2.RequestHandler):
    def get(self):
        
        template = template_env.get_template('main.html')
        context = {
        }
        
        self.response.write(template.render(context))
        
        
app = webapp2.WSGIApplication([
    ('/', MainHandler),
], debug=True)