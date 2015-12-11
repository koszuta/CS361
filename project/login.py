import webapp2
import jinja2
import os
from webapp2_extras import auth

from basehandler import BaseHandler
from user import User

template_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.getcwd())
    )
    
class LoginHandler(BaseHandler):
    def render(self, errors = None):
        template = template_env.get_template('login.html')
        context = {
            'errors': errors
        }
        self.response.write(template.render(context))

    def get(self):
        self.render()

    def post(self):
        self.auth.unset_session()
        self.session.clear()

        username = self.request.get('usernameLogin')
        password = self.request.get('passwordLogin')

        try:
            self.auth.get_user_by_password(username, password)          
            return self.redirect('/list')
            
        except (auth.InvalidAuthIdError, auth.InvalidPasswordError) as e:
            return self.render(['Invalid username and/or password'])
