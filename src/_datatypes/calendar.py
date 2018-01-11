from copy import copy
from datatypes import Term
from datetime import datetime, timedelta
from google.appengine.ext import ndb

class CalendarEntry(ndb.Model):
    day = ndb.DateProperty(indexed=False)
    active = ndb.BooleanProperty(indexed=False)
    reading = ndb.StringProperty(indexed=False)
    topic = ndb.StringProperty(indexed=False)
    
    @classmethod
    def create(cls, day=None, active=False, reading="", topic=""):
        return cls(day=day, active=active, reading=reading, topic=topic)

class Calendar(ndb.Model):
    notes = ndb.StringProperty(indexed=False, default="")
    start = ndb.DateProperty(indexed=False)
    end = ndb.DateProperty(indexed=False)
    weekly = ndb.BooleanProperty(default=True)
    weekdays = ndb.BooleanProperty(repeated=True)
    entries = ndb.StructuredProperty(CalendarEntry, repeated=True)
    final = ndb.DateProperty(indexed=False)
    final_desc = ndb.StringProperty(indexed=False, default="")

    def update(self, meetTimes=None, start=None, end=None):
        invalid = False
        
        # If meetTimes was provided, calculate a new weekday set
        if meetTimes != None:
            weekdays = [False] * 7;
            for time in meetTimes:
                weekdays[time.weekday] = True
            
            if weekdays != self.weekdays:
                self.weekdays = weekdays
                invalid = True
        
        # If start or end were provided, update them
        if start != None and start != self.start:
            self.start = start
            invalid = True
        
        if end != None and end != self.end:
            self.end = end
            invalid = True
        
        # If no final exam date is set, default to the end date
        if self.final is None:
            self.final = self.end
        
        # If the calendar has been invalidated, regenerate the dates
        if invalid:
            self.generate()
        
        # Trim any entries from end that are inactive and blank
        for entry in self.entries[::-1]:
            if (entry.active or
                    len(entry.reading) > 0 or
                    len(entry.topic) > 0):
                break
            else:
                self.entries.remove(entry)
                invalid = True
        
        return invalid

    def generate(self):
        datelist = []
        d = copy(self.start)
        td = timedelta(days=1)
        
        # Calculate all of the dates for the calendar
        while d <= self.end:
            if self.weekdays[d.weekday()]:
                datelist.append(copy(d))
            d += td
        
        # Get the length of both the current and new entry lists
        cur_len = len(self.entries)
        new_len = len(datelist)
        
        # If the current is too short, add new blank entries
        if cur_len < new_len:
            for i in range(0, new_len - cur_len):
                self.entries.append(CalendarEntry.create())
        
        # If the current is too long, mark the overflow entries as inactive
        elif cur_len > new_len:
            for i in range(0, cur_len - new_len):
                self.entries[new_len + i].active = False
        
        # Activate and set times for all entries in list
        for i in range(0, new_len):
            self.entries[i].active = True
            self.entries[i].day = datelist[i]
    
    def entries_list(self):
        out = []
        
        prev = None
        for entry in self.entries:
            # Exit the loop once inactive entries are reached
            if not entry.active:
                break

            # Check conditions to determine if a new entry should be added
            if not self.weekly or prev is None or entry.day.isocalendar()[1] != prev.day.isocalendar()[1]:
                out.append( [entry.day, entry.reading, entry.topic] )
            
            # If not adding a new entry, add to the previous entry
            else:
                if len(out[-1][1]) > 0:
                    out[-1][1] += "<br/>"
                out[-1][1] += entry.reading
                
                if len(out[-1][2]) > 0:
                    out[-1][2] += "<br/>"
                out[-1][2] += entry.topic
            
            prev = entry
        return out

    @classmethod
    def current_sem(cls):
        if datetime.now().month >= 6:
            return 'F'
        return 'S'
    
    @classmethod
    def current_year(cls):
        return datetime.now().year
    
    @classmethod
    def create(cls, term):
        return cls(start=Term.start_date(term), end=Term.end_date(term))