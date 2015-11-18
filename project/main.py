import webapp2
import jinja2
import os
import time

from google.appengine.ext import ndb

import user
import course
import syllabus
import instructor
import textbook
import calendarEdit
import scalesEdit
import assessment
import policy

user = user.User()
user.put()
syl = syllabus.Syllabus()
syl.put()

scott = instructor.Instructor(first='Scott', last='Ehlert', email='scott@uwm.edu', phone='(414) 555-1234', building='PHY', room='333', hours='MW 11am', isSelected=False) 
dylan = instructor.Instructor(first='Dylan', last='Harrison', email='dylan@uwm.edu', phone='(414) 555-9999', building='LAPH', room='150', hours='MWF 2pm', isSelected=False) 
nathan = instructor.Instructor(first='Nathan', last='Koszuta', email='nkoszuta@uwm.edu', phone='(414) 531-7488', building='CHEM', room='147', hours='MWR 10am', isSelected=False) 
shane = instructor.Instructor(first='Shane', last='Sedgwick', email='shane@uwm.edu', phone='(262) 555-0101', building='EMS', room='E190', hours='TR 12pm', isSelected=False)

p = assessment.Assessment(title="Project", percentage=40, description="The course project is implemented in phases by small groups of students. There are several phases of creating and refining deliverables such as requirements specifications, design documents, etc.", isSelected=False)
p2 = assessment.Assessment(title="Quizzes", percentage=10, description="Online quizzes will be posted in D2L. You may take each quiz up to 2 times. The score of the best attempt is recorded in the grade book. Unannounced quizzes in lecture are given to assess comprehension of concepts from the previous assignment, encourage attendance, and give you feedback about your progress. The low score will be dropped.", isSelected=False)

user.savedAssessments.append(p)
user.savedAssessments.append(p2)

p3 = policy.Policy(title="Academic Misconduct", description="The university has a responsibility to promote academic honesty and integrity and to develop procedures to deal effectively with instances of academic dishonesty. Students are responsible for the honest completion and representation of their work, for the appropriate citation of sources, and for respect of others' academic endeavors. A more detailed description of Student Academic Disciplinary Procedures may be found at http://www4.uwm.edu/acad_aff/policy/academicmisconduct.cfm", isSelected=False)

user.savedPolicies.append(p3)

user.savedInstructors.append(scott)
user.savedInstructors.append(nathan)
user.savedInstructors.append(dylan)
user.savedInstructors.append(shane)

    
template_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.getcwd())
    )

class MainHandler(webapp2.RequestHandler):
    def get(self):
                
        ilist = []
        for i in syl.instructors:
            ilist.append(i)
            
        alist = []
        for i in syl.assessments:
            alist.append(i)
            
        plist = []
        for i in syl.policies:
            plist.append(i)
            
        template = template_env.get_template('main.html')
        context = {
            'books': textbook.Textbook.query().fetch(),
            'instructors': ilist,
            'assessments': alist,
            'policies': plist,
        }
        
        self.response.write(template.render(context))


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/addinstructor', instructor.AddHandler),
    ('/removeinstructor', instructor.RemoveHandler),
    ('/editinstructor', instructor.EditHandler),
    ('/editbooks', textbook.TextbookHandler),
    ('/editbook', textbook.EditTextbookHandler),
    ('/removebooks', textbook.RemoveTextbookHandler),
    ('/editcalendar', calendarEdit.CalendarHandler),
    ('/editscales', scalesEdit.ScalesHandler),
    ('/editassessment', assessment.EditHandler),
    ('/addassessment', assessment.AddHandler),
    ('/removeassessment', assessment.RemoveHandler),
    ('/editpolicy', policy.EditHandler),
    ('/addpolicy', policy.AddHandler),
    ('/removepolicy', policy.RemoveHandler),
], debug=True)