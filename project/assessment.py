import webapp2
import jinja2
import os
from google.appengine.ext import ndb
   
class Assessment(ndb.Model):
    title = ndb.StringProperty()
    description = ndb.StringProperty()
    percentage = ndb.IntegerProperty()
    isSelected = ndb.BooleanProperty()
    onSyllabus = ndb.BooleanProperty(default = False)
    
    def copy(self):
        return Assessment(title=self.title, description=self.description, percentage=self.percentage, isSelected=self.isSelected)
        
    @webapp2.cached_property
    def name(self):
        return self.title + " (" + str(self.percentage) + "%)" if self.title else None
        

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
            a = Assessment.query(ancestor = user.key).filter(Assessment.isSelected == True).get()
            a.key.delete()
        
        option = self.request.get("assessmentEditorButton")
        mytitle = self.request.get("assessmentTitle")
        mypercentage = int(self.request.get("assessmentPercentage"))
        mydescription = self.request.get("assessmentDescription")
        a = None
        
        if option == "Update":
            a = Assessment.query(ancestor = user.key).filter(Assessment.isSelected == True).get()
        elif option == "Create New":
            for a in user.savedAssessments:
                a.isSelected = False
                a.put()
            a = Assessment(parent = user.key)
        
        if a:
            a.title = mytitle
            a.percentage = mypercentage
            a.description = mydescription
            a.isSelected = True
            a.put()
            
        self.redirect('/assessment')
        
    
class MainHandler(BaseHandler):
    @login_required     
    @syllabus_required
    def get(self, errors = None):
        user = self.current_user
        syllabus = self.current_syllabus
        
        selected = Assessment.query(ancestor = user.key).filter(ndb.AND(Assessment.isSelected == True, Assessment.onSyllabus == False)).get()
        
        template = template_env.get_template('assessmentEdit.html')
        context = {
            'assessments': user.savedAssessments,
            'onSyllabus': syllabus.assessments,
            'selected': selected.name if selected else None,
            'title': selected.title if selected else None,
            'description': selected.description if selected else None,
            'percentage': selected.percentage if selected else None,
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
            selected = Assessment.query(ancestor = user.key).filter(Assessment.description == edit).get()
            if selected:
                for a in user.savedAssessments:
                    a.isSelected = False
                    a.put()
                selected.isSelected = True
                selected.put()
            
            return self.redirect('/assessment')
            
        option = self.request.get("saveButton")
        
        list_to_save = []
        for a in user.savedAssessments:
            assessment = str(self.request.get(str(a.description)))
            if assessment:
                list_to_save.append(assessment) 
        
        total = 0
        if option:
            for a in syllabus.assessments:
                a.key.delete()
                
            for l in list_to_save:
                temp = Assessment.query(ancestor = user.key).filter(Assessment.description == l).get()
                if temp:
                    total += temp.percentage
                    new = Assessment(parent = syllabus.key, title = temp.title, percentage = temp.percentage, description = temp.description, isSelected = temp.isSelected, onSyllabus = True)
                    new.put()
                    
        if total != 100:
            return self.get('Total percentage must equal 100%')
                
        self.redirect("/")
        