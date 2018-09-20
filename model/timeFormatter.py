from datetime import datetime
from abc import ABC, abstractmethod

class TimeFormatter(ABC):

    @abstractmethod
    def formatDuration(timedelta):
        pass

    # should produce a UTC datetime str easy for javascript
    # to parse into local timezone
    @abstractmethod
    def format(time):
        pass

# formatter for event last for days
# for Seminar
class DayFormatter(TimeFormatter):
    """
    e.g. 5 days
    """
    def formatDuration(timedelta):
        # round up to days inclusive of start and end
        days = timedelta.days
        if timedelta.seconds > 0:
            days += 1
        return str(days) + ' Day' + ('s' if days > 1 else '')

    """
    e.g. 12/04 to 15/04
    12/31/18 to 03/01/19
    """
    def format(time):
        # if same year and is in current year, does not bother to display year
        formatStr = '%d/%m' \
                if datetime.utcnow().year == time.end.year and \
                time.start.year == time.end.year \
                else '%d/%m/%Y' 
        dateStr = time.start.strftime(formatStr)
        dateStr += ' to '
        dateStr += time.end.strftime(formatStr)
        return dateStr

# formatter for event/session within a day
# for course and Seminar sessions
class HourFormatter(TimeFormatter):
    def formatDuration(timedelta):
        hours = int(timedelta.seconds / 3600)
        minutes = int((timedelta.seconds % 3600) / 60)
        returnStr = str(hours) + ' Hour' + ('s' if hours > 1 else '') 
        if minutes:
            returnStr += ' ' + str(minutes) + ' Minute' + ('s' if minutes > 1 else '')
        return returnStr

    """
    e.g. 12/04/18 12:00 to 15:00
    """
    def format(time):
        formatStr = '%d/%m/%Y %H:%M' \
                if datetime.utcnow().year != time.end.year \
                else '%d/%m %H:%M'
        returnStr = time.start.strftime(formatStr)
        returnStr += ' to '
        returnStr += time.end.strftime('%H:%M')
        return returnStr
