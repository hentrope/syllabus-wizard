import sys, unittest
from google.appengine.ext import ndb, testbed
sys.modules['ndb'] = ndb

class TestBase(unittest.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        ndb.get_context().clear_cache()
    
    def tearDown(self):
        self.testbed.deactivate()

"""
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

suite = unittest.TestLoader().loadTestsFromTestCase(DatastoreTestcases)
unittest.TextTestRunner(verbosity=2).run(suite)
"""