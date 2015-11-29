import webapp2
import jinja2
import os
from google.appengine.ext import ndb
from webapp2_extras.appengine.users import login_required

from basehandler import BaseHandler
from term import Term         

template_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.getcwd())
    )
    
#@login_required
class ListerHandler(BaseHandler):
    def get(self):
        termKey = self.session.get('term')
        term = ndb.Key(urlsafe = termKey).get()
            
        template = template_env.get_template('list.html')
        context = {
            'term': term,
        }
        
        self.response.write(template.render(context))
        
class TermSelectHandler(BaseHandler):
    def post(self):
        user = self.user
        
        semester = self.request.get('listSelectSemester')
        year = self.request.get('listSelectYear')
    
        term = None
        for t in user.terms:
            if t.semester == semester and t.year == year:
                term = t
        
        if term:
            term.isSelected = True
            self.session['term'] = term
        else:
            self.session['term'] = Term(parent = user.key, semester = semester, year = year, isSelected = True)
    
        self.redirect('/list')
        