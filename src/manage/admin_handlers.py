from datatypes import Instructor, User
from handlers import ADMIN_USERNAME, AuthHandler, admin_required, uri_for
from sint import sint
import time

HOME_TEMP = 'admin/home'
CONFIRM_TEMP = 'manage/confirm'

class AdminHandler(AuthHandler):
    def get(self):
        self.handle(False)
    def post(self):
        self.handle(True)
        
    @admin_required
    def handle(self, isPost):
        error = ''
        
        if isPost:
            username = self.request.get('username')
            password = self.request.get('password')
            success, newuser = self.user_model.create_user(username, password_raw=password)
            
            if not success:
                error = 'User with given username already exists.'
            
            newuser.instructor = Instructor.create(newuser.key)
            newuser.put()
            
            time.sleep(1)
            
        lst = list(User.query().fetch())
        
        for user in lst:
            if user.name == ADMIN_USERNAME:
                lst.remove(user)
                break;
        
        self.send_page(HOME_TEMP, {
            'error': error,
            'users': lst,
            'username': self.user_name,
        })
        
class AdminDeleteHandler(AuthHandler):
    def get(self, uid):
        self.handle(uid, False)
    def post(self, uid):
        self.handle(uid, True)

    @admin_required
    def handle(self, uid, isPost):
        user = self.user_model.get_by_id(sint(uid))
        
        if user is None:
            self.redirect(uri_for('admin-home'))
        elif isPost:
            if self.request.get('result') == 'Yes':
                self.user_model.delete_user(user)
            time.sleep(1)
            self.redirect(uri_for('admin-home'))
        else:
            self.send_page(CONFIRM_TEMP, {
                'type': 'user',
                'name': user.name,
                'id': user.key.id(),
                'details': 'This user and his/her syllabi will be deleted.',
            })