from tests.base import TestBase
from datatypes import Assessment

class test_Datastore(TestBase):
    def test_add_assessment_to_datastore(self):
        asmt = Assessment(name='Project', perc = 40, desc = 'final project')
        asmt.put()
        self.assertEqual(1, len(Assessment.query().fetch()))