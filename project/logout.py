import webapp2
import jinja2
import os
from webapp2_extras import auth

from basehandler import BaseHandler, login_required
from user import User

template_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.getcwd())
    )
    
class LogoutHandler(BaseHandler):
	@login_required
	def get(self):
		self.session['term'] = None
		self.session['syllabus'] = None
		self.auth.unset_session
		self.redirect('/login')