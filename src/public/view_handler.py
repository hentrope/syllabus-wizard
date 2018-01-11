from datatypes import Syllabus, User
from handlers import BaseHandler, uri_for

TEMPLATE = 'public/view'

class ViewHandler(BaseHandler):
    def get(self, instructor, term, name):
        user = User.get_by_auth_id(instructor)
        syll = Syllabus.from_name(user.key, term, name)
        
        if syll is None or not syll.active:
            self.abort(404)
        else:
            sdict = syll.get_dict()
            sdict['standalone'] = True
            sdict['owner'] = user
            sdict['list_url'] = uri_for('public-term', instructor=instructor, term=term)
            self.send_page(TEMPLATE, sdict)