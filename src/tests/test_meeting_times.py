from tests.base import TestBase
from datatypes import MeetingTime

class MeetingTimeTest(TestBase):
    def test_add_to_Datastore(self):
        mtime = MeetingTime(weekday=4, startMins=600, durMins=50)
        mtime.put()
        self.assertEqual(1, len(MeetingTime.query().fetch()))
        
    def test_getstartHour(self):
        m = MeetingTime(startMins=600)
        self.assertEqual(m.get_start_hour(), 10)
        
    def test_getstartHour_12h(self):
        m = MeetingTime(startMins=50)
        self.assertEqual(m.get_start_hour(), 0)
            
    def test_get_start_pm(self):
        m = MeetingTime(startMins=1200)
        m.get_start_pm()
        self.assertTrue(m.get_start_pm())
        
    def test_get_start_min(self):
        m = MeetingTime(startMins=50)
        self.assertEqual(m.get_start_min(), 50)
    
    def test_getDurHour(self):
        start = MeetingTime(weekday=2, startMins=600, durMins=50)
        self.assertEqual(start.get_dur_hour(), 0)
        
    def test_getDurMin(self):
        start = MeetingTime(weekday=2, startMins=600, durMins=50)
        self.assertEqual(start.get_dur_min(), 50)
        
    def test_set_start(self):
        i = MeetingTime(startMins=0)
        i.set_start(1,50)
        self.assertEqual(i.startMins, 110)
        
    def test_set_dur(self):
        i = MeetingTime(durMins=0)
        i.set_dur(1,45)
        self.assertEqual(i.durMins, 105)