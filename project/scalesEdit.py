import jinja2
import webapp2
import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb
from basehandler import BaseHandler, login_required, syllabus_required


JINJA_ENVIRONMENT = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
  extensions=['jinja2.ext.autoescape'],
  autoescape=True)
  
class Grade(ndb.Model):
    grade = ndb.IntegerProperty()
    letter = ndb.StringProperty()
    
               
class GradeScale(ndb.Model):
    scaleName = ndb.StringProperty()
    gradeScale = ndb.StructuredProperty(Grade, repeated=True)
    isSelected = ndb.BooleanProperty()
    onSyllabus = ndb.BooleanProperty(default = False)
    
    
              
grade = []
letter = []
scale = []

class ScalesHandler(BaseHandler):
    @login_required
    @syllabus_required
    def get(self):
        user = self.current_user
        
        global grade
        global letter
        global scale
        
        scaleName = ""
        currentLetter = ""
        currentGrade = 0
        size = len(grade) + 1
        
        save = self.request.get('save')
        next = self.request.get('next')
        if next:
            currentLetter = str(self.request.get("letter" + str(size - 1)))
            currentGrade = int(self.request.get("grade" + str(size - 1)))
            grade.append(currentGrade)
            letter.append(currentLetter)
            self.redirect("/editscales")
        elif save:
            size = len(grade)
            scaleName = self.request.get("scaleName")
            for i in range(0,size):
                newGrade = Grade(letter = letter[i], grade = grade[i])
                scale.append(newGrade)
            newScale = GradeScale(parent = user.key, scaleName = scaleName, gradeScale = scale)
            newScale.put()
            letter = []
            grade = []
            scale = []
                    
        template_values = {
                "scaleName": scaleName,
                "grade": grade,
                "letter": letter,
                "size": size,
                "save": save,
                "next": next,
                "savedScales": user.savedScales,
                
            }
                
        template = JINJA_ENVIRONMENT.get_template("scalesEdit.html")
        self.response.out.write(template.render(template_values))
   
    @login_required
    def post(self):
    
        self.redirect('/editscales')
              
class AddScalesHandler(BaseHandler):
    @login_required
    @syllabus_required
    def post(self):
        usedscale = self.request.get("selectedScale")

        user = self.current_user
        syllabus = self.current_syllabus

        
        for s in user.savedScales:
            if s.scaleName == usedscale:
                old = GradeScale.query(ancestor = syllabus.key).get()
                if old:
                    old.key.delete()
                syScale = GradeScale(parent = syllabus.key)
                syScale.onSyllabus = True
                syScale.gradeScale = s.gradeScale
                syScale.scaleName = s.scaleName
                syScale.isSelected = True
                syScale.put()
                break
        
        
        self.redirect("/")
        
