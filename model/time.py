from datetime import datetime

class Time:
    """
    parse start/end str into datetime object
    all datetime in UTC
    'Jun 1 2005 1:33PM'
    also store a instantiated object of given TimeFormatter class
    """
    def __init__(self, start, end, formatter):
        self._start = datetime.strptime(start, '%Y-%m-%dT%H:%M')
        self._end = datetime.strptime(end, '%Y-%m-%dT%H:%M')
        self._duration = self._end - self._start
        self._formatter = formatter

    """
    format the duration into a sensible string
    """
    @property
    def duration(self):
        return self._formatter.formatDuration(self._duration)

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end


    """
    format start/end time
    """
    def __str__(self):
        return self._formatter.format(self)

