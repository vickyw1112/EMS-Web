"""
EMS related exceptions
"""


class EMSException(Exception):
    def __init__(self, msg, element):
        super().__init__(msg)
        self._element = element
    
    @property
    def fieldname(self):
        return self._element

class UserDataException(EMSException):
    pass

class PostEventException(EMSException):
    pass

class EventException(EMSException):
    def __init__(self, msg):
        Exception.__init__(self, msg)

class SessionDataException(PostEventException):
    pass

class SeminarDataException(PostEventException):
    pass

class CourseDataException(PostEventException):
    pass


