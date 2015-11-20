import webapp2
import jinja2
import os

from google.appengine.ext import ndb

import syllabus
import calendars
import textbook

class Policy(ndb.Model):
	title = ndb.StringProperty()
	description = ndb.TextProperty()
	isSelected = ndb.BooleanProperty()
	
	def copy(self):
		return Policy(title=self.title, description=self.description, isSelected=self.isSelected)
		
	def key(self):
		if self.title == "" or self.title is None:
			return "none"
			
		return self.title
	
		        
class EditHandler(webapp2.RequestHandler):
    def get(self):
        x = policy.Policy()
        for item in user.savedPolicies:
            if item.isSelected:
                x = item.copy()
            
        template = template_env.get_template('policyEdit.html')
        
        context = {
            'savedPolicies': user.savedPolicies,
            'selected': x.key(),
            'policies': syl.policies,
            'title': x.title,
            'description': x.description,
        }

        self.response.write(template.render(context))
        
    def post(self):
        option = self.request.get("policyEditorButton")
        
        mytitle = self.request.get("policyTitle")
        mydescription = self.request.get("policyDescription")
        
        chosen = policy.Policy()
                
        if option == "Update":
            for item in user.savedPolicies:
                if item.isSelected:
                    item.title = mytitle
                    item.description = mydescription
                    
        elif option == "Create New":
            chosen.title = mytitle
            chosen.description = mydescription
            
            user.savedPolicies.append(chosen) 

            chosen.put()
            
        syl.put()
        self.redirect('/editpolicy')
        

class AddHandler(webapp2.RequestHandler):
    def post(self):
        option = self.request.get("savedPolicyButton")
        selected = self.request.get("savedpolicies")
        chosen = policy.Policy()
        
        for item in user.savedPolicies:
            if item.key() == selected:
                chosen = item
            item.isSelected = False
        
        if option == "Add":
            syl.policies.append(chosen)
        
        chosen.isSelected = True
        
        chosen.put()
        syl.put()
        self.redirect("/editpolicy")
        
        
class RemoveHandler(webapp2.RequestHandler):
    def post(self):
        selected = self.request.get("policiesOnSyllabus")
        chosen = policy.Policy()
        
        for item in syl.policies:
            if item.key() == selected:
                chosen=item
                syl.policies.remove(item) 
            item.isSelected = False
                
        chosen.isSelected = True  
           
        syl.put()
        self.redirect("/editpolicy")