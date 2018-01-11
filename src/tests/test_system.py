from tests.base import TestBase
from datatypes import Syllabus, Term, User

class TestSystem(TestBase):
    def test_system_1(self):
        # Create the user, no need to simulate logging in
        success, user = User.create_user("test", password_raw="test")
        self.assertEqual(success, True, "Unable to create user \"test\".")
        
        # Create the syllabus
            #term = Term.build_term("F", "2015")
        syllabus = Syllabus.create(user.key, "F15/test")
        
        # Modify the syllabus as if you were manually setting TAs, textbooks, etc.
        "Blah Blah do stuff here"
        
        # Test the dictionary created by the syllabus
        di = syllabus.get_dict()
        self.assertIsNotNone(di['term']) # For basically all of the different keys of the dictionary
        
        """ List of all the dictionary keys for your convenience
            'term': self.get_term_instance(),
            'name': self.name,
            'course': self.course,
            'course_title': self.courseName,
            'ta_list': self.taList,
            'textbooks': self.textbooks,
            'Assessments': self.asmt,
            'gradescale': self.scale,
            'policies': self.policies,
            'meeting_times': self.meetTimes,
            'calendar_notes': self.calendarnotes,
            'calendar': self.calendar,
        """