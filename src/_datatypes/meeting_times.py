from datatypes import WEEKDAY_CHARS
from datetime import datetime, timedelta
from google.appengine.ext import ndb

class MeetingTime(ndb.Model):    
    weekday = ndb.IntegerProperty()
    startMins = ndb.IntegerProperty()
    durMins = ndb.IntegerProperty()
    
    def get_start_hour(self):
        return int(self.startMins / 60)
    
    def get_start_hour_12h(self):
        hour = self.get_start_hour()
        if hour == 0:
            return 12
        if hour > 12:
            return hour - 12
        return hour
        
    def get_start_pm(self):
        return self.get_start_hour() >= 12
    
    def get_start_min(self):
        return int(self.startMins % 60)
    
    def set_start(self, hour, mins):
        self.startMins = 60 * hour + mins
        
    def set_start_12h(self, hour, mins, pm):
        if not pm and hour == 12:
            hour = 0
        elif pm and hour < 12:
            hour += 12
        self.set_start(hour, mins)
    
    def get_dur_hour(self):
        return int(self.durMins / 60 % 24)
    
    def get_dur_min(self):
        return int(self.durMins % 60)
    
    def set_dur(self, hour, mins):
        self.durMins = 60 * hour + mins
    
    def get_start_string(self):
        return MeetingTime.get_time_string(self.startMins)
    
    def get_end_string(self):
        return MeetingTime.get_time_string(self.startMins + self.durMins)
    
    def __eq__(self, other):
        return not other is None and self.weekday == other.weekday and self.startMins == other.startMins and self.durMins == other.durMins
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    @classmethod
    def create(cls, weekday=0, startMins=0, durMins=0):
        return cls(weekday=weekday, startMins=startMins, durMins=durMins)
    
    @classmethod
    def get_time_string(cls, mins, show_am_pm = True):
        mins = mins % (24 * 60) # loop over into next day
        hours = int(mins / 60)
        mins = mins % 60
        
        pm = hours >= 12
        
        if hours > 12:
            hours -= 12
        elif hours == 0:
            hours = 12
        
        if show_am_pm:
            return "{}:{:02d} {}".format(hours, mins, "PM" if pm else "AM")
        else:
            return "{}:{:02d}".format(hours, mins)
    
    @classmethod
    def parse_strings(cls, day_str, time_str):
        meeting_times = []
        time_split = time_str.split(", ")
        for split in time_split:
            split2 = split.split("-")
            try:
                start = datetime.strptime(split2[0], "%H:%M %p")
                end = datetime.strptime(split2[1], "%H:%M %p")
                duration = int((end - start).total_seconds() / 60)
                if duration < 0:
                    duration += 3600
                
                for char in day_str:
                    for i in range(len(WEEKDAY_CHARS)):
                        if char == WEEKDAY_CHARS[i]:
                            startMins = 60 * start.hour + start.minute
                            meeting_time = MeetingTime.create(i, startMins, duration)
                            meeting_times.append(meeting_time)
            except (KeyError, ValueError):
                print "Error reading time: " + split
        return meeting_times

    @classmethod
    def build_string(cls, time_list, show_am_pm=False):
        out_list = []
        for time in time_list:
            for tup in out_list:
                if time.startMins == tup[7].startMins and time.durMins == tup[7].durMins:
                    tup[time.weekday] = True
                    break
            else:
                tup = [False]*7
                tup.append(time)
                tup[time.weekday] = True
                out_list.append( tup )

        strout = ""
        for time in out_list:
            if len(strout) != 0:
                strout += " "
            for i in range(7):
                if time[i]:
                    strout += WEEKDAY_CHARS[i]
            strout += " "
            strout += MeetingTime.get_time_string(time[7].startMins, show_am_pm)
            strout += "-"
            strout += MeetingTime.get_time_string(time[7].startMins + time[7].durMins, show_am_pm)

        return strout
