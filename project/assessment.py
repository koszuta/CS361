import webapp2
import jinja2
import os
from google.appengine.ext import ndb

class Assessment(ndb.Model):
    title = ndb.StringProperty()
    description = ndb.TextProperty()
    percentage = ndb.IntegerProperty()
    isSelected = ndb.BooleanProperty()
    onSyllabus = ndb.BooleanProperty()
    
    def copy(self):
        return Assessment(title=self.title, description=self.description, percentage=self.percentage, isSelected=self.isSelected)
        
    def key(self):
        if self.title == "" or self.title is None:
            return "none"
            
        return self.title + " (" + str(self.percentage) + "%)"
        

from basehandler import BaseHandler, login_required
'''
from syllabus import Syllabus
from calendars import Calendar
from textbook import Textbook
'''
    
class EditHandler(BaseHandler):
    @login_required     
    def get(self):
        x = Assessment()
        for item in user.savedAssessments:
            if item.isSelected:
                x = item.copy()
                
        template = template_env.get_template('assessmentEdit.html')
        context = {
            'savedAssessments': user.savedAssessments,
            'selected': x.key(),
            'assessments': syl.assessments,
            'title': x.title,
            'description': x.description,
            'percentage': x.percentage,
        }

        self.response.write(template.render(context))
        
    @login_required     
    def post(self):
        option = self.request.get("assessmentEditorButton")
        
        mytitle = self.request.get("assessmentTitle")
        mypercentage = int(self.request.get("assessmentPercentage"))
        mydescription = self.request.get("assessmentDescription")
        
        chosen = assessment.Assessment()
                
        if option == "Update":
            for item in user.savedAssessments:
                if item.isSelected:
                    item.title = mytitle
                    item.percentage = mypercentage
                    item.description = mydescription
                    
        elif option == "Create New":
            chosen.title = mytitle
            chosen.percentage = mypercentage
            chosen.description = mydescription
            
            user.savedAssessments.append(chosen) 

            chosen.put()
        syl.put()
        self.redirect('/editassessment')
        
    
class AddHandler(BaseHandler):
    @login_required     
    def post(self):
        option = self.request.get("savedAssessmentButton")
        selected = self.request.get("savedAssessments")
        chosen = assessment.Assessment()
        
        for item in user.savedAssessments:
            if item.key() == selected:
                chosen = item
            item.isSelected = False
        
        if option == "Add":
            syl.assessments.append(chosen)
        
        chosen.isSelected = True
        
        chosen.put()
        syl.put()
        self.redirect("/editassessment")
        
            
class RemoveHandler(BaseHandler):
    @login_required     
    def post(self):
        selected = self.request.get("assessmentsOnSyllabus")
        chosen = assessment.Assessment()
        
        for item in syl.assessments:
            if item.key() == selected:
                chosen=item
                syl.assessments.remove(item) 
            item.isSelected = False
                
        chosen.isSelected = True  
           
        syl.put()
        self.redirect("/editassessment")