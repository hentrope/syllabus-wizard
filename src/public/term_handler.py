from datatypes import Syllabus, User
from handlers import BaseHandler

TEMPLATE = 'public/term'

class TermHandler(BaseHandler):
    def get(self, instructor, term):
        user = User.get_by_auth_id(instructor)
        
        if user is None:
            self.abort(404)
        
        syllabi = Syllabus.query_user_term_active(user.key, term).fetch()
        office_term = user.instructor.get_office_user_term(user.key, term)
        office_times = office_term.times if office_term is not None else []
        
        if len(office_times) == 0 and len(syllabi) == 0:
            self.abort(404)

        self.send_page(TEMPLATE, {
            'heading': "<span>Course List - " + user.instructor.name + "</span>",
            'syllabi': syllabi,
            'calendar': self.generate_calendar(office_times, syllabi),
        })
    
    def generate_calendar(self, office_times, syllabi):
        calendar = []
        for i in range(24):
            calendar.append([])
        
        for time in office_times:
            hour = time.get_start_hour()
            if 0 <= hour < 24:
                calendar[hour].append(self.get_time_tuple(time, "Office"))
        
        for syllabus in syllabi:
            classname = syllabus.course.dept + ' ' + str(syllabus.course.num)
            for time in syllabus.meetTimes:
                hour = time.get_start_hour()
                if 0 <= hour < 24:
                    calendar[hour].append(self.get_time_tuple(time, classname))

        return calendar
    
    def get_time_tuple(self, time, title):
        return (time.weekday, title, time.get_start_string(), time.get_end_string())