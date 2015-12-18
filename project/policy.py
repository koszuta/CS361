import webapp2
import jinja2
import os
from google.appengine.ext import ndb

class Policy(ndb.Model):
    title = ndb.StringProperty()
    description = ndb.StringProperty()
    isSelected = ndb.BooleanProperty()
    onSyllabus = ndb.BooleanProperty(default = False)
    
    def copy(self):
        return Policy(title=self.title, description=self.description, isSelected=self.isSelected)
      
    @webapp2.cached_property
    def name(self):
        if self.title == "" or self.title is None:
            return "none"
            
        return self.title
    
    
from basehandler import BaseHandler, login_required, syllabus_required

template_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.getcwd())
    )
                
class EditHandler(BaseHandler):
    @login_required     
    def post(self):
        user = self.current_user
        
        delete = str(self.request.get('deleteButton'))
        if delete:
            p = Policy.query(ancestor = user.key).filter(Policy.isSelected == True).get()
            p.key.delete()
        
        option = self.request.get("policyEditorButton")
        mytitle = self.request.get("policyTitle")
        mydescription = self.request.get("policyDescription")
        p = None      
          
        if option == "Update":
            p = Policy.query(ancestor = user.key).filter(Policy.isSelected == True).get()
        elif option == "Create New":
            for p in user.savedPolicies:
                p.isSelected = False
                p.put()
            p = Policy(parent = user.key)
            
        if p:
            p.title = mytitle
            p.description = mydescription
            p.isSelected = True
            p.put()
        
        self.redirect('/policy')
        

class MainHandler(BaseHandler):
    @login_required 
    @syllabus_required    
    def get(self, errors = None):
        user = self.current_user
        syllabus = self.current_syllabus
        
        selected = Policy.query(ancestor = user.key).filter(ndb.AND(Policy.isSelected == True, Policy.onSyllabus == False)).get()
        
        template = template_env.get_template('policyEdit.html')
        context = {
            'policies': user.savedPolicies,
            'onSyllabus': syllabus.policies,
            'selected': selected.name if selected else None,
            'title': selected.title if selected else None,
            'description': selected.description if selected else None,
            'errors': errors,
        }

        self.response.write(template.render(context))
        
    @login_required  
    @syllabus_required   
    def post(self):
        user = self.current_user
        syllabus = self.current_syllabus
        
        edit = str(self.request.get('editButton'))
        
        if edit:
            selected = Policy.query(ancestor = user.key).filter(Policy.description == edit).get()
            if selected:
                for p in user.savedPolicies:
                    p.isSelected = False
                    p.put()
                selected.isSelected = True
                selected.put()
            
            return self.redirect('/policy')
            
        option = self.request.get("saveButton")
        
        list_to_save = []
        for p in user.savedPolicies:
            policy = str(self.request.get(str(p.description)))
            if policy:
                list_to_save.append(policy) 
        
        if option:
            for p in syllabus.policies:
                p.key.delete()
                
            for l in list_to_save:
                temp = Policy.query(ancestor = user.key).filter(Policy.description == l).get()
                if temp:
                    new = Policy(parent = syllabus.key, title = temp.title, description = temp.description, isSelected = temp.isSelected, onSyllabus = True)
                    new.put()
                    
        self.redirect("/")
        