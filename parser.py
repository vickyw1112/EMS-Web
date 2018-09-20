'''
Part of controller
Use to define data structure used by controller to parse view/model data
for each kind of obj in model
To comply with MVC
'''
from exceptions import *
from validate_email import validate_email
from collections import namedtuple
from abc import ABC, abstractmethod
from flask_login import current_user
from datetime import datetime

ems = None
def registerEMS(ems_instance):
    global ems
    ems = ems_instance


EVENT_MODEL_ATTRS = 'title, capacity, timeStart, timeEnd, lastTimeToLeave, desc, fee, earlyBirdTime'
EVENT_VIEW_ATTRS = 'eid, title, time, duration, status, convenor, lastTimeToLeave, earlyBirdTime, availableSeats, desc, currFee, fee, type'

TIME_FORMAT = '%Y-%m-%dT%H:%M'

# Base Class
class Parser(ABC):
    '''
    Subclass shall also have:
        ViewData - namedtuple used for View
        ModelData - namedtuple used for Model
    '''

    '''
    Parse given Obj defined in Model to a ViewData
    which is a namedtuple used for View
    This defines the conversion from Model interfaces(property)
    and ViewData interfaces(property)
    '''
    @classmethod
    @abstractmethod
    def parseModelToView(cls, obj):
        pass

    '''
    Parse user input (form) into a ModelData
    which is a namedtuple used for Model
    This defines the conversion from View (form) to
    ModelData interfaces(property)
    and 
    '''
    @classmethod
    @abstractmethod
    def parseViewToModel(cls, form): 
        pass

        
class CourseData(Parser):
    ViewData = namedtuple('CourseViewData', EVENT_VIEW_ATTRS)
    ModelData = namedtuple('CourseModelData', EVENT_MODEL_ATTRS)

    @staticmethod  
    def validate(form):
        if not form.get('title'): raise CourseDataException("Invalid title", "title")
        
        if not form.get('capacity').isdigit() or \
                int(form.get('capacity')) <= 0:
            raise CourseDataException("Capacity is not valid", "capacity") 

        try:
           timeStart = datetime.strptime(form.get('timeStart'), TIME_FORMAT)
        except:
            raise CourseDataException("Invalid start time", "timeStart")
        
        try:
            timeEnd = datetime.strptime(form.get('timeEnd'), TIME_FORMAT)
        except:
            raise CourseDataException("Invalid end time", "timeEnd")

        if timeStart > timeEnd:
            raise CourseDataException("End time is before start time", "timeEnd")

            
        try:
            lastTimeToLeave = datetime.strptime(form.get('lastTimeToLeave'), TIME_FORMAT)
        except:
            raise CourseDataException("Invalid last time to leave", "lastTimeToLeave")

        try:
            earlyBirdTime = datetime.strptime(form.get('earlyBirdTime'), TIME_FORMAT)
        except:
            raise CourseDataException("Invalid early bird time", "earlyBirdTime")

        if(timeEnd < timeStart): 
            raise CourseDataException("Invalid start and end times combination", "timeEnd")
        if(lastTimeToLeave > timeEnd):
            raise CourseDataException("Last time to leave is after the course ends", "lastTimeToLeave")
        if(earlyBirdTime > timeStart):
            raise CourseDataException("Early bird time is beyond the course starting time", "earlyBirdTime")

        if not form.get('description'):
            raise CourseDataException("Description is empty", 'description')

        try:
            fee = float(form.get('fee'))
        except:
            raise CourseDataException("Invalid fee", "fee")

    @classmethod
    def parseModelToView(cls, course):
        return cls.ViewData(
            eid = course.eid,
            title = course.title,
            status = course.status.name,
            time = str(course.time),
            duration = course.time.duration,
            type = type(course).__name__,
            convenor = course.convenor,
            availableSeats = course.availableSeats,
            desc = course.description,
            fee = course.fee,
            currFee = course.currFee,
            lastTimeToLeave = course.lastTimeToLeave,
            earlyBirdTime = course.earlyBirdTime
        )

    @classmethod
    def parseViewToModel(cls, form):
        cls.validate(form)

        return cls.ModelData(
            title = form['title'],
            capacity = int(form['capacity']),
            timeStart = form['timeStart'],
            timeEnd = form['timeEnd'],
            lastTimeToLeave = form['lastTimeToLeave'],
            desc = form['description'],
            fee = float(form['fee']),
            earlyBirdTime = form['earlyBirdTime']
        )

class SeminarData(Parser):
    ViewData = namedtuple('SeminarViewData', ','.join([EVENT_VIEW_ATTRS, 'sessionCount, sessions, isCurrUserPresenter']))
    ModelData = namedtuple('SeminarModelData', ','.join([EVENT_MODEL_ATTRS, 'sessions']))
    
    @staticmethod
    def validate(form):   
        if not form.get('title'): raise SeminarDataException("Invalid title", "title")

        try:
           timeStart = datetime.strptime(form.get('timeStart'), TIME_FORMAT)
        except:
            raise SeminarDataException("Invalid start time", "timeStart")
        
        try:
            timeEnd = datetime.strptime(form.get('timeEnd'), TIME_FORMAT)
        except:
            raise SeminarDataException("Invalid end time", "timeEnd")
            
        if timeStart > timeEnd:
            raise SeminarDataException("End time is before start time", "timeEnd")

        try:
            lastTimeToLeave = datetime.strptime(form.get('lastTimeToLeave'), TIME_FORMAT)
        except:
            raise SeminarDataException("Invalid last time to leave", "lastTimeToLeave")

        try:
            earlyBirdTime = datetime.strptime(form.get('earlyBirdTime'), TIME_FORMAT)
        except:
            raise SeminarDataException("Invalid early bird time", "earlyBirdTime")

        if(timeEnd < timeStart): 
            raise SeminarDataException("Invalid start and end times combination", "timeEnd")
        if(lastTimeToLeave > timeEnd): 
            raise SeminarDataException("Last time to leave is after the seminar ends", "lastTimeToLeave")
        if(earlyBirdTime > timeStart):
            raise SeminarDataException("Early bird time is beyond the seminar starting time", "earlyBirdTime")

        desc = form.get('description')
        if(not desc):
            raise SeminarDataException("Description is empty", 'description')

        try:
            float(form.get('fee'))
        except:
            raise SeminarDataException("Invalid fee", "fee")
        
    @classmethod
    def parseModelToView(cls, seminar, **kwargs):
        return cls.ViewData(
            eid = seminar.eid,
            title = seminar.title,
            status = seminar.status.name,
            time = str(seminar.time),
            duration = seminar.time.duration,
            type = type(seminar).__name__,
            convenor = seminar.convenor,
            availableSeats = max([session.availableSeats for session in seminar.sessions]),
            desc = seminar.description,
            sessionCount = seminar.sessionCount,
            fee = seminar.fee,
            currFee = seminar.currFee,
            sessions = [session.parseToView for session in seminar.sessions],
            lastTimeToLeave = seminar.lastTimeToLeave,
            earlyBirdTime = seminar.earlyBirdTime,
            isCurrUserPresenter = seminar.hasPresenter(current_user)
        )


    @classmethod
    def parseViewToModel(cls, form):
        cls.validate(form)

        sessions = []
        for i in range(int(form['sessionCount'])):
            sessions.append(SessionData.parseViewToModel(i, form))
        return cls.ModelData(
            title = form['title'],
            capacity = None,
            timeStart = form['timeStart'],
            timeEnd = form['timeEnd'],
            lastTimeToLeave = form['lastTimeToLeave'],
            desc = form['description'],
            fee = float(form['fee']),
            earlyBirdTime = form['earlyBirdTime'],
            sessions = sessions
        )


class SessionData(Parser):
    ModelData = namedtuple('SessionModelData', 'id, title, presenter, timeStart, timeEnd, capacity, desc')
    ViewData = namedtuple('SessionViewData', 'id, title, presenter, presenter_uid, availableSeats, time, duration, desc')

    @staticmethod
    def validate(form, sessionNo):
        title = form.get('session{}_title'.format(sessionNo))
        timeStart = form.get('session{}_timeStart'.format(sessionNo))
        timeEnd = form.get('session{}_timeEnd'.format(sessionNo))
        desc = form.get('session{}_description'.format(sessionNo))
        presenter = form.get('session{}_presenter'.format(sessionNo))
        capacity = form['session{}_capacity'.format(sessionNo)]
        
        if(not title): 
            raise SessionDataException("Invalid title for session {}".format(sessionNo + 1), 
                    "session{}_title".format(sessionNo))
            
        try:
           timeStart = datetime.strptime(timeStart, TIME_FORMAT)
        except:
            raise SessionDataException("Invalid start time for session {}".format(sessionNo + 1), 
                    "session{}_timeStart".format(sessionNo))
        
        try:
            timeEnd = datetime.strptime(timeEnd, TIME_FORMAT)
        except:
            raise SessionDataException("Invalid end time for session {}".format(sessionNo + 1), 
                    "session{}_timeEnd".format(sessionNo))

        if(timeEnd < timeStart): 
            raise SessionDataException("Invalid start and end times combination for session {}".format(sessionNo + 1), 
                    "session{}_timeEnd".format(sessionNo))

        if(not desc):
            raise SessionDataException("Description is empty for session {}".format(sessionNo + 1), 
                    "session{}_description".format(sessionNo))

        if(not validate_email(presenter)): 
            raise SessionDataException("Presenter's email address is invalid for session {}".format(sessionNo + 1), 
                    "session{}_presenter".format(sessionNo))

        if(not ems.getUserByEmail(presenter)): 
            raise SessionDataException("Presenter does not exists for session {}".format(sessionNo + 1), 
                    "session{}_presenter".format(sessionNo))
                    
        if(not capacity.isdecimal() or int(capacity) <= 0):
            raise SessionDataException("Invalid capacity for session {}".format(sessionNo + 1), 
                    "session{}_capacity".format(sessionNo))

    @classmethod
    def parseModelToView(cls, session):
        return cls.ViewData(
            title = session.title,
            id = session.id,
            presenter = ems.getUserByEmail(session.presenter).name,
            presenter_uid = ems.getUserByEmail(session.presenter).uid,
            time = str(session.time),
            duration = session.time.duration,
            desc = session.description,
            availableSeats = session.availableSeats
        )

    @classmethod
    def parseViewToModel(cls, sessionNo, form):
        cls.validate(form, sessionNo)

        return cls.ModelData(
            title = form['session{}_title'.format(sessionNo)],
            id = sessionNo,
            timeStart = form['session{}_timeStart'.format(sessionNo)],
            timeEnd = form['session{}_timeEnd'.format(sessionNo)],
            desc = form['session{}_description'.format(sessionNo)],
            presenter = form['session{}_presenter'.format(sessionNo)],
            capacity = int(form['session{}_capacity'.format(sessionNo)]),
        )


class UserData(Parser):
    ViewData = namedtuple('UserViewData',
            'uid, name, email, zid, desc, notification, noNotification, seminarSessions, events, eventEids, userType, isStaff, isGuest, postedEvents')
    ModelData = namedtuple('UserModelData', 'zid, email, password, name, desc')

    @staticmethod
    def validate(form):
        
        zid = form.get('zid')
        email = form.get('email')
        password = form.get('password')
        name = form.get('name')


        #1. ZID
        if(not zid):
            # do nothing
            # as Guest user does not have a zid
            pass
        else:
            if(zid[0] != 'z' or not zid[1:].isdecimal()): 
                raise UserDataException("zID numeric is invalid", "zid")

        #2. Email
        if (not validate_email(email)): 
            raise UserDataException("Invalid email: "+email, "email")

        #3. Password
        if (not password): raise UserDataException("The password is empty!", "password")           
        
        #4. Name
        name_len = len(name)

        if(name_len == 0):
            raise UserDataException("Empty name", "name")
        elif (name_len > 80):
            raise UserDataException("Too long name", "name")

    @classmethod
    def parseModelToView(cls, user):
        return cls.ViewData(
            uid = user.uid,
            name = user.name,
            email = user.email,
            desc = user.desc,
            notification = user.notification,
            noNotification = len(user.notification),
            zid = user.zid,
            userType = type(user).__name__,
            isStaff = user.isStaff,
            isGuest = user.isGuest,
            seminarSessions = user.seminarSessions,
            events = [e.parseToView for e in user.events],
            eventEids = [e.eid for e in user.events],
            postedEvents = [e.parseToView for e in user.postedEvents] if user.isStaff else []
        )

    @classmethod
    def parseViewToModel(cls, form):
        cls.validate(form)

        return cls.ModelData(
            zid = form.get('zid'),
            email = form.get('email'),
            password = form.get('password'),
            name = form.get('name'),
            desc = form.get('description')
        )

# Mapping for obj and ViewData
Parser.ALL_DATA = {
    'Course': CourseData,
    'Seminar': SeminarData,
    'Session': SessionData,
    'User': UserData
}
