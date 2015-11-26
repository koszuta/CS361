from google.appengine.ext import ndb

class Term(ndb.Model):
    semester = ndb.StringProperty()
    year = ndb.IntegerProperty()
    isSelected = ndb.BooleanProperty()
    @property
    def syllabi(self):
        from syllabus import Syllabus
        return Syllabus.query(ancestor = self.key).fetch()