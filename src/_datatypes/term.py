from sint import sint
#from datatypes import SEMESTERS
from datetime import date, timedelta

"""
Term is stored as a string, and is not a proper datatype.
This string has a specific format. The first character of
the string specifies the semester in which the term takes
place, while the remaining characters are all digits that
are equal to the year minus 2000.
"""

SEMESTERS = {'F':'Fall', 'W': 'Winter', 'S': 'Spring', 'M': 'Summer', }

FALL = 'F'
WINTER = 'W'
SPRING = 'S'
SUMMER = 'M'

YEAR_OFFSET = 2000

class Term():
    @classmethod
    def build_term(cls, sem, year):
        return sem.upper() + str( sint(year, 2000) - YEAR_OFFSET )
    
    @classmethod
    def term_sem(cls, term):
        return term[:1]
    
    @classmethod
    def term_year(cls, term):
        return sint(term[1:]) + 2000
    
    @classmethod
    def term_num(cls, term):
        sem = cls.term_sem(term)
        year = cls.term_year(term)
        ret = 2000 + (year-2000)*10
        
        if sem == FALL:
            return ret + 9
        elif sem == WINTER:
            return ret + 1
        elif sem == SPRING:
            return ret + 2
        elif sem == SUMMER:
            return ret + 6
    
    @classmethod
    def get_extended(cls, term):
        return SEMESTERS[cls.term_sem(term)] + " " + str(cls.term_year(term))

    @classmethod
    def start_date(cls, term):
        sem = cls.term_sem(term)
        year = cls.term_year(term)
        
        if (sem == FALL):
            d = date(year, 9, 1)
            wd = d.weekday()
            if (wd <= 2):
                d = d.replace(day = 2)
            else:
                d = d.replace(day = 9 - wd)
            return d
        elif (sem == SPRING):
            d = date(year, 1, 1)
            wd = d.weekday()
            if (wd <= 1):
                d = d.replace(day = 22)
            elif (wd == 2):
                d = d.replace(day = 21)
            else:
                d = d.replace(day = 29 - wd)
            return d
        elif (sem == WINTER):
            d = date(year, 1, 1)
            wd = d.weekday()
            if (wd <= 2):
                d = d.replace(day = 2)
            elif (wd <= 5):
                d = d.replace(day = 8 - wd)
            else:
                d = d.replace(day = 3)
            return d
        else:
            return date(year, 6, 1)
    
    @classmethod
    def end_date(cls, term):
        sem = cls.term_sem(term)
        
        if (sem == FALL):
            return cls.start_date(term) + timedelta(weeks=15)
        elif (sem == SPRING):
            return cls.start_date(term) + timedelta(weeks=16)
        elif (sem == WINTER):
            return cls.start_date(term) + timedelta(weeks=2)
        else:
            return cls.start_date(term) + timedelta(weeks=6)