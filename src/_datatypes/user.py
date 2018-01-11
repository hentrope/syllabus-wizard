from datatypes import Instructor
from google.appengine.ext import ndb

from webapp2 import cached_property
from webapp2_extras import security
from webapp2_extras.appengine.auth.models import User

class User(User):
    instructor = ndb.StructuredProperty(Instructor)
    
    @cached_property
    def name(self):
        return self.auth_ids[0]
    
    # Sets the password for the current user
    def set_password(self, raw_password):
        self.password = security.generate_password_hash(raw_password, length=12)
    
    @classmethod
    def delete_user(cls, user):
        user.key.delete()
        cls.unique_model.delete_multi(['%s.auth_id:%s' % (cls.__name__, aid) for aid in user.auth_ids])
