import webapp2
import jinja2
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
    def get(self):
        template = template_env.get_template('signup.html')
        context = {
            
        }
        self.response.write(template.render(context))
        
    def post(self):
        username = self.request.get('usernameSignup')
        email = self.request.get('emailSignup')
        password = self.request.get('passwordSignup')
        confirm = self.request.get('confirmSignup')
        
        if password != confirm:
            self.redirect('/signup')
        
        success, info = self.auth.store.user_model.create_user(username, password_raw = password)
        
        if success:
            return self.redirect('/login')
        else:
            '''
            Errors errors errors
            '''
            print "error"
        
        self.redirect('/signup')