"""
import webapp2
import unittest
from datatypes import CalendarEntry

class CalenderTest():#unittest.TestCase):
    def test_start_date(self):
        self.assertEqual(start_date(2004, "FALL"), date(2004, 9, 2))
        
        self.assertEqual(start_date(2005, "WINTER"), date(2005, 1, 3))
        self.assertEqual(start_date(2005, "SPRING"), date(2005, 1, 24))
        self.assertEqual(start_date(2005, "FALL"), date(2005, 9, 6))
        
        self.assertEqual(start_date(2006, "WINTER"), date(2006, 1, 3))
        self.assertEqual(start_date(2006, "SPRING"), date(2006, 1, 23))
        self.assertEqual(start_date(2006, "FALL"), date(2006, 9, 5))
        
        self.assertEqual(start_date(2007, "WINTER"), date(2007, 1, 2))
        self.assertEqual(start_date(2007, "SPRING"), date(2007, 1, 22))
        self.assertEqual(start_date(2007, "FALL"), date(2007, 9, 4))
        
        self.assertEqual(start_date(2008, "WINTER"), date(2008, 1, 2))
        self.assertEqual(start_date(2008, "SPRING"), date(2008, 1, 22))
        self.assertEqual(start_date(2008, "FALL"), date(2008, 9, 2))
        
        self.assertEqual(start_date(2009, "WINTER"), date(2009, 1, 5))
        self.assertEqual(start_date(2009, "SPRING"), date(2009, 1, 26))
        self.assertEqual(start_date(2009, "FALL"), date(2009, 9, 2))
        
        self.assertEqual(start_date(2010, "WINTER"), date(2010, 1, 4))
        self.assertEqual(start_date(2010, "SPRING"), date(2010, 1, 25))
        self.assertEqual(start_date(2010, "FALL"), date(2010, 9, 2))
        
        self.assertEqual(start_date(2011, "WINTER"), date(2011, 1, 3))
        self.assertEqual(start_date(2011, "SPRING"), date(2011, 1, 24))
        self.assertEqual(start_date(2011, "FALL"), date(2011, 9, 6))
        
        self.assertEqual(start_date(2012, "WINTER"), date(2012, 1, 3))
        self.assertEqual(start_date(2012, "SPRING"), date(2012, 1, 23))
        self.assertEqual(start_date(2012, "FALL"), date(2012, 9, 4))
        
        self.assertEqual(start_date(2013, "WINTER"), date(2013, 1, 2))
        self.assertEqual(start_date(2013, "SPRING"), date(2013, 1, 22))
        self.assertEqual(start_date(2013, "FALL"), date(2013, 9, 3))
        
        self.assertEqual(start_date(2014, "WINTER"), date(2014, 1, 2))
        self.assertEqual(start_date(2014, "SPRING"), date(2014, 1, 21))
        self.assertEqual(start_date(2014, "FALL"), date(2014, 9, 2))
        
        self.assertEqual(start_date(2015, "WINTER"), date(2015, 1, 5))
        self.assertEqual(start_date(2015, "SPRING"), date(2015, 1, 26))
        self.assertEqual(start_date(2015, "FALL"), date(2015, 9, 2))
        
        self.assertEqual(start_date(2016, "WINTER"), date(2016, 1, 4))
        self.assertEqual(start_date(2016, "SPRING"), date(2016, 1, 25))
    
    def test_term_length(self):
        self.assertEqual(term_length_weeks("FALL"), 16)
        self.assertEqual(term_length_weeks("WINTER"), 3)
        self.assertEqual(term_length_weeks("SPRING"), 17)
    
    def test_generate_calender(self):
        start = start_date(2015, "FALL")
        length = term_length_weeks("FALL")
        cal = generate_calendar(start, length)
        
        self.assertEquals(len(cal), length)
        self.assertEquals(cal[0].day, start)"""
