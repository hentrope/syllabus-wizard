from tests.base import TestBase
from datatypes import Policy

class TextbookDatastoreTestcases(TestBase):
    def test_add_to_datastore(self):
        policy = Policy(title='policy', desc='policy desc goes here')
        policy.put()
        self.assertEqual(1, len(Policy.query().fetch()))