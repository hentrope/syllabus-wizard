from datatypes import Syllabus, Term
from handlers import uri_for, user_required, AuthHandler
from webapp2_extras.auth import InvalidAuthIdError, InvalidPasswordError

HOME_TEMP = 'manage/home'
PROFILE_TEMP = 'manage/profile'
OFFICE_TEMP = 'manage/profile_office'

class HomeHandler(AuthHandler):
    @user_required
    def get(self):
        self.send_page(HOME_TEMP, {
            'syllabi': Syllabus.query_user(self.user_key).fetch(),
        })
        
class ProfileHandler(AuthHandler):
    def get(self):
        self.handle(False)
    def post(self):
        self.handle(True)
        
    @user_required
    def handle(self, isPost):
        error=""
        
        if isPost:
            self.user.instructor.name = self.request.get('name')
            self.user.instructor.email = self.request.get('email')
            
            newpass = self.request.get('newpass1')
            if len(newpass) > 0:
                if newpass != self.request.get('newpass2'):
                    error = "New password does not match."
                else:
                    try:
                        retdict = self.auth.get_user_by_password(self.user_name, self.request.get('oldpass'), save_session=False)
                        
                        if retdict['user_id'] == self.user_info['user_id']:
                            self.user.set_password(newpass)
                            error = "Password change successful."
                        else:
                            error = "Invalid session."
                    except (InvalidAuthIdError, InvalidPasswordError):
                        error = "Invalid password."

            self.user.put()

            if self.request.get('action') == 'office':
                term = Term.build_term(self.request.get('sem'), self.request.get('year'))
                self.redirect(uri_for('manage-profile-office', term=term), True)
        
        self.send_page(PROFILE_TEMP, {
            'instructor': self.user.instructor,
            'error': error,
        })