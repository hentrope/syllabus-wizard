from google.appengine.ext import ndb

class Policy(ndb.Model):
    title = ndb.StringProperty()
    desc = ndb.StringProperty()

    @classmethod
    def create(cls, title="", desc=""):
        return cls(title=title, desc=desc)