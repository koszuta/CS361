import webapp2
import jinja2
import os
from webapp2_extras import auth
from wtforms import Form, TextField, PasswordField, validators

from basehandler import BaseHandler
from user import User

template_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.getcwd())
    )
    
	
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
        
        unique_properties = ['email_address']
        user_data = self.user_model.create_user(username, unique_properties, email_address = email, password_raw = password, verified = False)
        
        if not user_data[0]:
            self.display_message('Unable to create user for email %s because of duplicate keys %s' % (user_name, user_data[1]))
            return
            
        user = user_data[1]
        user_id = user.get_id()
        
        token = self.user_model.create_signup_token(user_id)
        
        ver_url = self.uri_for('verification', type = 'v', user_id = user_id, signup_token = token, _full = True)
        
        msg = 'Send an email to user in order to verify their address. They will be able to do so by visiting <a href="{ url }"> { url } </a>'
        
        self.display_message(msg.format(url = ver_url))