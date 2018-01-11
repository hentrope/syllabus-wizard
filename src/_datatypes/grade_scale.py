from google.appengine.ext import ndb

class GradeScale(ndb.Model):
    letter = ndb.StringProperty(indexed=False)
    grademin = ndb.IntegerProperty(indexed=False)

    @classmethod
    def create(cls, letter="", grademin=0):
        return cls(letter=letter, grademin=grademin)