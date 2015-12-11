import webapp2
import jinja2
import os
from google.appengine.ext import ndb

class Policy(ndb.Model):
    title = ndb.StringProperty()
    description = ndb.TextProperty()
    isSelected = ndb.BooleanProperty()
    onSyllabus = ndb.BooleanProperty(default = False)
    
    def copy(self):
        return Policy(title=self.title, description=self.description, isSelected=self.isSelected)
        
    def name(self):
        if self.title == "" or self.title is None:
            return "none"
            
        return self.title
    
    
from basehandler import BaseHandler, login_required
from syllabus import Syllabus
from textbook import Textbook

template_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.getcwd())
    )
                
class EditHandler(BaseHandler):
    @login_required     
    def get(self):
        user = self.current_user
        syllabus = self.current_syllabus
        
        selected = Policy.query(ancestor = user.key).filter(Policy.isSelected == True).get()
        if not selected:
            selected = Policy()
            
        template = template_env.get_template('policyEdit.html')
        context = {
            'savedPolicies': user.savedPolicies,
            'policies': syllabus.policies,
            'selected': selected.name(),
            'title': selected.title,
            'description': selected.description,
        }

        self.response.write(template.render(context))
        
    @login_required     
    def post(self):
        user = self.current_user
        
        option = self.request.get("policyEditorButton")
        mytitle = self.request.get("policyTitle")
        mydescription = self.request.get("policyDescription")
        p = None      
          
        if option == "Update":
            p = Policy.query(ancestor = user.key).filter(Policy.isSelected == True).get()
        elif option == "Create New":
            p = Policy(parent = user.key, title = mytitle, description = mydescription)
            
        if p:
            p.title = mytitle
            p.description = mydescription
            p.isSelected = True
            p.put()
        
        self.redirect('/editpolicy')
        

class AddHandler(BaseHandler):
    @login_required     
    def post(self):
        user = self.current_user
        syllabus = self.current_syllabus
        
        option = self.request.get("savedPolicyButton")
        selected = self.request.get("savedpolicies")
        
        chosen = Policy()
        
        for p in user.savedPolicies:
            p.isSelected = False
            if p.name() == selected:
                p.isSelected = True
                chosen = p
            p.put()
        
        if option == "Add":
            new = Policy(parent = syllabus.key, title = chosen.title, description = chosen.description, onSyllabus = True, isSelected = True)
            new.put()
        
        self.redirect("/editpolicy")
        
        
class RemoveHandler(BaseHandler):
    @login_required     
    def post(self):
        syllabus = self.current_syllabus
        
        selected = self.request.get("policiesOnSyllabus")
        
        for p in syllabus.policies:
            if p.name() == selected:
                chosen = p
                chosen.key.delete()
            p.isSelected = False
           
        self.redirect("/editpolicy")
