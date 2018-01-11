from datatypes import Calendar, SEMESTERS, MONTHS, WEEKDAYS
from jinja2 import Environment, FileSystemLoader
from os import path
from webapp2 import uri_for

JINJA_ENVIRONMENT = Environment(
    loader=FileSystemLoader(path.join(path.dirname(__file__), '_templates')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
JINJA_ENVIRONMENT.globals = {
        'uri_for': uri_for,
        'range': range,
        'current_sem': Calendar.current_sem,
        'current_year': Calendar.current_year,
        'semesters': SEMESTERS,
        'months': MONTHS,
        'weekdays': WEEKDAYS,
    }
JINJA_ENVIRONMENT.trim_blocks = True;
JINJA_ENVIRONMENT.lstrip_blocks = True;

def get_template(name, parent=None, globals=None):
    return JINJA_ENVIRONMENT.get_template(name + '.html', parent, globals)