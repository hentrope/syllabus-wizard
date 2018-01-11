from datatypes import User
from handlers import uri_for, AuthHandler, ADMIN_USERNAME, ADMIN_PASSWORD
from webapp2_extras.auth import InvalidAuthIdError, InvalidPasswordError

TEMPLATE = 'public/login'

class LoginHandler(AuthHandler):
    def get(self):
        self.handle(False)
    def post(self):
        self.handle(True)
            
    def handle(self, isPost):
        error=""
        if isPost:
            username = self.request.get('user')
            password = self.request.get('pass')
            try:
                self.auth.get_user_by_password(username, password, remember=True, save_session=True)
            except (InvalidAuthIdError, InvalidPasswordError):
                error = "Invalid username/password."
        
        if self.user_info:
            if self.user_name == ADMIN_USERNAME:
                self.redirect(uri_for('admin-home'))
            else:
                self.redirect(uri_for('manage-home'))
        else:
            if User.get_by_auth_id(ADMIN_USERNAME) is None:
                self.user_model.create_user(ADMIN_USERNAME, password_raw=ADMIN_PASSWORD)

            self.send_page(TEMPLATE, {'error':error})
        
    # returns user_data, "if not user_data[0]" means not created
    def create_user(self, username, password):
        return self.user_model.create_user(username, password_raw=password)

class LogoutHandler(AuthHandler):
    def post(self):
        self.get()

    def get(self):
        self.auth.unset_session()
        self.redirect(self.uri_for('manage-home'))