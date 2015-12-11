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
        
        if number < 10:
            number = '00' + str(number)
        elif number < 100:
            number = '0' + str(number)
        else:
            number = str(number)
            
        if section < 10:
            section = '00' + str(section)
        elif section < 100:
            section = '0' + str(section)
        else:
            section = str(section)
        
        course_list = WebScraper.scrapeCourseNames(str(term.semester), int(term.year), subject)
        course_name = None
        for c in course_list:
            if WebScraper.getCourseSubjectFromCourseName(c) == subject and WebScraper.getCourseNumberFromCourseName(c) == number:
                course_name = c
                break
            
        if course_name:
            syllabus.info.title = WebScraper.getCourseTitleFromCourseName(course_name)               
                
            sections_list = WebScraper.scrapeCourseSections(str(term.semester), int(term.year), course_name)
            course_section = None
            for s in sections_list:
                if WebScraper.getSectionFromCourseSection(s) == 'LEC ' + section:
                    course_section = s
                    break
            
            if course_section:
                room = WebScraper.getRoomFromCourseSection(course_section)
                if room:
                    syllabus.info.building = room.split()[0]
                    syllabus.info.room = room.split()[1]
                    
                syllabus.info.days = WebScraper.getMeetDaysFromCourseSection(course_section)
                
                time = WebScraper.getMeetTimeFromCourseSection(course_section)
                if time:
                    syllabus.info.start = time.split()[0]
                    syllabus.info.end = time.split('-')[1].split()[0]
        
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