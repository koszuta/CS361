import webapp2
import jinja2
import os
from google.appengine.ext import ndb

from basehandler import BaseHandler, login_required
from user import User
from term import Term   
from syllabus import Syllabus      

template_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.getcwd())
    )
    
class ListerHandler(BaseHandler):
    @login_required
    def get(self):
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
        term = ndb.Key(urlsafe = termKey).get()
            
        syllabus = Syllabus(parent = term.key, title = 'Temp Title')
        syllabus.put()
        self.session['syllabus'] = syllabus.key.urlsafe()
        
        self.redirect('/')
  
       
class SelectSyllabusHandler(BaseHandler):
    @login_required	 
    def post(self):
        termKey = self.session.get('term')
        term = ndb.Key(urlsafe = termKey).get()
        
        select = str(self.request.get('syllabusSelectRadio'))
        
        for s in term.syllabi:
            if s.title == select:
                self.session['syllabus'] = s.key.urlsafe()
                
        self.redirect('/')