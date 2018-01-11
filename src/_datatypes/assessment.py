from google.appengine.ext import ndb

class Assessment(ndb.Model):
    name = ndb.StringProperty()
    perc = ndb.IntegerProperty()
    desc = ndb.StringProperty()

    @classmethod
    def create(cls, name="", perc=0, desc=""):
        i = Assessment()
        i.name = name
        i.perc = perc
        i.desc = desc
        return i