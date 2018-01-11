from tests.base import TestBase
from datatypes import Textbook

class TextbookDatastoreTestcases(TestBase):
    def test_add_to_datastore(self):
        tb = Textbook(title='Intro', author='author', isbn='isbn', publisher='bloomberg')
        tb.put()
        self.assertEqual(1, len(Textbook.query().fetch()), msg=None)
        #tb_list = Textbook.query(Textbook.title == 'Intro').fetch()
        #self.assertEqual(1, len(tb_list), msg=None)
        #self.assertEqual(1, len(tb_list[0]).course)