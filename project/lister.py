import webapp2
import jinja2
import os
from google.appengine.ext import ndb

from basehandler import BaseHandler, login_required
from user import User
from term import Term   
from syllabus import Syllabus
from courseinfo import Info    

from webscrape import WebScraper

template_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.getcwd())
    )
    
class ListerHandler(BaseHandler):
    @login_required
    def get(self):
        user_id = self.auth.get_user_by_session().get('user_id')
        user = self.auth.store.user_model.get_by_id(user_id)
        term = None
        termKey = self.session.get('term')
        if termKey:
            term = ndb.Key(urlsafe = termKey).get()
            
        template = template_env.get_template('list.html')
        context = {}
        if term:
            context = {
                'semester': term.semester,
                'year': term.year,
                'term': term,
                'username': user.auth_ids[0],
                'term_abbr': term.url
            }
        
        self.response.write(template.render(context))
  
        
class TermSelectHandler(BaseHandler):
    @login_required	
    def post(self):
        user_id = self.auth.get_user_by_session().get('user_id')
        user = self.auth.store.user_model.get_by_id(user_id)
        
        semester = str(self.request.get('listSelectSemester'))
        year = int(self.request.get('listSelectYear'))
    
        term = Term.query(ancestor = user.key).filter(ndb.AND(Term.semester == semester, Term.year == year)).get()
            
        if not term:
            term = Term(parent = user.key, semester = semester, year = year)
            term.put()
            
        self.session['term'] = term.key.urlsafe()
    
        self.redirect('/list')
 
       
class CreateSyllabusHandler(BaseHandler):
    @login_required	 
    def post(self):
        termKey = self.session.get('term')
        if not termKey:
            return self.redirect('/list')
            
        term = ndb.Key(urlsafe = termKey).get()
        
        subject = str(self.request.get('subjectSelect'))
        number = int(self.request.get('courseNumber'))
        section = int(self.request.get('sectionNumber'))
        
        info = Info(subject = subject, number = number, section = section)
        syllabus = Syllabus(parent = term.key, info = info)
        
        course_list = WebScraper.scrapeCourseNames(str(term.semester), int(term.year), subject)
        
        course = None
        for c in course_list:
            if WebScraper.getCourseSubjectFromCourseName(c) == str(subject) and WebScraper.getCourseNumberFromCourseName(c) == str(number):
                course = c
                
        syllabus.info.title = WebScraper.getCourseTitleFromCourseName(course)
        
            
        syllabus.put()
        self.session['syllabus'] = syllabus.key.urlsafe()
        
        self.redirect('/')
  
       
class SelectSyllabusHandler(BaseHandler):
    @login_required	 
    def get(self):
        termKey = self.session.get('term')
        if not termKey:
            return self.redirect('/list')
        term = ndb.Key(urlsafe = termKey).get()
        
        select = str(self.request.get('select'))
        
        for s in term.syllabi:
            combined = s.info.subject + str(s.info.number) + str(s.info.section)
            if combined == select:
                self.session['syllabus'] = s.key.urlsafe()
                
        self.redirect('/')
        
        
class ActivateSyllabusHandler(BaseHandler):
    @login_required
    def get(self):
        termKey = self.session.get('term')
        if not termKey:
            return self.redirect('/list')
        term = ndb.Key(urlsafe = termKey).get()
        
        activate = str(self.request.get('activate'))
        
        for s in term.syllabi:
            combined = s.info.subject + str(s.info.number) + str(s.info.section)
            if combined == activate:
                s.isActive = not s.isActive
                s.put()
                
        self.redirect('/list')