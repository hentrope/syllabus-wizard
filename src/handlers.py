from google.appengine.ext import ndb
from main import ADMIN_USERNAME, ADMIN_PASSWORD
from templates import get_template
from webapp2 import RequestHandler, cached_property, uri_for
from webapp2_extras import auth, sessions

class BaseHandler(RequestHandler):
    def send_page(self, template, page_dict):
        self.response.write(get_template(template).render(page_dict))

class AuthHandler(BaseHandler):
    def send_page(self, template, page_dict):
        if self.user_info:
            if page_dict is None:
                page_dict = {}
            page_dict['username'] = self.user_name

        super(AuthHandler, self).send_page(template, page_dict)
    
    # Shortcut to access the auth instance as a property.
    @cached_property
    def auth(self):
        return auth.get_auth()
    
    # Returns the user info from the current user session.
    @cached_property
    def user_info(self):
        return self.auth.get_user_by_session()
    
    @cached_property
    def user_name(self):
        return self.user_info['auth_ids'][0]
    
    # Returns the User instance from the provided user_info.
    @cached_property
    def user(self):
        return self.user_model.get_by_id(self.user_info['user_id']) if self.user_info else None

    # Returns the User key from the provided user_info.
    @cached_property
    def user_key(self):
        return ndb.Key('User', self.user_info['user_id']) if self.user_info else None
    
    # Returns the implementation of the user model.
    @cached_property
    def user_model(self):
        return self.auth.store.user_model
    
    # Shortcut to access the current session.
    @cached_property
    def session(self):
        return self.session_store.get_session(backend="datastore")
    
    # This is needed for webapp2 sessions to work
    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

# Decorator that checks if there's a user associated with the current session. 
# Will also fail and redirect to login if there's no session present.
# Only works with AuthHandler
def user_required(handler):
    def check_login(self, *args, **kwargs):
        if self.user_info and self.user_name != ADMIN_USERNAME:
            return handler(self, *args, **kwargs)
        else:
            self.redirect(uri_for('login'), abort=True)
    return check_login

def admin_required(handler):
    def check_login(self, *args, **kwargs):
        if self.user_info and self.user_name == ADMIN_USERNAME:
            return handler(self, *args, **kwargs)
        else:
            self.redirect(uri_for('login'), abort=True)
    return check_login