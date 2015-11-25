import webapp2
import jinja2
import os

from google.appengine.api import oauth

import user

from basehandler import BaseHandler

template_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.getcwd())
    )
    
class LoginHandler(BaseHandler):
    def get(self):
                
        template = template_env.get_template('login.html')
        context = {
            
        }
        self.response.write(template.render(context))
        
    def post(self):
        u = self.request.get("usernameLogin")
        p = self.request.get("passwordLogin")
        
        current = matchUser(u, p)
        if current:
            current.isActive = True
            current.put()
            self.redirect("/")
        else:
            self.redirect("/login")

def matchUser(username, password):
    users = user.User.query().fetch()
    for u in users:
        if u.username == username and u.password == password:
            return u
    return None