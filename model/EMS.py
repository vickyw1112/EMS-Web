import pickle
import sys
from abc import ABC, abstractmethod
from csv import DictReader
from model.user import User, Student, Staff, Guest
from model.event import Event, Course, Seminar, Session, Status
from parser import UserData, registerEMS
from exceptions import EMSException, UserDataException
from copy import copy

class EMS:
    def __init__(self, **kwargs):
        self._users = {}
        self._events = {}
        self._binFile = 'emsData.bin'
        registerEMS(self)
        if 'userCSV' in kwargs:
            print('Reading from {}...'.format(kwargs['userCSV']))
            self.loadUsers(kwargs['userCSV'])
        elif 'binFile' in kwargs:
            self.loadData(file=kwargs['binFile'])
            self._binFile = kwargs['binFile']
    
    @property
    def users(self):
        return copy(self._users)

    def addUser(self, user):
        if user.email in self._users:
            raise UserDataException('Email already exists', 'email')
        self._users[user.email] = user

    """
    load users from given format csv file
    """
    def loadUsers(self, csvPath):
        user = None
        reader = None

        # try to open given csv file
        # fail gracefully and log error
        try:
            reader = DictReader(open(csvPath, "r"))
        except OSError as err:
            print("Cannot Open {} to read: {}".format(csvPath, err), 
                    file=sys.stderr)
            exit(1)

        # instantiate corresponding User obj and add it to EMS
        for row in reader:

            row['zid'] = 'z' + row.pop('zID')

            if row['role'] == 'trainee':
                user = Student(UserData.parseViewToModel(row))
            elif row['role'] == 'trainer':
                user = Staff(UserData.parseViewToModel(row))
            elif row['role'] == 'guest':
                row['zid'] = False
                user = Guest(UserData.parseViewToModel(row))
            if user:
                self.addUser(user)
                print("[{}] {} loaded: {}".format(user.uid, type(user).__name__, user))
    
    def getUserById(self, uid):
        for user in self._users.values():
            if user.uid == uid:
                return user
        return None


    def dumpData(self, **kwargs):
        dataPath = kwargs['file'] if 'file' in kwargs else self._binFile
        try:
            pickle.dump((self._users, self._events), open(dataPath, 'wb+'))
            print('Dumped into file:\n{}'.format(dataPath))
        except OSError as err:
            print('Error when dumping into file:\n{}\n{}'.format(dataPath, err), 
                    file=sys.stderr)
    
    def loadData(self, **kwargs):
        dataPath = kwargs['file'] if 'file' in kwargs else self._binFile
        try:
            self._users, self._events = pickle.load(open(dataPath, 'rb'))
            # update Event static var __eid
            # and User static var __uid
            Event.setEid(self.maxEid)
            User.setUid(self.maxUid)
        except OSError as err:
            print('Error when loading file:\n{}\n{}'.format(dataPath, err), file=sys.stderr)

    def addEvent(self, event):
        self._events[event.eid] = event

    def getUserByEmail(self, email):
        if not email in self._users:
            return None
        return self._users[email]
    
    def getEventById(self, eid):
        if not eid in self._events:
            return None
        return self._events[eid]

    """
    Given a category name which is the class name
    i.e. "Seminar" or "Course" or "All"
    Returns the list of open events in that category
    """
    def getOpenEventsByCategory(self, category):
        # capitalise first char of category
        category = category[:1].capitalize() + category[1:]

        if category not in Event.ALL_CATEGORY and category != 'All':
            raise EMSException('Undefined Category', 'category')

        return [e for e in self._events.values() 
                if e.status == Status.OPEN and 
                (e.category == category or category == 'All')]

    """
    validate if zid/password combination is correct

    return a tuple (user, message)
    where user is a object of User if login success, otherwise None
    message is to be displayed
    """
    def login(self, zid, passwd):
        user = self.getUserByEmail(zid)
        if not user:
            return (None, 'User does not exist!')
        if user.password != passwd:
            return (None, 'Wrong password!')
        return (user, 'Successfully logged in...')
		
    @property
    def maxEid(self):
        return max([e.eid for e in self._events.values()], default=-1)

    @property
    def maxUid(self):
        return max([u.uid for u in self._users.values()], default=-1)
