from handlers import BaseHandler, uri_for

class IndexHandler(BaseHandler):
    def get(self):
        self.redirect(uri_for('login'))