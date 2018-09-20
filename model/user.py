from abc import ABC, abstractmethod
from flask_login import UserMixin
from model.event import Event, Status
from parser import UserData
from exceptions import EventException
from copy import copy


# inherit UserMixin let User class works with flask_login
# without defining is_authenticated .... ourself
class User(ABC, UserMixin):
    __uid = -1
    def __init__(self, userData):
        self._uid = User._genUid()
        self._zid = userData.zid
        self._password = userData.password
        self._name = userData.name
        self._email = userData.email
        self._desc = userData.desc
        self._events = []
        self._notification = []
        self._cancelled = []
        # to track which session the user registered for
        # for a seminar
        # key is eid, value is list of session ids
        self._seminarSessions = {}


    @classmethod
    def setUid(cls, uid):
        cls.__uid = uid

    @staticmethod
    def _genUid():
        User.__uid += 1
        return User.__uid
    
    @property
    def uid(self):
        return self._uid

    @property
    def name(self):
        return self._name

    @property
    def desc(self):
        return self._desc

    @property
    def notification(self):
        return self._notification[:]

    def addNotification(self, msg):
        self._notification.append(msg)

    def clearNotification(self):
        self._notification = []

    @property
    def parseToView(self):
        return UserData.parseModelToView(self)

    @property
    def zid(self):
        return self._zid
    
    @property
    def email(self):
        return self._email

    @property
    def password(self):
        return self._password

    @property
    def events(self):
        return self._events[:]

    @property
    def cancelled(self):
        return self._cancelled[:]

    @property
    def isGuest(self):
        return False

    @property
    def isStaff(self):
        return False

    @property
    def seminarSessions(self):
        # shadow copy
        return copy(self._seminarSessions)

    def addSeminarSessions(self, eid, sessions):
        self._seminarSessions[eid] = sessions

    def removeSeminarSessions(self, eid):
        del self._seminarSessions[eid]
    
    def addToEvents(self, event):
        self._events.append(event)

    def removeEvent(self, event):
        self._events.remove(event)

    def get_id(self):
        return self._email

    # pretty print user
    def __str__(self):
        return "{}<{}>".format(self._name, self._email)

class Guest(User):
    @property
    def isGuest(self):
        return True


class Student(User):
    pass

class Staff(User):
    def __init__(self, userData):
        super().__init__(userData)
        self._postedEvents = []

    @property
    def postedEvents(self):
        return self._postedEvents[:]
    
    @property
    def isStaff(self):
        return True

    '''
    Post new event
    return eid
    '''
    def postEvent(self, ems, classname, eventModelData):
        newEvent = Event.ALL_CATEGORY[classname](self._name, eventModelData, ems=ems)
        ems.addEvent(newEvent)  
        self._postedEvents.append(newEvent)
        return newEvent.eid

    def canJoinEvent(self, event):
         return super().canJoinEvent(event) and not event in self._postedEvents

    '''
    Change the status of a event
    '''
    def changeEventStatus(self, event, status):
        if event.status == status:
            raise EventException('This event is already in status {}'.format(status.name))
        event.status = status
