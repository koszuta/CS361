import os
import webapp2

from collections import OrderedDict
from jinja2 import Environment, FileSystemLoader, Undefined
from google.appengine.ext import ndb

from instructor import Instructor
from textbook import Textbook

from basehandler import BaseHandler

class SilentUndefined(Undefined):
    def _fail_with_undefined_error(self, *args, **kwargs):
        return '{{ ' + self._undefined_name + '.undefined }}'

jinja_env = Environment(
  loader=FileSystemLoader(os.path.dirname(__file__)),
  extensions=['jinja2.ext.autoescape'],
  autoescape=True,
  undefined=SilentUndefined)
  
class PreviewHandler(BaseHandler):
    @staticmethod
    def createDummyContext():
        course = {
                'title': 'CompSci 361: Intro to Software Engineering',
                'term': 'Fall 2015'
        }

        instructors = [
            {
                'name': 'Jayson Rock',
                'email': 'rock@uwm.edu',
                'class': 'COMPSCI 361-401 EMS E145 MW 10-10:50am',
                'officeRoom': 'EMS E307',
                'officePhone': '(262) 825-4129',
                'officeHours': 'MTR 11am'
            },
            {
                'name': 'Tanawat Khunlertkit',
                'email': 'tanawat@uwm.edu',
                'class': '',
                'officeRoom': 'EMS 962',
                'officePhone': '(262) 825-4129',
                'officeHours': ''
            }
        ]

        textbooks = [
            {
                'title': 'Essential Skills for the Agile Developer',
                'author': 'Shalloway',
                'edition': '',
                'publisher': 'Addison-Wesley Professional',
                'isbn': '0785342543735'
            },
            {
                'title': 'Programming Google App Engine',
                'author': 'Sanderson',
                'edition': '2nd Ed.',
                'publisher': 'O\'Reilly Media',
                'isbn': '9781449398262'
            }
        ]

        assessments = [
            {
                'title': 'Project',
                'weight': '40',
                'description': 'The course project is implemented in phases by small groups of students. There are several phases of creating and refining deliverables such as requirements specifications, design documents, etc.'
            },
            {
                'title': 'Quizzes',
                'weight': '10',
                'description': 'Online quizzes will be posted in D2L. You may take each quiz up to 2 times. The score of the best attempt is recorded in the grade book. Unannounced quizzes in lecture are given to assess comprehension of concepts from the previous assignment, encourage attendance, and give you feedback about your progress. The low score will be dropped.'
            },
            {
                'title': 'Midterm',
                'weight': '20',
                'description': 'The midterm will be given during regular lecture time.'
            },
            {
                'title': 'Final',
                'weight': '20',
                'description': 'The final exam is cumulative; it is scheduled according to university policy.'
            },
            {
                'title': 'Labs',
                'weight': '10',
                'description': 'Weekly activities in lab for check-off.<br>Half credit for incomplete or inadequate work is possible.'
            }
        ]
            
        gradingScale = {
            'A':    '92',
            'A-':   '88',
            'B+':   '84',
            'B':    '80',
            'B-':   '76',
            'C+':   '72',
            'C':    '68',
            'C-':   '64',
            'D+':   '60',
            'D':    '56',
            'D-':   '52',
            'F':    '0'
        }
        
        policies = [
            {'title': 'Participation by Students with Disabilities', 'desc': 'If you need special accommodations in order to meet any of the requirements of this course, please contact me as soon as possible.'},
            {'title': 'Accommodation for Religious Observances', 'desc': 'Students will be allowed to complete examinations or other requirements that are missed because of a religious observance. See <a href="http://www.uwm.edu/Dept/SecU/acad+admin_policies/S1.5.htm">http://www.uwm.edu/Dept/SecU/acad+admin_policies/S1.5.htm</a>.'},
            {'title': 'Academic Misconduct', 'desc': 'The university has a responsibility to promote academic honesty and integrity and to develop procedures to deal effectively with instances of academic dishonesty. Students are responsible for the honest completion and representation of their work, for the appropriate citation of sources, and for respect of others\' academic endeavors. A more detailed description of Student Academic Disciplinary Procedures may be found at <a href="http://www4.uwm.edu/acad_aff/policy/academicmisconduct.cfm">http://www4.uwm.edu/acad_aff/policy/academicmisconduct.cfm</a>'},
            {'title': 'Makeup/Late Policy', 'desc': 'Assignments are submitted electronically via D2L.uwm.edu. An assignment is penalized 20% for each day (or part of a day) that it is late. The lowest quiz score is dropped to accommodate students who have life circumstances that prevent them from taking a quiz. There are no makeup quizzes.<br><br>Exams can be made up only if each of the following criteria are met:<br><br>1.      The circumstance that caused the student to miss the exam is unexpected, verifiable, and beyond the student\'s control.<br><br>2.      The student contacts the instructor as soon as possible by leaving a message at the phone number listed on the syllabus or by sending an email to <a href="mailto:rock@uwm.edu">rock@uwm.edu</a>. The message/email must contain a phone number the instructor can use to contact the student.<br><br>With sufficient advance notice, the instructor may allow students to take the exam at an alternate time to accommodate travel for extramural activities, work schedule, etc. Arranging to take the exam at an alternate time in advance is not considered a makeup exam.'},
        ]
        
        calendar = [
            {'date': '9/2', 'reading': '', 'topic': 'What is software engineering?'},
            {'date': '9/9', 'reading': '<a href="http://www.w3.org/wiki/Web_Standards_Curriculum">HTML5/CSS</a>', 'topic': 'HTML5/CSS'},
            {'date': '9/16', 'reading': '<a href="https://www.scrum.org/Portals/0/Documents/Scrum%20Guides/2013/Scrum-Guide.pdf#zoom=100">Scrum</a>', 'topic': 'Scrum: Intro, PB grooming'},
            {'date': '9/23', 'reading': '', 'topic': ''},
            {'date': '9/30', 'reading': '', 'topic': ''},
            {'date': '10/7', 'reading': 'GAE: 1-2', 'topic': ''},
            {'date': '10/14', 'reading': 'Midterm', 'topic': ''},
            {'date': '10/21', 'reading': 'S: 1-2, GAE: 3', 'topic': 'Jinja2, TDD'},
            {'date': '10/28', 'reading': 'S: 3, GAE: 4', 'topic': '<a href="http://www.scrum.org/About/All-Articles/articleType/ArticleView/articleId/642/Adopting-Test-First-Development">Test-Driven Dev</a>, datastore'},
            {'date': '11/4', 'reading': 'GAE: 5, S: 4', 'topic': 'datastore, redundancy'},
            {'date': '11/11', 'reading': 'S: 5-6', 'topic': 'Encapsulation, interface oriented design'},
            {'date': '11/18', 'reading': '', 'topic': ''},
            {'date': '11/25', 'reading': '', 'topic': ''},
            {'date': '12/2', 'reading': '', 'topic': 'Continuous Integration'},
            {'date': '12/9', 'reading': '', 'topic': ''},
            {'date': '12/16', 'reading': 'Final Exam', 'topic': ''},
        ]

        contextDict = {
            'course': course,
            'instructors': instructors,
            'textbooks': textbooks,
            'assessments': assessments,
            'gradingScale': OrderedDict(sorted(gradingScale.items(), key=lambda t: t[1], reverse=True)),
            'policies': policies,
            'calendar': calendar
        }
            
        return contextDict
            
    def get(self):
        dummy = self.request.get('dummy')
        
        try:
            dummy = int(dummy) != 0
        except Exception:
            dummy = True

        template = jinja_env.get_template('preview.html')
        if dummy:
            context = self.createDummyContext()
        else:
            syllabusKey = self.session.get('syllabus')
            syllabus = ndb.Key(urlsafe = syllabusKey).get()
            context = {
                #'instructors': Instructor.query(ancestor = syllabus.key).fetch(),
                'textbooks': Textbook.query(ancestor = syllabus.key).fetch(),
            }
        self.response.write(template.render(context))
