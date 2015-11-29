import webapp2
import jinja2
import os
from webapp2_extras import auth
from webapp2_extras.appengine.users import login_required

from basehandler import BaseHandler
from user import User

template_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.getcwd())
    )
    
#@login_required
class LogoutHandler(BaseHandler):
	def get(self):
		self.auth.unset_session
		self.redirect('/login')