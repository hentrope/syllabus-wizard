from handlers import user_required, uri_for, AuthHandler
from datatypes import Assessment, Calendar, CourseID, Instructor, MeetingTime, Policy, Section, Syllabus, Term, Textbook
from datetime import date
from sint import sint
from webapp2 import cached_property
import scraper

STEP_LIST = (
    "",
    "Import From Web",
    "Course Information",
    "Additional Sections",
    "Textbooks",
    "Assessments",
    "Grade Scale",
    "Course Policies",
    "Course Calendar",
    "Review & Activate",
)

STEP_TEMP = (
    None,
    'manage/syllabus_1',
    'manage/syllabus_2',
    'manage/syllabus_3',
    'manage/syllabus_4',
    'manage/syllabus_5',
    'manage/syllabus_6',
    'manage/syllabus_7',
    'manage/syllabus_8',
    'manage/syllabus_9',
)
NAV_TOP = 'manage/nav_top'
NAV_BOTTOM = 'manage/nav_bottom'
STEP_1_CONFIRM = 'manage/syllabus_1_confirm'
CREATE_TEMP = 'manage/syllabus_create'
DELETE_TEMP = 'manage/confirm'

class SyllabusHandler(AuthHandler):
    def post(self, term, name, step):
        self.get(term, name, step, True)
    
    @user_required
    def get(self, term, name, step, isPost=False):
        fromStep = sint(self.request.get('from'), -1)
        
        syllabus = Syllabus.from_name(self.user_key, term, name)
        if syllabus is None:
            self.abort(404)
        
        self.handle(isPost, term, name, fromStep, sint(step), syllabus)
    
    def handle(self, isPost, term, name, fromStep, step, syllabus):
        self.syll = syllabus
        self.error = ""

        if isPost:
            self.syll.currstep = step
            
            #if fromStep == 1:
            #    self.post_step_1()
            if fromStep == 2:
                self.post_step_2()
            elif fromStep == 3:
                self.post_step_3()
            elif fromStep == 4:
                self.post_step_4()
            elif fromStep == 5:
                self.post_step_5()
            elif fromStep == 6:
                self.post_step_6()
            elif fromStep == 7:
                self.post_step_7()
            elif fromStep == 8:
                self.post_step_8()
            elif fromStep == 9:
                self.post_step_9()

            self.syll.put()
            
            if self.request.get("jump") == "true":
                jstep = sint(self.request.get("jumpstep"))
                if jstep > 0 and jstep != step:
                    self.redirect(uri_for("edit-syllabus", term=term, name=name, step=jstep), abort=True)
        
        # If we go to step 0, redirect back to the syllabus list
        if step <= 0:
            if self.syll.currstep < 1:
                self.syll.currstep = 1
                self.syll.put()
            self.redirect(uri_for('manage-home'), abort=True)

        dictionary = self.syll.get_dict()
        dictionary.update({
            'syllabus': self.syll,
            'error': self.error,
            'step': step,
            'currstep': self.syll.currstep,
            'step_list': STEP_LIST,
        })
        
        if step == 1:
            dictionary.update(self.step_1_dict())
            
            if len(dictionary["selected_cour"]) > 0 and len(self.request.get("result")) == 0:
                self.send_page(STEP_1_CONFIRM, dictionary)
                return
        
        if 2 <= step <= 3:
            dictionary['instructors'] = self.instructors_list
        
        self.send_page(STEP_TEMP[step], dictionary)
    
    @cached_property
    def instructors_list(self):
        instructors = {'none': self.user.instructor}
        for instructor in Instructor.query_user(self.user_key).fetch():
            iid = str(instructor.key.id())
            instructors[iid] = instructor
        return instructors
    
    def step_1_dict(self):
        dicti = {"selected_cour": ""}
        
        dicti["departments"] = scraper.list_departments(self.syll.term, self.request.get("refresh_dept") == "true")
        dicti["departments"].insert(0, ("", ""))
        
        department = ""
        if self.request.get("submit_dept") == "true":
            department = self.request.get("department")
        else:
            department = self.request.get("selected_dept")
        
        if len(department) > 0:
            dicti["selected_dept"] = department
            
            dicti["courses"] = scraper.list_courses(self.syll.term, department, self.request.get("refresh_cour") == "true")
            dicti["courses"].insert(0, ("", ""))
        
            course = ""
            if self.request.get("submit_cour") == "true":
                course = self.request.get("course")
            else:
                course = self.request.get("selected_cour")
            
            if len(course) > 0:
                dicti["selected_cour"] = course
                
                if self.request.get("result") == "Yes":
                    course_info = scraper.get_course_info(self.syll.term, department, sint(course))
                    self.syll.scrape_populate(course_info)
                    self.syll.put()
                    self.redirect(uri_for("edit-syllabus", term=self.syll.term, name=self.syll.name, step=2))
        
        return dicti

    def post_step_2(self):
        self.syll.course = CourseID.create(self.request.get('dept'), sint(self.request.get('num')))
        self.syll.courseName = self.request.get('course_title')
        self.syll.room = self.request.get('room')
        
        iid = self.request.get('instructor')
        print self.syll.instructor
        if iid == 'none':
            self.syll.instructor = None
        else:
            try:
                self.syll.instructor = self.instructors_list[iid].key
                print "success"
            except KeyError:
                self.syll.instructor = None
        
        i = 1
        for t in self.syll.meetTimes:
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
            self.syll.meetTimes.append(MeetingTime.create())
        elif action != '' and len(self.syll.meetTimes) > 1:
            index = sint(action, -1) - 1
            if index >= 0:
                self.syll.meetTimes.remove(self.syll.meetTimes[index])
        
        self.syll.calendar.update(self.syll.meetTimes)
    
    def post_step_3(self):
        sections = self.syll.sections
        i = 1
        for sect in sections:
            sect.name = self.request.get('name' + str(i))
            sect.room = self.request.get('room' + str(i))
            sect.notes = self.request.get('notes' + str(i))
            
            iid = self.request.get('instructor' + str(i))
            if iid == 'none':
                sect.instructor = None
            else:
                try:
                    sect.instructor = self.instructors_list[iid].key
                except KeyError:
                    sect.instructor = None
            
            i += 1
        
        action = self.request.get('action')

        if action == 'new':
            sections.append(Section.create())
        elif action != '':
            index = sint(action, 0) - 1
            if index >= 0:
                sections.remove(sections[index])

    def post_step_4(self):
        textbooks = self.syll.textbooks
        i = 1
        for t in textbooks:
            t.title = self.request.get('title' + str(i))
            t.edition = self.request.get('edition' + str(i))
            t.author = self.request.get('author' + str(i))
            t.publisher = self.request.get('publisher' + str(i))
            t.year = sint(self.request.get('year' + str(i)))
            t.isbn = self.request.get('isbn' + str(i))
            i += 1
        
        action = self.request.get('action')

        if action == 'new':
            textbooks.append(Textbook.create())
        elif action != '':
            index = sint(action, 0) - 1
            if index >= 0:
                textbooks.remove(textbooks[index])

    def post_step_5(self):
        assessments = self.syll.asmt
        i = 1
        for a in assessments:
            a.name = self.request.get('name' + str(i))
            a.perc = sint(self.request.get('perc' + str(i)))
            a.desc = self.request.get('desc' + str(i))
            i += 1
        
        action = self.request.get('action')

        if action == 'new':
            assessments.append(Assessment.create())
        elif action != '':
            index = sint(action, 0) - 1
            if index >= 0:
                assessments.remove(assessments[index])
    
    def post_step_6(self):
        i = 1
        for gs in self.syll.scale:
            gs.letter = self.request.get('letter' + str(i))
            gs.grademin = sint(self.request.get('grademin' + str(i)))
            i += 1
    
    def post_step_7(self):
        policies = self.syll.policies
        i = 1
        for p in policies:
            p.title = self.request.get('title' + str(i))
            p.desc = self.request.get('desc' + str(i))
            i += 1

        action = self.request.get('action')

        if action == 'new':
            policies.append(Policy.create())
        elif action != '':
            index = sint(action, 0) - 1
            if index >= 0:
                policies.remove(policies[index])
    
    def post_step_8(self):
        self.syll.calendar.notes = self.request.get('notes')
        self.syll.calendar.final = date(Term.term_year(self.syll.term), sint(self.request.get("monthfinal"), 1), sint(self.request.get("dayfinal"), 1))
        self.syll.calendar.final_desc = self.request.get("descfinal")
        
        i = 1
        for cent in self.syll.calendar.entries:
            cent.reading = self.request.get('reading' + str(i)).strip()
            cent.topic = self.request.get('topic' + str(i)).strip()
            i += 1
        self.syll.calendar.weekly = self.request.get('weekly') == 'true'
        
        start = date(Term.term_year(self.syll.term), sint(self.request.get("monthstart"), 1), sint(self.request.get("daystart"), 1))
        end = date(start.year, sint(self.request.get("monthend"), 1), sint(self.request.get("dayend"), 1))
        if end < start:
            end = end.replace(start.year+1)

        self.syll.calendar.update(self.syll.meetTimes, start, end)
    
    def post_step_9(self):
        if len(self.request.get('activate')) > 0:
            self.syll.active = True
        elif len(self.request.get('deactivate')) > 0:
            self.syll.active = False

class SyllabusCreateHandler(AuthHandler):
    def get(self, fterm="", fname=""):
        self.handle(False, fterm, fname)
    def post(self, fterm="", fname=""):
        self.handle(True, fterm, fname)
        
    @user_required
    def handle(self, isPost, fterm, fname):
        error = ""
        old = Syllabus.from_name(self.user_key, fterm, fname)
        sem = self.request.get("sem")
        year = self.request.get("year")
        name = self.request.get("name")

        if isPost:
            sid = Syllabus.build_id_ext(sem, year, name)

            if sint(year) < 2000:
                error = "Year must be 2000 or later."
            elif len(name) < 1:
                error = "Name must be at least 1 character long."
            elif Syllabus.from_id(self.user_key, sid):
                error = "Syllabus with this term and name already exists."
            else:
                syll = Syllabus.create(self.user_key, sid, old=old)
                self.redirect(uri_for('edit-syllabus', term=syll.term, name=syll.name, step=1), abort=True)
        
        if len(sem) == 0:
            sem = Calendar.current_sem()
        if len(year) == 0:
            year = Calendar.current_year()
        
        self.send_page(CREATE_TEMP, {
            'error': error,
            'old': old,
            'sem': sem,
            'year': year,
            'name': name,
        })

class SyllabusDeleteHandler(AuthHandler):
    @user_required
    def get(self, term, name):
        syllabus = Syllabus.from_name(self.user_key, term, name)
        if syllabus is None:
            self.abort(404)
        
        self.send_page(DELETE_TEMP, {
            'type': 'syllabus',
            'term': syllabus.term,
            'name': syllabus.name,
            'title': syllabus.extended_name,
            'details': 'Once deleted, the syllabus cannot be recovered.',
        })
    
    @user_required
    def post(self, term, name):
        if self.request.get("result") == "Yes":
            Syllabus.remove_by_name(self.user_key, term, name)
        self.redirect(uri_for("manage-home"))
            