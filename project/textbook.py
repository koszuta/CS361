import os
import webapp2
import urllib

from jinja2 import Environment, FileSystemLoader
from google.appengine.ext import ndb

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
    
    @staticmethod
    def exists(isbn):
        return Textbook.query(Textbook.isbn == isbn).get() is not None

def doRefresh(webapp, title, message, url, timeout=2):
    template = jinja_env.get_template('refresh.html')
    context = {
        'title': title,
        'timeout': str(timeout),
        'url': url,
        'message': message
    }
    webapp.response.write(template.render(context))
    
class RemoveTextbookHandler(webapp2.RequestHandler):
    def post(self):
        selectedBooks = self.request.get_all('bookSelect')
        books = Textbook.query().fetch()
        books[:] = [x for x in books if x not in selectedBooks]
        for book in books:
            if book.isbn not in selectedBooks:
                book.key.delete()
        msg = 'Updating book selections...'
        doRefresh(self, 'Updating Book Selections', msg, '/editbooks')

class EditTextbookHandler(webapp2.RequestHandler):
    def get(self):
        isbn = self.request.get('isbn')
        currentBook = self.getCurrentBook(isbn)
        
        if (currentBook is not None):
            template = jinja_env.get_template('bookInfoEdit.html')
            context = {
                'title': currentBook.title,
                'author': currentBook.author,
                'edition': currentBook.edition,
                'publisher': currentBook.publisher,
                'isbn': currentBook.isbn,
                'editISBN': currentBook.isbn
            }
            self.response.write(template.render(context))
        else:
            msg = 'Error: ISBN {0} does not exist. Returning to textbook listing...'.format(isbn)
            doRefresh(self, 'Bad ISBN', msg, '/editbooks', 3)
    
    def post(self):
        title = self.request.get('bookTitle')
        author = self.request.get('bookAuthor')
        edition = self.request.get('bookEdition')
        publisher = self.request.get('bookPublisher')
        isbn = self.request.get('bookISBN')
        editISBN = self.request.get('isbn')
        errors = []

        if (title == ''):
            errors.append('Title field must not be empty')
        if (author == ''):
            errors.append('Author field must not be empty')
        if (publisher == ''):
            errors.append('Publisher field must not be empty')
        if (isbn == ''):
            errors.append('ISBN field must not be empty')
        elif (isbn != editISBN and Textbook.exists(isbn)):
            errors.append('Book with ISBN already exists')
        
        context = {}
        currentBook = self.getCurrentBook(editISBN)
        
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
                'editISBN': editISBN
            })
            self.response.write(template.render(context))
        else:
            currentBook.title = title
            currentBook.author = author
            currentBook.edition = edition
            currentBook.publisher = publisher
            currentBook.isbn = isbn
            currentBook.put()
            msg = 'Updating {0}...'.format(title)
            doRefresh(self, 'Updating Textbook', msg, '/editbooks')

    def getCurrentBook(self, isbn):
        return Textbook.query(Textbook.isbn == isbn).get()
            
    
class TextbookHandler(webapp2.RequestHandler):
    def getBooks(self):
        return Textbook.query().fetch()

    def get(self):
        template = jinja_env.get_template('textbookEdit.html')
        
        context = {
            'books': self.getBooks()
        }

        self.response.write(template.render(context))
		
    def post(self):
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
        elif (Textbook.exists(isbn)):
            errors.append('Book with ISBN already exists')

        context = {
            'books': self.getBooks()
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
            newBook = Textbook(title=title, author=author, edition=edition,
                                publisher=publisher, isbn=isbn)
            newBook.put()
            msg = 'Adding {0}...'.format(title)
            doRefresh(self, "Adding Textbook", msg, "/editbooks")