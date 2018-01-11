from handlers import user_required, uri_for, AuthHandler
from datatypes import Instructor, Term
from sint import sint

LIST_TEMP = 'manage/instructor'
OFFICE_TEMP = 'manage/instructor_office'

class InstructorViewHandler(AuthHandler):
    def post(self):
        self.handle(True)
    def get(self):
        self.handle(False)
    
    @user_required
    def handle(self, isPost):
        # Fetch all instructor instances, place them in a dictionary based on key
        instructors = {}
        for instructor in Instructor.query_user(self.user_key).fetch():
            iid = str(instructor.key.id())
            instructors[iid] = instructor
            
            if isPost:
                instructor.name = self.user.full_name = self.request.get('name-' + iid)
                instructor.email = self.request.get('email-' + iid)
                instructor.put()
        
        if isPost:
            action = self.request.get('action')
            if action.startswith('off-'):
                iid = action[4:]
                term = Term.build_term(self.request.get('sem-' + iid), self.request.get('year-' + iid))
                self.redirect(uri_for('manage-instructor-office', iid=iid, term=term), True)
            elif action.startswith('del-'):
                iid = action[4:]
                instructors[iid].key.delete()
                del instructors[iid]
            elif action == 'new':
                instructor = Instructor.create(self.user_key)
                instructor.put()
                instructors[str(instructor.key.id())] = instructor

        self.send_page(LIST_TEMP, {
            'instructors': instructors,
        })

class InstructorOfficeHandler(AuthHandler):
    def get(self, term, iid=None):
        self.handle(False, iid, term)
    def post(self, term, iid=None):
        self.handle(True, iid, term)
    
    @user_required        
    def handle(self, isPost, iid, term):
        if iid is None:
            instructor = self.user.instructor
            office = instructor.get_office_user_term(self.user_key, term)
        else:
            instructor = Instructor.get_by_id(sint(iid), parent=self.user_key)
            office = instructor.get_office_term(term)
        
        if isPost:
            office.room = self.request.get("room")
            office.phone = self.request.get("phone")
            
            i = 1
            for t in office.times:
                t.weekday = sint(self.request.get('day'+str(i)))
                t.set_start_12h(
                    sint(self.request.get('starth'+str(i))),
                    sint(self.request.get('startm'+str(i))),
                    self.request.get('startp'+str(i)) == 'y')
                t.set_dur(
                    sint(self.request.get('durh'+str(i))),
                    sint(self.request.get('durm'+str(i))))
                i += 1
    
            action = self.request.get('action')
            if action == 'new':
                office.add()
            elif action != '' and action != 'return':
                index = sint(action, -1)
                if index >= 0:
                    office.remove_index(index)
            
            office.put()
            
            if action == 'return':
                if iid is None:
                    self.redirect(uri_for('manage-profile'), abort=True)
                else:
                    self.redirect(uri_for('manage-instructor'), abort=True)
        
        self.send_page(OFFICE_TEMP, {
            'instructor': instructor,
            'office': office,
            'term': term,
            'term_name': Term.get_extended(term),
        })