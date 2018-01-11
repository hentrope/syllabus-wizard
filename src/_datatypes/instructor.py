from datatypes import MeetingTime
from google.appengine.ext import ndb
from webapp2 import cached_property

WEEKDAY_CHARS = ['M', 'T', 'W', 'R', 'F', 'S', 'U']

#from datatypes import meeting_time

"""class Instructor(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    office = ndb.StringProperty()
    oHours = ndb.StringProperty()

    @classmethod
    def create(cls, name="", email="", office="", oHours=""):
        return Instructor(name=name, email=email, office=office, oHours=oHours)"""

class OfficeTerm(ndb.Model):
    room = ndb.StringProperty(default="", indexed=False)
    phone = ndb.StringProperty(default="", indexed=False)
    times = ndb.StructuredProperty(MeetingTime, repeated=True)
    
    def add(self):
        self.times.append(MeetingTime.create())
    
    def remove(self, time):
        self.times.remove(time)

    def remove_index(self, index):
        self.times.remove(self.times[index])
    
    @cached_property
    def schedule_string(self):
        return MeetingTime.build_string(self.times)

    @classmethod
    def create(cls, parent, term):
        i = cls(parent=parent, id=term)
        i.put()
        return i

class Instructor(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    
    def get_office_user_term(self, user_key, term):
        ret = OfficeTerm.get_by_id(term, parent=user_key)
        if ret is None:
            ret = OfficeTerm.create(user_key, term)
        return ret
    
    def get_office_term(self, term):
        ret = OfficeTerm.get_by_id(term, parent=self.key)
        if ret is None:
            ret = OfficeTerm.create(self.key, term)
        return ret

    @classmethod
    def create(cls, user_key, name="", email=""):
        return cls(parent=user_key, name=name, email=email)
    
    @classmethod
    def query_user(cls, user_key):
        return cls.query(ancestor=user_key)