from google.appengine.ext import ndb

class Textbook(ndb.Model):
    title = ndb.StringProperty()
    edition = ndb.StringProperty()
    author = ndb.StringProperty()
    publisher = ndb.StringProperty()
    year = ndb.IntegerProperty()
    isbn = ndb.StringProperty()

    @classmethod
    def create(cls, title="", edition="", year=0, author="", isbn="", publisher=""):
        return cls(title=title, edition=edition, year=year, author=author, isbn=isbn, publisher=publisher)