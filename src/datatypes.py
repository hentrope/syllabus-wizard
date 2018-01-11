# This just imports the classes from the separate modules to make imports cleaner

SEMESTERS = {'F':'Fall', 'W': 'Winter', 'S': 'Spring', 'M': 'Summer', }
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
WEEKDAY_CHARS = ['M', 'T', 'W', 'R', 'F', 'S', 'U']

from _datatypes.meeting_times import MeetingTime
from _datatypes.term import Term

from _datatypes.assessment import Assessment
from _datatypes.calendar import Calendar
from _datatypes.course_id import CourseID
from _datatypes.grade_scale import GradeScale
from _datatypes.instructor import Instructor
from _datatypes.policy import Policy
from _datatypes.section import Section
from _datatypes.textbook import Textbook

from _datatypes.syllabus import Syllabus
from _datatypes.user import User