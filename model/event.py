from enum import Enum, unique
from datetime import datetime
from abc import ABC, abstractmethod
from parser import Parser
from model.time import Time
from model.timeFormatter import DayFormatter, HourFormatter
from exceptions import EventException


# Common attributes/methods of event-like classes
# i.e. Course/Seminar/Session
class EventMixin:
    def __init__(self, ModelData):
        self._title = ModelData.title
        startTime = ModelData.timeStart
        endTime = ModelData.timeEnd
        formatter = Event.FORMATTER_MAP.get(type(self).__name__, HourFormatter)
        self._time = Time(startTime, endTime, formatter)
        self._capacity = ModelData.capacity
        self._description = ModelData.desc
        self._attendeeCount = 0

    @property
    def title(self):
        return self._title

    @property
    def time(self):
        return self._time

    @property
    def description(self):
        return self._description

    @property
    def capacity(self):
        return self._capacity

    @property
    def availableSeats(self):
        return self._capacity - self._attendeeCount if self._capacity else None

    def changeAttendeeCount(self, delta):
        self._attendeeCount += delta

    @property
    def parseToView(self):
        try:
            return Parser.ALL_DATA[type(self).__name__].parseModelToView(self)
        except KeyError:
            raise NotImplementedError(
                "{} class has no corresponding ViewData".format(type(self).__name__))

    @property
    def isFull(self):
        return (self._attendeeCount >= self._capacity) if self._capacity else False


class Event(ABC, EventMixin):
    # static auto increment var
    __eid = -1

    def __init__(self, convenor, EventModelData, **kwargs):
        EventMixin.__init__(self, EventModelData)
        self._eid = Event._genEid()
        # use hour formatter if formatter map is not defined for current category
        lastTimeToLeave = EventModelData.lastTimeToLeave
        earlyBirdTime = EventModelData.earlyBirdTime
        self._lastTimeToLeave = datetime.strptime(lastTimeToLeave, '%Y-%m-%dT%H:%M')
        self._earlyBirdTime = datetime.strptime(earlyBirdTime, '%Y-%m-%dT%H:%M')
        self._status = Status.OPEN
        self._fee = EventModelData.fee
        self._convenor = convenor


    @classmethod
    def setEid(cls, eid):
        cls.__eid = eid

    @staticmethod
    def _genEid():
        Event.__eid += 1
        return Event.__eid

    @property
    def category(self):
        return type(self).__name__
    
    @property
    def eid(self):
        return self._eid

    @property
    def fee(self):
        return self._fee
    
    @property
    def convenor(self):
        return self._convenor
    
    @property
    def lastTimeToLeave(self):
        return self._lastTimeToLeave    

    @property
    def earlyBirdTime(self):
        return self._earlyBirdTime

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        if not status in Status:
            raise EventException('Invalid Status')
        self._status = status

    @property
    def currFee(self):
        return 0.5 * self._fee if datetime.now() < self._earlyBirdTime \
                else self._fee
        
    @property
    def joinable(self):
        return not self.isFull and self.status == Status.OPEN

    @abstractmethod
    def enrolUser(self, user, sessions=[]):
        pass

    @abstractmethod
    def unenrolUser(self, user):
        pass


    def hasPresenter(self, user):
        return False 

    def joinCheck(self, user):
        eventType = self.category.lower()
        if self in user.events:
            raise EventException("You have joined this {}".format(eventType))
        if not self.joinable:
            raise EventException("This {} is full or closed".format(eventType))
        if user.isStaff and self in user.postedEvents:
            raise EventException("You cannot join event that you posted")

    def leaveCheck(self, user):
        eventType = type(self).__name__.lower()
        if not self in user.events:
            raise EventException('You are not in this event!'.format(eventType))
        if datetime.now() > self.lastTimeToLeave:
            raise EventException('You cannot leave this event after: {}'.format(self.lastTimeToLeave))

    def changeStatusCheck(self, user):
        if not user.isStaff:
            abort(401)
        if not self in user._postedEvents:
            raise EventException('You can only change the status of event that you posted')

class Course(Event):
    def enrolUser(self, user, **form):
        self.joinCheck(user)

        user.addToEvents(self)
        self.changeAttendeeCount(1)

    def unenrolUser(self, user):
        self.leaveCheck(user)
        user.removeEvent(self)
        self.changeAttendeeCount(-1)

class Seminar(Event):
    def __init__(self, convenor, seminarModelData, **kwargs):
        super().__init__(convenor, seminarModelData)
        self._sessions = {session.id : Session(session) for session in seminarModelData.sessions}

        # for a non-duplicated set of all presenter of the seminar
        for presenter in set(s.presenter for s in seminarModelData.sessions):
            # enrol the presenter to all his participated sessions
            sessionIDs = [s.id for s in seminarModelData.sessions if s.presenter == presenter]
            self.enrolUser(kwargs.get('ems').getUserByEmail(presenter), sessionIDs=sessionIDs, presenter=True)
        
    @property
    def sessions(self):
        return self._sessions.values()

    @property
    def sessionCount(self):
        return len(self._sessions)

    def hasPresenter(self, user):
        return user.email in [session.presenter for session in self._sessions.values()]

    def enrolUser(self, user, **kwargs):
        self.joinCheck(user)

        sessionIDs = [int(sessionID) for sessionID in kwargs['form'].getlist('sessionSel')] \
                        if kwargs.get('form') else kwargs.get('sessionIDs')
        if not sessionIDs:
            raise EventException("You have to register for at least one session for a seminar")
        if any([self._sessions[sessionID].isFull for sessionID in sessionIDs]):
            raise EventException("One or more of the session you select is full")

        user.addToEvents(self)
        user.addSeminarSessions(self._eid, sessionIDs)
        if not kwargs.get('presenter', False):
            for session in [self._sessions[sessionID] for sessionID in sessionIDs]:
                session.changeAttendeeCount(1)

    def leaveCheck(self, user):
        super().leaveCheck(user)
        if self.hasPresenter(user):
            raise EventException('You cannot leave this seminar as you are presenting')

    def unenrolUser(self, user):
        self.leaveCheck(user)
        user.removeEvent(self)
        for sessionID in user.seminarSessions[self._eid]:
            self._sessions[sessionID].changeAttendeeCount(-1)
        user.removeSeminarSessions(self._eid)

class Session(EventMixin):
    def __init__(self, SessionModelData):
        EventMixin.__init__(self, SessionModelData)
        self._presenter = SessionModelData.presenter
        self._id = SessionModelData.id
    
    @property
    def id(self):
        return self._id

    @property
    def presenter(self):
        return self._presenter

@unique
class Status(Enum):
    OPEN = 1
    CLOSE = 2
    CANCEL = 3

# define the change status button style
Status.COLOR_MAP = {
    'OPEN': 'success',
    'CLOSE': 'danger',
    'CANCEL': 'dark' 
}

# dict of all category of Event
Event.ALL_CATEGORY = {event.__name__: event for event in Event.__subclasses__()}

# mapping for event front end color
Event.COLOR_MAP = {
        'Course' : 'info',
        'Seminar' : 'secondary'
    }

# define which formatter to use for each subclass of Event
Event.FORMATTER_MAP = {
    'Seminar': DayFormatter,
    'Course': HourFormatter,
    'Session': HourFormatter
}
