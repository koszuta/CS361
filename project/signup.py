import webapp2
import jinja2
import re
import os
from webapp2_extras import auth

from basehandler import BaseHandler
from user import User

template_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.getcwd())
    )
    
'''	
from wtforms import Form, TextField, PasswordField, validators

class SignupForm(Form):
    email = TextField('Email', 
                    [validators.Required(), 
                     validators.Email()])
    password = PasswordField('Password', 
                    [validators.Required(), 
                     validators.EqualTo('confirm_password', 
                                    message="Passwords must match.")])
    password_confirm = PasswordField('Confirm Password', 
                        [validators.Required()])
'''

class SignupHandler(BaseHandler):
    def render(self, errors = None, username = ''):
        template = template_env.get_template('signup.html')
        context = {
            'errors': errors,
            'username': username
        }
        self.response.write(template.render(context))

    def get(self):
        self.render()

    def post(self):
        username = self.request.get('usernameSignup')
        email = self.request.get('emailSignup')
        password = self.request.get('passwordSignup')
        confirm = self.request.get('confirmSignup')
        errors = []

        if not username:
            errors.append('Username field must not be empty')
        elif len(username) < 3:
            errors.append('Username must be at least 3 characters long')
        elif self.auth.store.user_model.get_by_auth_id(username):
            errors.append('Username "' + username + '" already exists')
        elif not re.match('^[\w_]+$', username):
            errors.append('Username must only contain alphanumeric characters (letters A-Z or numbers 0-9) or underscores (_)')
        if not password:
            errors.append('Password field must not be empty')
        elif len(password) < 8:
            errors.append('Password must be at least 8 characters long')
        if password != confirm:
            errors.append('Password and Confirm Password fields must match')

        if errors:
            return self.render(errors, username)

        success, info = self.auth.store.user_model.create_user(username, password_raw = password)

        if success:
            return self.redirect('/login')

        return self.render(['Unexpected error creating user'])
