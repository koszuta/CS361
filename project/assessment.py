import webapp2
import jinja2
import os
from google.appengine.ext import ndb
   
class Assessment(ndb.Model):
    title = ndb.StringProperty()
    description = ndb.TextProperty()
    percentage = ndb.IntegerProperty()
    isSelected = ndb.BooleanProperty()
    onSyllabus = ndb.BooleanProperty(default = False)
    
    def copy(self):
        return Assessment(title=self.title, description=self.description, percentage=self.percentage, isSelected=self.isSelected)
        
    def name(self):
        return self.title + " (" + str(self.percentage) + "%)" if self.title else None
        

from basehandler import BaseHandler, login_required
'''
from syllabus import Syllabus
from calendars import Calendar
from textbook import Textbook
'''

template_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.getcwd())
    )  
    
class EditHandler(BaseHandler):
    @login_required     
    def get(self):
        user = self.current_user
        syllabus = self.current_syllabus
        
        selected = Assessment.query(ancestor = user.key).filter(Assessment.isSelected == True).get()
        if not selected:
            selected = Assessment()
                
        template = template_env.get_template('assessmentEdit.html')
        context = {
            'savedAssessments': user.savedAssessments,
            'assessments': syllabus.assessments,
            'selected': selected.name(),
            'title': selected.title,
            'description': selected.description,
            'percentage': selected.percentage,
        }

        self.response.write(template.render(context))
        
    @login_required     
    def post(self):
        user = self.current_user
        
        option = self.request.get("assessmentEditorButton")
        mytitle = self.request.get("assessmentTitle")
        mypercentage = int(self.request.get("assessmentPercentage"))
        mydescription = self.request.get("assessmentDescription")
        a = None
        
        if option == "Update":
            a = Assessment.query(ancestor = user.key).filter(Assessment.isSelected == True).get()
        elif option == "Create New":
            a = Assessment(parent = user.key)
        
        if a:
            a.title = mytitle
            a.percentage = mypercentage
            a.description = mydescription
            a.put()
            
        self.redirect('/editassessment')
        
    
class AddHandler(BaseHandler):
    @login_required     
    def post(self):
        user = self.current_user
        syllabus = self.current_syllabus
        
        option = self.request.get("savedAssessmentButton")
        selected = self.request.get("savedAssessments")
        
        temp = Assessment()
        
        for before in user.savedAssessments:
            before.isSelected = False
            if before.name() == selected:
                before.isSelected = True
                temp = before
            before.put()
        
        total = 0
        for a in syllabus.assessments:
            total += a.percentage
            
        total += temp.percentage
            
        if option == "Add" and not total > 100:
            new = Assessment(parent = syllabus.key, title = temp.title, percentage = temp.percentage, description = temp.description, isSelected = temp.isSelected, onSyllabus = True)
            new.put()
            
        self.redirect("/editassessment")
        
            
class RemoveHandler(BaseHandler):
    @login_required     
    def post(self):
        syllabus = self.current_syllabus
        
        selected = self.request.get("assessmentsOnSyllabus")
        
        for a in syllabus.assessments:
            if a.name() == selected:
                a.key.delete()
            a.isSelected = False
            
        self.redirect("/editassessment")