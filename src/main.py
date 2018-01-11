#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'password'

from webapp2 import WSGIApplication, Route
from webapp2_extras.routes import PathPrefixRoute, RedirectRoute

from manage.admin_handlers import AdminHandler, AdminDeleteHandler
from manage.main_handlers import HomeHandler, ProfileHandler
from manage.syllabus_handlers import SyllabusHandler, SyllabusCreateHandler, SyllabusDeleteHandler
from manage.instructor_handlers import InstructorViewHandler, InstructorOfficeHandler

from public.index_handler import IndexHandler
from public.login_handlers import LoginHandler, LogoutHandler
from public.term_handler import TermHandler
from public.view_handler import ViewHandler

app = WSGIApplication([
    RedirectRoute('/manage', redirect_to_name='manage-home'), #fixes stupid trailing slash thing
    PathPrefixRoute('/manage', [
        Route('/', HomeHandler, 'manage-home'),
        Route('/profile/<term>', InstructorOfficeHandler, 'manage-profile-office'),
        Route('/profile', ProfileHandler, 'manage-profile'),
        Route('/syllabus/create', SyllabusCreateHandler, 'create-syllabus'),
        Route('/syllabus/<fterm>/<fname>/duplicate', SyllabusCreateHandler, 'duplicate-syllabus'),
        Route('/syllabus/<term>/<name>/delete', SyllabusDeleteHandler, 'delete-syllabus'),
        Route('/syllabus/<term>/<name>/<step>', SyllabusHandler, 'edit-syllabus'),
        Route('/instructor', InstructorViewHandler, 'manage-instructor'),
        Route('/instructor/<iid>/<term>', InstructorOfficeHandler, 'manage-instructor-office'),
    ]),
    
    RedirectRoute('/admin', redirect_to_name='admin-home'), #fixes stupid trailing slash thing
    PathPrefixRoute('/admin', [
        Route('/', AdminHandler, 'admin-home'),
        Route('/<uid>/delete', AdminDeleteHandler, 'admin-delete'),
    ]),
    
    Route('/', IndexHandler, 'index'),
    Route('/static/<path:.+>', None, 'static'),
    Route('/login', LoginHandler, 'login'),
    Route('/logout', LogoutHandler, 'logout'),
    Route('/<instructor>/<term>', TermHandler, 'public-term'),
    Route('/<instructor>/<term>/<name>', ViewHandler, 'public-view'),
], debug=True, config={
    'webapp2_extras.auth': {'user_model': '_datatypes.user.User', 'user_attributes': ['auth_ids']},
    'webapp2_extras.sessions': {'secret_key': 'I_wanted2eatPotato1nce'}
})
