from datatypes import Instructor
from google.appengine.ext import ndb

class Section(ndb.Model):
    name = ndb.StringProperty()
    room = ndb.StringProperty()
    notes = ndb.StringProperty()
    instructor = ndb.KeyProperty(kind=Instructor)
    suggestion = ndb.StringProperty()
    
    def instructor_instance(self, owner):
        if self.instructor is None:
            return owner.instructor
        else:
            return self.instructor.get()
    
    @classmethod
    def create(cls, name="", room="", notes="", instructor=None, suggestion=""):
        return cls(name=name, room=room, notes=notes, instructor=instructor, suggestion=suggestion)