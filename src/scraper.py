from bs4 import BeautifulSoup
from google.appengine.ext import ndb
from urllib import urlencode
from urllib2 import Request, urlopen
from _datatypes.term import Term
import re

class TermModel(ndb.Model):
    @classmethod
    def get_or_create(cls, term):
        model = cls.get_by_id(term, None)
        if model == None:
            model = cls.create(term)
            model.put()
        return model
    
    @classmethod
    def create(cls, term):
        return cls(id=term)

class DepartmentModel(ndb.Model):
    name = ndb.StringProperty(required=True, indexed=False)
    
    @classmethod
    def get_or_create(cls, department, term_key):
        model = cls.get_by_id(department, term_key)
        if model == None:
            model = cls.create(department, term_key)
            model.put()
        return model
    
    @classmethod
    def create(cls, department, term_key):
        return cls(id=department, parent=term_key)

class CourseSection(ndb.Model):
    name = ndb.StringProperty(required=True, indexed=False)
    hours = ndb.StringProperty(required=True, indexed=False)
    days = ndb.StringProperty(required=True, indexed=False)
    instructor = ndb.StringProperty(required=True, indexed=False)
    room = ndb.StringProperty(required=True, indexed=False)
    
    @classmethod
    def create(cls):
        return cls(hours="", days="", instructor="", room="")

class CourseModel(ndb.Model):
    name = ndb.StringProperty(required=True)
    sections = ndb.StructuredProperty(CourseSection, repeated=True)

    @classmethod
    def create(cls, course_num, department_key):
        return cls(id=course_num, parent=department_key)

def scrape_term(term):
    term_num = Term.term_num(term.key.string_id())
    page = urlopen("http://www4.uwm.edu/schedule/index.cfm?a1=search&strm=" + str(term_num)).read()
    soup = BeautifulSoup(page, "html.parser")
    select = soup.find("select", attrs={"name":"subject"})
    options = select.find_all("option")
    
    for key in DepartmentModel.query(ancestor=term.key).iter(keys_only=True):
        key.delete()
    
    ret = []
    for option in options:
        value = option["value"]
        if not value == "ALL":
            data = DepartmentModel.create(value, term.key)
            data.name = option.text.strip()
            data.put()
            ret.append(data)

    return ret

def scrape_department(term, department):
    term_num = Term.term_num(term.key.string_id())
    department_name = department.key.id()
    url = "http://www4.uwm.edu/schedule/pdf/pf_dsp_soc_search_results.cfm"
    values = urlencode({
        "strm": term_num,
        "subject": department_name,
        "term_descr": "",
        "term_season": "",
        "mon": "0",
        "tue": "0",
        "wed": "0",
        "thu": "0",
        "fri": "0",
        "sat": "0",
        "sun": "0",
        "gergroup": "100",
        "checkurl": "N",
        "category": "",
        "lastname": "",
        "firstname": "",
        "EXACTWORDPHRASE": "",
        "COURSETYPE": "ALL",
        "timerangefrom": "",
        "timerangeto": "",
        "datebeginning": "",
        "school": "ALL",
        "school_descrformal": "",
        "results_title": "",
        "term_status": "L",
        "datasource": "cf_web_soc",
        "subjdtlhide": "false",
    })
    page = urlopen(Request(url, values)).read()
    
    splits = page.split('<span class="subhead">')
    splits.pop(0) # First entry is just the garbage in header
    
    for key in CourseModel.query(ancestor=department.key).iter(keys_only=True):
        key.delete()
    
    ret = []
    for split in splits:
        course_name = split[:split.find(':')]
        course_num = int(re.findall('\d+', course_name)[0])
        data = CourseModel.create(course_num, department.key)
        
        data.name = split[split.find(': ')+2:split.find('<')]
        
        soup = BeautifulSoup(split, "html.parser")
        table = soup.find('table', attrs={'border': '0',
                                          'cellpadding': '0',
                                          'cellspacing': '0',
                                          'width': '100%' })
        rows = table.find_all('tr', attrs={'class': 'body copy'})
        
        prevcol = None
        for row in rows:
            if prevcol == None or row['bgcolor'] != prevcol:
                section = CourseSection.create()
                data.sections.append(section)
                prevcol = row['bgcolor']
            else:
                section = data.sections[-1]

            cols = row.find_all('td')
            if len(cols) >= 10:
                if len(section.hours) > 0:
                    section.hours += ", "
                section.hours += cols[5].text.strip()
                
                for c in cols[6].text.strip():
                    if section.days.find(c) < 0:
                        section.days += c
                    
                name = cols[3].text.strip()
                if len(name) > 0:
                    section.name = name
                
                instructor = cols[8].text.strip()
                if len(instructor ) > 0:
                    section.instructor  = instructor 
                    
                room = cols[9].text.strip()
                if len(room) > 0:
                    section.room = room
        
        data.put()
        ret.append(data)

    return ret

def get_term_model(term):
    model = TermModel.get_by_id(term, None)
    if model == None:
        model = TermModel.create(term)
        model.put()

def get_depar_model(term):
    model = TermModel.get_by_id(term, None)
    if model == None:
        model = TermModel.create(term)
        model.put()

def list_departments(term, refresh=False):
    term_model = TermModel.get_or_create(term)
    
    if refresh:
        departments = scrape_term(term_model)
    else:
        departments = DepartmentModel.query(ancestor=term_model.key).fetch()
        if len(departments) == 0:
            departments = scrape_term(term_model)
    
    ret = []
    for dep in departments:
        ret.append( (dep.key.string_id(), dep.name) )
    return ret

def list_courses(term, department, refresh=False):
    term_model = TermModel.get_or_create(term)
    department_model = DepartmentModel.get_or_create(department, term_model.key)
    
    if refresh:
        courses = scrape_department(term_model, department_model)
    else:
        courses = CourseModel.query(ancestor=department_model.key).order(CourseModel.key).fetch(projection=[CourseModel.name])
        if len(courses) == 0:
            courses = scrape_department(term_model, department_model)
    
    ret = []
    for course in courses:
        ret.append( (course.key.id(), course.name) )
    return ret

def get_course_info(term, department, number):
    term_model = TermModel.get_or_create(term)
    department_model = DepartmentModel.get_or_create(department, term_model.key)
    course_model = CourseModel.get_by_id(number, department_model.key)
    
    if course_model is None:
        return None
    
    return (department_model.key.string_id(), int(course_model.key.id()), course_model.name, course_model.sections)