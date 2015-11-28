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
    def get(self):
        template = template_env.get_template('login.html')
        context = {
            
        }
        self.response.write(template.render(context))
        
    def post(self):
        username = self.request.get('usernameLogin')
        password = self.request.get('passwordLogin')
        
        try:
            u = self.auth.get_user_by_password(username, password, remember = True)
            self.redirect('/main')
        except (auth.InvalidAuthIdError, auth.InvalidPasswordError) as e:
            #logging.info('Login failed for user %s because of %s', username, type(e))
            self._serve_page(True)
            
    def _serve_page(self, failed = False):
        username = self.request.get('username')
        params = {
            'username': username,
            'failed': failed,
        }
        self.render_template('login.html', params)