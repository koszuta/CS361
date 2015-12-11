import os
import webapp2
import urllib

from jinja2 import Environment, FileSystemLoader
from google.appengine.ext import ndb

from basehandler import BaseHandler, login_required

jinja_env = Environment(
  loader=FileSystemLoader(os.path.dirname(__file__)),
  extensions=['jinja2.ext.autoescape'],
  autoescape=True)

def urlencode(text):
    return urllib.quote_plus(text)

# Add URL encoding filter for templates
jinja_env.filters['urlencode'] = urlencode
  
class Textbook(ndb.Model):
    title = ndb.StringProperty()
    author = ndb.StringProperty()
    edition = ndb.StringProperty()
    publisher = ndb.StringProperty()
    isbn = ndb.StringProperty()
    onSyllabus = ndb.BooleanProperty()
    
    @staticmethod
    def exists(parent, isbn):
        return Textbook.query(ancestor=parent.key).filter(Textbook.isbn == isbn).get() is not None

def doRefresh(webapp, title, message, url, timeout=2):
    template = jinja_env.get_template('refresh.html')
    context = {
        'title': title,
        'timeout': str(timeout),
        'url': url,
        'message': message
    }
    webapp.response.write(template.render(context))

# Clones datastore entity (extra_args overrides values)
def clone_entity(e, **extra_args):
    cls = e.__class__
    props = dict((v._code_name, v.__get__(e, cls)) for v in cls._properties.itervalues() if type(v) is not ndb.ComputedProperty)
    props.update(extra_args)
    return cls(**props)

class AddTextbookHandler(BaseHandler):
    @login_required
    def post(self):
        user = self.current_user
        syllabus = self.current_syllabus

        onSyllabus = self.request.get('onSyllabus')
        try:
            onSyllabus = int(onSyllabus) == 1
        except:
            onSyllabus = False

        errors = []
        
        selectedBooks = self.request.get_all('bookSelect')
        if selectedBooks:
            bookQuery = Textbook.query(ancestor=user.key)
            bookQuery = bookQuery.filter(Textbook.onSyllabus == onSyllabus)
            bookQuery = bookQuery.filter(Textbook.isbn.IN(selectedBooks))
            books = bookQuery.fetch()
        else:
            errors.append('No books were selected to add to the syllabus')

        if not errors:
            syllabusBooks = Textbook.query(ancestor=syllabus.key).fetch()
            syllabusList = []
            for book in syllabusBooks:
                syllabusList.append(book.isbn)
            
            for book in books:
                if book.isbn in syllabusList:
                    errors.append('Book with ISBN (' + book.isbn + ') is already on syllabus')
        
        if not errors:
            for book in books:
                syllabusBook = clone_entity(book, 
                                            parent=syllabus.key if not onSyllabus else user.key, 
                                            onSyllabus=(not onSyllabus))
                syllabusBook.put()
        
            self.redirect('/editbooks')
        else:
            self.session['bookErrors'] = errors
            self.redirect('/findbook')

class RemoveTextbookHandler(BaseHandler):
    @login_required
    def post(self):
        user = self.current_user

        onSyllabus = self.request.get('onSyllabus')
        try:
            onSyllabus = int(onSyllabus) == 1
        except:
            onSyllabus = False

        errors = []

        selectedBooks = self.request.get_all('bookSelect')
        
        if selectedBooks or onSyllabus:
            books = Textbook.query(ancestor=user.key).filter(Textbook.onSyllabus == onSyllabus).fetch()
            books[:] = [x for x in books if x not in selectedBooks]
            for book in books:
                if book.isbn not in selectedBooks:
                    book.key.delete()
        else:
            errors.append('No books were selected for removal')
        
        if not errors:
            self.redirect('/editbooks')
        else:
            self.session['bookErrors'] = errors
            self.redirect('/findbook')
        
class FindTextbookHandler(BaseHandler):
    @login_required
    def get(self):
        self.post()

    @login_required
    def post(self):
        searchFields = ['title', 'author', 'edition', 'publisher', 'isbn']
        
        query = self.request.get('bookQuery')
        if not query:
            query = self.session.get('lastBookQuery')
            if query is None:
                query = ''
        else:
            self.session['lastBookQuery'] = query

        queryField = self.request.get('bookQueryType')
        if not queryField:
            queryField = self.session.get('lastBookQueryType')
        else: 
            if queryField in searchFields:
                self.session['lastBookQueryType'] = queryField
            else:
                self.session['lastBookQueryType'] = 'all'
        
        user = self.current_user
        syllabus = self.current_syllabus

        allBooks = Textbook.query(ancestor=user.key).filter(Textbook.onSyllabus == False).fetch()
        syllabusBooks = Textbook.query(ancestor=syllabus.key).fetch()
        import logging
        logging.info(syllabusBooks)
        books = []
        syllabusList = []
        errors = self.session.get('bookErrors')
        if errors:
            del self.session['bookErrors']
        
        for b in syllabusBooks:
            syllabusList.append(b.isbn)

        if queryField in searchFields:
            # Search in specified field
            for book in allBooks:
                if query.lower() in book.to_dict()[queryField].lower():
                    books.append(book)
        else:
            for book in allBooks:
                # Search in all fields
                bookDict = book.to_dict()
                for field in searchFields:
                    if query.lower() in bookDict[field].lower():
                        books.append(book)
                        break
        
        template = jinja_env.get_template('textbookSearch.html')
        context = {
            'query': query,
            'queryField': queryField,
            'books': books,
            'syllabusList': syllabusList,
            'errors': errors
        }
        self.response.write(template.render(context))
        
        
class EditTextbookHandler(BaseHandler):
    @login_required
    def get(self):
        isbn = self.request.get('isbn')
        onSyllabus = self.request.get('onSyllabus')
        try:
            onSyllabus = int(onSyllabus) == 1
        except:
            onSyllabus = False

        currentBook = self.getCurrentBook(onSyllabus, isbn)
        
        if (currentBook is not None):
            template = jinja_env.get_template('bookInfoEdit.html')
            context = {
                'title': currentBook.title,
                'author': currentBook.author,
                'edition': currentBook.edition,
                'publisher': currentBook.publisher,
                'isbn': currentBook.isbn,
                'editISBN': currentBook.isbn,
                'onSyllabus': '1' if onSyllabus else '0'
            }
            self.response.write(template.render(context))
        else:
            msg = 'Error: ISBN {0} does not exist. Returning to textbook listing...'.format(isbn)
            doRefresh(self, 'Bad ISBN', msg, '/editbooks', 3)
    
    @login_required
    def post(self):
        title = self.request.get('bookTitle')
        author = self.request.get('bookAuthor')
        edition = self.request.get('bookEdition')
        publisher = self.request.get('bookPublisher')
        isbn = self.request.get('bookISBN')
        editISBN = self.request.get('isbn')

        onSyllabus = self.request.get('onSyllabus')
        try:
            onSyllabus = int(onSyllabus) == 1
        except:
            onSyllabus = False

        errors = []
        
        user = self.current_user

        if (title == ''):
            errors.append('Title field must not be empty')
        if (author == ''):
            errors.append('Author field must not be empty')
        if (publisher == ''):
            errors.append('Publisher field must not be empty')
        if (isbn == ''):
            errors.append('ISBN field must not be empty')
        elif (isbn != editISBN and Textbook.exists(user, isbn)):
            errors.append('Book with ISBN already exists')
            
        context = {}
        currentBook = self.getCurrentBook(onSyllabus, editISBN)
        
        if errors:
            template = jinja_env.get_template('bookInfoEdit.html')
            context.update({
                'errors': errors,
                'book': currentBook,
                'title': title,
                'author': author,
                'edition': edition,
                'publisher': publisher,
                'isbn': isbn,
                'editISBN': editISBN,
                'onSyllabus': '1' if onSyllabus else '0'
            })
            self.response.write(template.render(context))
        else:
            currentBook.title = title
            currentBook.author = author
            currentBook.edition = edition
            currentBook.publisher = publisher
            currentBook.isbn = isbn
            currentBook.put()
            self.redirect('/editbooks')

    def getCurrentBook(self, onSyllabus, isbn):
        if onSyllabus:
            syllabusKey = self.session.get('syllabus')
            parent = ndb.Key(urlsafe = syllabusKey).get()
        else:
            userKey = self.session.get('user')
            parent = ndb.Key(urlsafe = userKey).get()
        
        return Textbook.query(ancestor=parent.key).filter(ndb.AND(Textbook.isbn == isbn, Textbook.onSyllabus == onSyllabus)).get()

class TextbookHandler(BaseHandler):
    def getBooks(self):
        syllabus = self.current_syllabus
        return syllabus.textbooks if syllabus else None

    @login_required
    def get(self):
        template = jinja_env.get_template('textbookEdit.html')
        
        context = {
            'books': self.getBooks(),
            'lastQuery': self.session.get('lastBookQuery'),
            'lastQueryType': self.session.get('lastBookQueryType')
        }

        self.response.write(template.render(context))
		
    @login_required
    def post(self):
        user = self.current_user
        syllabus = self.current_syllabus

        template = jinja_env.get_template('textbookEdit.html')
        title = self.request.get('newBookTitle')
        author = self.request.get('newBookAuthor')
        edition = self.request.get('newBookEdition')
        publisher = self.request.get('newBookPublisher')
        isbn = self.request.get('newBookISBN')
        errors = []
        
        if (title == ''):
            errors.append('Title field must not be empty')
        if (author == ''):
            errors.append('Author field must not be empty')
        if (publisher == ''):
            errors.append('Publisher field must not be empty')
        if (isbn == ''):
            errors.append('ISBN field must not be empty')
        elif (Textbook.exists(user, isbn)):
            errors.append('Book with ISBN already exists')

        context = {
            'books': self.getBooks(),
            'lastQuery': self.session.get('lastBookQuery'),
            'lastQueryType': self.session.get('lastBookQueryType')
        }
        
        if (errors):
            context.update({
                'errors': errors,
                'title': title,
                'author': author,
                'edition': edition,
                'publisher': publisher,
                'isbn': isbn
            })
            self.response.write(template.render(context))
        else:
            # Add this new book to the current syllabus
            newBook = Textbook(parent=syllabus.key, title=title, author=author, edition=edition,
                                publisher=publisher, isbn=isbn, onSyllabus=True)
            newBook.put()
            
            # Add copy of book associated with this user
            userBook = clone_entity(newBook, parent=user.key, onSyllabus=False)
            userBook.put()

            self.redirect("/editbooks")
