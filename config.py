import os
from datetime import timedelta

class Production(object):
    DEBUG = False
    SERVER_NAME = 'sample.com:80'
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)

    def __init__(self):
        self.SECRET_KEY = os.environ['SECRET_KEY']

class Development(object):
    DEBUG = True
    SECRET_KEY = 'VERY VERY SECURE KEY'
    PERMANENT_SESSION_LIFETIME = timedelta(days=365)

config = Development()