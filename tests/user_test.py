import pytest
import os
from model.user import Guest
from model.EMS import EMS
from parser import UserData, registerEMS
from exceptions import *

def test_guest_registration_success():
    ems1 = EMS()
    user1 = Guest(createUser(None, 'hahaha', 'testName23', 'z5135009@unsw.net'))
    ems1.addUser(user1)
    assert(ems1.getUserByEmail('z5135009@unsw.net').name == 'testName23')
    registerEMS(None)

def test_guest_registration_empty_name():
    with pytest.raises(UserDataException) as exc_info:
        user1 = Guest(createUser(None, 'hahaha', '', 'z5135009@unsw.net'))
    assert(exc_info.type == UserDataException)
    assert(exc_info.value.fieldname == 'name')
    assert(str(exc_info.value) == 'Empty name')

def test_guest_registration_long_name():
    with pytest.raises(UserDataException) as exc_info:
        user1 = Guest(createUser(None, 'hahaha', 'LONG_NAME' * 50, 'z5135009@unsw.net'))
    assert(exc_info.type == UserDataException)
    assert(exc_info.value.fieldname == 'name')
    assert(str(exc_info.value) == 'Too long name')


def test_guest_registration_invalid_email():
    with pytest.raises(UserDataException) as exc_info:
        user1 = Guest(createUser(None, 'hahaha', 'hahah', 'z5135009unsw.net'))
    assert(exc_info.type == UserDataException)
    assert(exc_info.value.fieldname == 'email')
    assert(str(exc_info.value) == 'Invalid email: z5135009unsw.net')

def test_guest_registration_empty_email():
    with pytest.raises(UserDataException) as exc_info:
        user1 = Guest(createUser(None, 'hahaha', 'hahah', ''))
    assert(exc_info.type == UserDataException)
    assert(exc_info.value.fieldname == 'email')
    assert(str(exc_info.value) == 'Invalid email: ')

def test_guest_registration_empty_pwd():
    with pytest.raises(UserDataException) as exc_info:
        user1 = Guest(createUser(None, '', 'name23', 'z5135009@unsw.net'))
    assert(exc_info.type == UserDataException)
    assert(exc_info.value.fieldname == 'password')
    assert(exc_info.value.fieldname == 'password')

def test_guest_registration_email_exist():
    ems1 = EMS()
    user1 = Guest(createUser(None, 'hahaha1', 'hahah', 'z5135009@unse.net'))
    ems1.addUser(user1)
    with pytest.raises(UserDataException) as exc_info:
        user2 = Guest(createUser(None, 'hahaha', 'hahah', 'z5135009@unse.net'))
        ems1.addUser(user2)
    assert(exc_info.type == UserDataException)
    assert(exc_info.value.fieldname == 'email')
    assert(str(exc_info.value) == 'Email already exists')
    registerEMS(None)






# test load and dump 
# load data which from ems1 in ems2 
# check name
def test_dumpAndLoad1():
    ems1 = EMS(userCSV = 'user.csv')
    user1 = Guest(createUser('z5135009', 'hahaha', 'name5135009', 'z5135009@unsw.net'))
    ems1.addUser(user1)
    ems1.dumpData(file='user.data')
    ems2 = EMS(binFile = 'user.data')
    
    assert(ems2.getUserByEmail('z5135009@unsw.net').name == 'name5135009')
    assert(ems2.getUserByEmail('z6119994@unsw.net').name == 'name6119994')
    registerEMS(None)


# test load and dump 
# load data which from ems1 in ems2 
# test property for user --- password
def test_dumpAndLoad2():
    ems1 = EMS(userCSV = 'user.csv')
    user1 = Guest(createUser('z5135009', 'hahaha', 'name5135009', 'z5135009@unsw.net'))
    ems1.addUser(user1)
    ems1.dumpData(file='user.data')
    ems2 = EMS(binFile = 'user.data')
    
    assert(ems2.getUserByEmail('z5135009@unsw.net').password == 'hahaha')
    assert(ems2.getUserByEmail('z6119994@unsw.net').password == 'pass24064')
    registerEMS(None)


# test load and dump 
# load data which from ems1 in ems2 
# test property for user --- email
def test_dumpAndLoad3():
    ems1 = EMS(userCSV = 'user.csv')
    user1 = Guest(createUser('z5135009', 'hahaha', 'name5135009', 'z5135009@unsw.net'))
    ems1.addUser(user1)
    ems1.dumpData(file='test-user.data')
    ems2 = EMS(binFile = 'test-user.data')
    os.remove('test-user.data')
    assert(ems2.getUserByEmail('z5135009@unsw.net').email == 'z5135009@unsw.net')
    assert(ems2.getUserByEmail('z6119994@unsw.net').email == 'z6119994@unsw.net')
    registerEMS(None)

    
# test login 
# if user is not exist
def test_login1():
    ems1 = EMS(userCSV = 'user.csv')
    assert(ems1.login('z5135009@unsw.net', 'hahaha') == (None, 'User does not exist!')) 
    registerEMS(None)

# test login 
# if pwd is not right
def test_login2():
    ems1 = EMS(userCSV = 'user.csv')
    assert(ems1.login('z4119999@unsw.net', 'hahaha') == (None, 'Wrong password!'))
    registerEMS(None)

# test login 
# if name and pwd is right
def test_login3():
    ems1 = EMS(userCSV = 'user.csv')
    assert(ems1.login('z4119999@unsw.net', 'pass30778') == 
            (ems1.getUserByEmail('z4119999@unsw.net'), 'Successfully logged in...'))
    registerEMS(None)

# test login 
# if pwd is not right
def test_login4():
    ems1 = EMS(userCSV = 'user.csv')
    assert(ems1.login('z4119999@unsw.net', 'pass27204') == (None, 'Wrong password!'))

def createUser(zidC, passwordC, nameC, emailC):
    buf =  {
        "zid": zidC,
        "password": passwordC,
        "name": nameC,
        "email": emailC
       }
    return UserData.parseViewToModel(buf)
