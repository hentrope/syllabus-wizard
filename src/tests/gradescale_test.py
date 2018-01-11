from tests.base import TestBase
from datatypes import GradeScale

class DatastoreTestcases(TestBase):
    def test_add_grade_to_datastore(self):
        grade = GradeScale(letter='A', grademin=90)
        grade.put()
        self.assertEqual(1, len(GradeScale.query().fetch()))