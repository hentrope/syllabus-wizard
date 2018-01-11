from datatypes import Assessment, Calendar, CourseID, GradeScale, Instructor, MeetingTime, Policy, Section, Term, Textbook
from google.appengine.ext import ndb
from webapp2 import cached_property

class Syllabus(ndb.Model):
    term = ndb.StringProperty(indexed=True, required=True)
    active = ndb.BooleanProperty(default=False, indexed=True)
    currstep = ndb.IntegerProperty(default=1, indexed=False)
    
    course = ndb.StructuredProperty(CourseID, default=CourseID.create("",0))
    courseName = ndb.StringProperty(default="unnamed", indexed=False)
    room = ndb.StringProperty(default="", indexed=False)
    instructor = ndb.KeyProperty(Instructor, default=None)
    suggestion = ndb.StringProperty(indexed=False, default="", required=True)
    sections = ndb.StructuredProperty(Section, repeated=True)
    textbooks = ndb.StructuredProperty(Textbook, repeated=True)
    asmt = ndb.StructuredProperty(Assessment, repeated=True)
    scale = ndb.StructuredProperty(GradeScale, repeated=True)
    policies = ndb.StructuredProperty(Policy, repeated=True)
    meetTimes = ndb.StructuredProperty(MeetingTime, repeated=True)
    calendar = ndb.StructuredProperty(Calendar)
    
    @cached_property
    def owner(self):
        return self.key.parent().get()
    
    @cached_property
    def name(self):
        return self.key.string_id().split("/")[1]
    
    @cached_property
    def extended_name(self):
        return self.course.dept + ' ' + str(self.course.num) + ' - ' + self.courseName
    
    @cached_property
    def term_string(self):
        return Term.get_extended(self.term)
    
    @cached_property
    def instructor_instance(self):
        if self.instructor is None:
            return self.owner.instructor
        else:
            return self.instructor.get()
    
    @cached_property
    def schedule_string(self):
        return MeetingTime.build_string(self.meetTimes, True)

    def get_dict(self):
        return {
            'owner': self.owner,
            'term': self.term,
            'term_string': self.term_string,
            'name': self.name,
            'course': self.course,
            'course_title': self.courseName,
            'instructor': self.instructor_instance,
            'course_room': self.room,
            'schedule_string': self.schedule_string,
            'sections': self.sections,
            'textbooks': self.textbooks,
            'assessments': self.asmt,
            'gradescale': self.scale,
            'policies': self.policies,
            'meeting_times': self.meetTimes,
            'calendar': self.calendar,
        }
    
    def scrape_populate(self, course_info):
        self.course.dept = course_info[0]
        self.course.num = course_info[1]
        self.courseName = course_info[2]
        
        sections = course_info[3]
        if len(sections) > 0:
            self.room = sections[0].room
            self.meetTimes = MeetingTime.parse_strings(sections[0].days, sections[0].hours)
            self.suggestion = sections[0].instructor
            
            self.sections = []
            for sect_data in sections[1:]:
                section = Section.create(sect_data.name, sect_data.room, sect_data.days + " " + sect_data.hours, None, sect_data.instructor)
                self.sections.append(section)
        print "will modify here"

    @classmethod
    def query_user(cls, user_key):
        return cls.query(ancestor=user_key)
    
    @classmethod
    def query_user_term(cls, user_key, term):
        return cls.query_user(user_key).filter(Syllabus.term == term)
    
    @classmethod
    def query_user_term_active(cls, user_key, term):
        return cls.query_user(user_key).filter(ndb.AND(Syllabus.term == term, Syllabus.active == True))
    
    @classmethod
    def build_id(cls, term, name):
        return term.upper() + "/" + name.replace("/", "")
    
    @classmethod
    def build_id_ext(cls, semester, year, name):
        return cls.build_id(Term.build_term(semester, year), name)
    
    @classmethod
    def from_id(cls, user_key, sid):
        return cls.get_by_id(sid, parent=user_key)
    
    @classmethod
    def from_name(cls, user_key, term, name):
        return cls.from_id(user_key, cls.build_id(term, name))
    
    @classmethod
    def remove_by_name(cls, user_key, term, name):
        ndb.Key('Syllabus', cls.build_id(term, name), parent=user_key).delete()

    @classmethod
    def create(cls, user_key, sid, old=None):
        if user_key is None or not user_key.kind() == 'User':
            raise ValueError("Invalid parent.")
        term = sid.split("/")[0]
        
        syllabus = Syllabus(id=sid, parent=user_key, term=term)
        
        if old is None:
            syllabus.populate(**{
                'meetTimes': [MeetingTime.create()],
                'sections': [],
                'textbooks': [],
                'asmt': [],
                'scale': [GradeScale.create() for i in range(14)],
                'policies': [],
                'calendar': Calendar.create(term),
            })
        else:
            syllabus.populate(**old.to_dict())
        
        syllabus.term = term
        syllabus.calendar.update(syllabus.meetTimes, Term.start_date(term), Term.end_date(term))
        syllabus.active = False
        syllabus.currstep = 1
        
        syllabus.put()
        return syllabus