from google.appengine.ext import ndb
from sint import sint

class CourseID(ndb.Model):
    dept = ndb.StringProperty(default="")
    num = ndb.IntegerProperty(default=0)
    
    def __eq__(self, other):
        return self.dept == other.dept and self.num == other.num
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def to_string(self):
        return str(self.dept) + ":" + str(self.num)

    @classmethod
    def from_string(cls, string):
        i = cls()
        
        split = string.split(":")
        i.dept = split[0]
        i.num = sint(split[1])
        
        return i

    @classmethod
    def create(cls, dept, num):
        i = CourseID()
        i.dept = dept
        i.num = num
        return i