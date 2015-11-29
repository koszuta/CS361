import webapp2
import jinja2
import os
from google.appengine.ext import ndb

from basehandler import BaseHandler
from user import User
from term import Term         

template_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.getcwd())
    )
    
#@login_required
class ListerHandler(BaseHandler):
    def get(self):
        term = None
        termKey = self.session.get('term')
        if termKey:
            term = ndb.Key(urlsafe = termKey).get()
            
        template = template_env.get_template('list.html')
        context = {
            'term': term,
        }
        
        self.response.write(template.render(context))
        
class TermSelectHandler(BaseHandler):
    def post(self):
        user_id = self.auth.get_user_by_session().get('user_id')
        user = self.auth.store.user_model.get_by_id(user_id)
        
        semester = str(self.request.get('listSelectSemester'))
        year = int(self.request.get('listSelectYear'))
    
        term = Term.query(ancestor = user.key).filter(ndb.AND(Term.semester == semester, Term.year == year)).get()
        
        for t in user.terms:
            t.isSelected = False
            t.put()
            
        if term:
            term.isSelected = True
        else:
            term = Term(parent = user.key, semester = semester, year = year, isSelected = True)
            
        term.put()
        self.session['term'] = term.key.urlsafe()
    
        self.redirect('/list')
        