import pytest
from model.event import Event, Seminar, Course, Status
from model.EMS import EMS
from model.user import Staff, Guest
from parser import UserData, SeminarData, SessionData, registerEMS
from exceptions import *


# setup
@pytest.fixture
def ems():
    ems1 = EMS()
    staff = Staff(createUser('z5135009', 'hahaha', 'name5135009', 'z5135007@unsw.net'))
    presenter = Guest(createUser(None, 'samplepass', 'Vicky', 'z5135008@unsw.net'))
    ems1.addUser(staff)
    ems1.addUser(presenter)
    return ems1


# copy-paste from user_test.py
def createUser(zidC, passwordC, nameC, emailC):
    buf =  {
        "zid": zidC,
        "password": passwordC,
        "name": nameC,
        "email": emailC
       }
    return UserData.parseViewToModel(buf)

def createSession(i, title, timeStart, timeEnd, desc, presenter, capacity):
    form = {
        ('session{}_title'.format(i)):title,
        ('session{}_timeStart'.format(i)):timeStart,
        ('session{}_timeEnd'.format(i)):timeEnd,
        ('session{}_description'.format(i)):desc,
        ('session{}_presenter'.format(i)):presenter,
        ('session{}_capacity'.format(i)):capacity
        }
    return form

def createSeminar(title, timeStart, timeEnd, lastTimeToLeave,
                        desc, fee, earlyBirdTime, sessions, sessionCount):
    buf = {
        'title':title,
        'timeStart':timeStart,
        'timeEnd':timeEnd,
        'lastTimeToLeave':lastTimeToLeave, 
        'description':desc,
        'fee':fee,
        'earlyBirdTime': earlyBirdTime,
        **sessions,
        'sessionCount': sessionCount
    }

    return SeminarData.parseViewToModel(buf)

def test_post_seminar_success(ems):
    session1 = createSession(0, 'testSession1', '2005-06-01T13:33', '2005-06-02T13:33', 'This is a testSession', 'z5135008@unsw.net','4')
    session2 = createSession(1, 'testSession2', '2005-06-01T13:33', '2005-06-03T13:33', 'This is a testSession', 'z5135007@unsw.net','2')

    test_seminar = createSeminar(
                "TestEvent",
                '2018-06-01T13:33', 
                '2018-06-04T13:33',
                '2018-06-01T10:33',
                "This is a test event",
                "40",
                '2018-04-01T10:33',
                {**session1, **session2},
                '2'
           )
    staff = ems.getUserByEmail('z5135007@unsw.net')
    staff.postEvent(ems, 'Seminar', test_seminar)
    # registerEMS(None)

def test_post_seminar_empty_seminar_titile():
    session1 = createSession(0, 'testSession1', '2005-06-01T13:33', '2005-06-02T13:33', 'This is a testSession', 'z5135008@unsw.net','4')
    session2 = createSession(1, 'testSession2', '2005-06-01T13:33', '2005-06-03T13:33', 'This is a testSession', 'z5135007@unsw.net','2')

    with pytest.raises(SeminarDataException) as exe_info:
        test_seminar = createSeminar(
                    "",
                    '2018-06-01T13:33', 
                    '2018-06-04T13:33',
                    '2018-06-01T10:33',
                    "This is a test event",
                    "40",
                    '2018-04-01T10:33',
                    {**session1, **session2},
                    '2'
            )
    assert(exe_info.type == SeminarDataException)
    assert(exe_info.value.fieldname == "title")


def test_post_seminar_invalid_seminar_startTime():
    session1 = createSession(0, 'testSession1', '2005-06-01T13:33', '2005-06-02T13:33', 'This is a testSession', 'z5135008@unsw.net','4')
    session2 = createSession(1, 'testSession2', '2005-06-01T13:33', '2005-06-03T13:33', 'This is a testSession', 'z5135007@unsw.net','2')

    with pytest.raises(SeminarDataException) as exe_info:
        test_seminar = createSeminar(
                    "testSeminar",
                    '2018-06-013:33', 
                    '2018-06-04T13:33',
                    '2018-06-01T10:33',
                    "This is a test event",
                    "40",
                    '2018-04-01T10:33',
                    {**session1, **session2},
                    '2'
            )
    assert(exe_info.type == SeminarDataException)
    assert(exe_info.value.fieldname == 'timeStart')

def test_post_seminar_invalid_seminar_endTime():
    session1 = createSession(0, 'testSession1', '2005-06-01T13:33', '2005-06-02T13:33', 'This is a testSession', 'z5135008@unsw.net','4')
    session2 = createSession(1, 'testSession2', '2005-06-01T13:33', '2005-06-03T13:33', 'This is a testSession', 'z5135007@unsw.net','2')

    with pytest.raises(SeminarDataException) as exe_info:
        test_seminar = createSeminar(
                    "test",
                    '2018-06-01T13:33', 
                    '2018-06-013:33',
                    '2018-06-01T10:33',
                    "This is a test event",
                    "40",
                    '2018-04-01T10:33',
                    {**session1, **session2},
                    '2'
            )
    assert(exe_info.type == SeminarDataException)
    assert(exe_info.value.fieldname == "timeEnd")

def test_post_seminar_invalid_seminar_lastTime():
    session1 = createSession(0, 'testSession1', '2005-06-01T13:33', '2005-06-02T13:33', 'This is a testSession', 'z5135008@unsw.net','4')
    session2 = createSession(1, 'testSession2', '2005-06-01T13:33', '2005-06-03T13:33', 'This is a testSession', 'z5135007@unsw.net','2')

    with pytest.raises(SeminarDataException) as exe_info:
        test_seminar = createSeminar(
                    "test",
                    '2018-06-01T13:33', 
                    '2018-06-04T13:33',
                    '2018-06-00:33',
                    "This is a test event",
                    "40",
                    '2018-04-01T10:33',
                    {**session1, **session2},
                    '2'
            )
    assert(exe_info.type == SeminarDataException)
    assert(exe_info.value.fieldname == "lastTimeToLeave")

def test_post_seminar_invalid_seminar_early():
    session1 = createSession(0, 'testSession1', '2005-06-01T13:33', '2005-06-02T13:33', 'This is a testSession', 'z5135008@unsw.net','4')
    session2 = createSession(1, 'testSession2', '2005-06-01T13:33', '2005-06-03T13:33', 'This is a testSession', 'z5135007@unsw.net','2')

    with pytest.raises(SeminarDataException) as exe_info:
        test_seminar = createSeminar(
                    "test",
                    '2018-06-01T13:33', 
                    '2018-06-04T13:33',
                    '2018-06-01T10:33',
                    "This is a test event",
                    "40",
                    '2018-04-010:33',
                    {**session1, **session2},
                    '2'
            )
    assert(exe_info.type == SeminarDataException)
    assert(exe_info.value.fieldname == "earlyBirdTime")

def test_post_seminar_invalid_seminar_timeCom1():
    session1 = createSession(0, 'testSession1', '2005-06-01T13:33', '2005-06-02T13:33', 'This is a testSession', 'z5135008@unsw.net','4')
    session2 = createSession(1, 'testSession2', '2005-06-01T13:33', '2005-06-03T13:33', 'This is a testSession', 'z5135007@unsw.net','2')

    with pytest.raises(SeminarDataException) as exe_info:
        test_seminar = createSeminar(
                    "test",
                    '2018-06-05T13:33', 
                    '2018-06-04T13:33',
                    '2018-06-01T10:33',
                    "This is a test event",
                    "40",
                    '2018-04-01T10:33',
                    {**session1, **session2},
                    '2'
            )
    assert(exe_info.type == SeminarDataException)
    assert(exe_info.value.fieldname == "timeEnd")

def test_post_seminar_invalid_seminar_timeCom2():
    session1 = createSession(0, 'testSession1', '2005-06-01T13:33', '2005-06-02T13:33', 'This is a testSession', 'z5135008@unsw.net','4')
    session2 = createSession(1, 'testSession2', '2005-06-01T13:33', '2005-06-03T13:33', 'This is a testSession', 'z5135007@unsw.net','2')

    with pytest.raises(SeminarDataException) as exe_info:
        test_seminar = createSeminar(
                    "test",
                    '2018-06-01T13:33', 
                    '2018-06-04T13:33',
                    '2018-06-05T10:33',
                    "This is a test event",
                    "40",
                    '2018-04-01T10:33',
                    {**session1, **session2},
                    '2'
            )
    assert(exe_info.type == SeminarDataException)
    assert(exe_info.value.fieldname == "lastTimeToLeave")

    
def test_post_seminar_invalid_seminar_timeCom3():
    session1 = createSession(0, 'testSession1', '2005-06-01T13:33', '2005-06-02T13:33', 'This is a testSession', 'z5135008@unsw.net','4')
    session2 = createSession(1, 'testSession2', '2005-06-01T13:33', '2005-06-03T13:33', 'This is a testSession', 'z5135007@unsw.net','2')

    with pytest.raises(SeminarDataException) as exe_info:
        test_seminar = createSeminar(
                    "test",
                    '2018-06-01T13:33', 
                    '2018-06-04T13:33',
                    '2018-06-01T10:33',
                    "This is a test event",
                    "40",
                    '2018-07-01T10:33',
                    {**session1, **session2},
                    '2'
            )
    assert(exe_info.type == SeminarDataException)
    assert(exe_info.value.fieldname == "earlyBirdTime")
             
def test_post_seminar_invalid_seminar_fee():
    session1 = createSession(0, 'testSession1', '2005-06-01T13:33', '2005-06-02T13:33', 'This is a testSession', 'z5135008@unsw.net','4')
    session2 = createSession(1, 'testSession2', '2005-06-01T13:33', '2005-06-03T13:33', 'This is a testSession', 'z5135007@unsw.net','2')
    with pytest.raises(SeminarDataException) as exe_info:
        test_seminar = createSeminar(
                    "test",
                    '2018-06-01T13:33', 
                    '2018-06-04T13:33',
                    '2018-06-01T10:33',
                    "This is a test event",
                    "",
                    '2018-04-01T10:33',
                    {**session1, **session2},
                    '2'
            )
    assert(exe_info.type == SeminarDataException)
    assert(exe_info.value.fieldname == "fee")

def test_post_seminar_invalid_seminar_desc():
    session1 = createSession(0, 'testSession1', '2005-06-01T13:33', '2005-06-02T13:33', 'This is a testSession', 'z5135008@unsw.net','4')
    session2 = createSession(1, 'testSession2', '2005-06-01T13:33', '2005-06-03T13:33', 'This is a testSession', 'z5135007@unsw.net','2')
    with pytest.raises(SeminarDataException) as exe_info:
        test_seminar = createSeminar(
                    "test",
                    '2018-06-01T13:33', 
                    '2018-06-04T13:33',
                    '2018-06-01T10:33',
                    "",
                    "40",
                    '2018-04-01T10:33',
                    {**session1, **session2},
                    '2'
            )
    assert(exe_info.type == SeminarDataException)
    assert(exe_info.value.fieldname == "description")

def test_post_seminar_invalid_ssession_title():
    session1 = createSession(0, '', '2005-06-01T13:33', '2005-06-02T13:33', 'This is a testSession', 'z5135008@unsw.net','4')
    session2 = createSession(1, 'testSession2', '2005-06-01T13:33', '2005-06-03T13:33', 'This is a testSession', 'z5135007@unsw.net','2')
    with pytest.raises(SessionDataException) as exe_info:
        test_seminar = createSeminar(
                    "test",
                    '2018-06-01T13:33', 
                    '2018-06-04T13:33',
                    '2018-06-01T10:33',
                    "This is a test event",
                    "40",
                    '2018-04-01T10:33',
                    {**session1, **session2},
                    '2'
            )
    assert(exe_info.type == SessionDataException)
    assert(exe_info.value.fieldname == 'session0_title')

def test_post_seminar_invalid_ssession_timeStart():
    session1 = createSession(0, 'test', '2005-06-13:33', '2005-06-02T13:33', 'This is a testSession', 'z5135008@unsw.net','4')
    session2 = createSession(1, 'testSession2', '2005-06-01T13:33', '2005-06-03T13:33', 'This is a testSession', 'z5135007@unsw.net','2')
    with pytest.raises(SessionDataException) as exe_info:
        test_seminar = createSeminar(
                    "test",
                    '2018-06-01T13:33', 
                    '2018-06-04T13:33',
                    '2018-06-01T10:33',
                    "This is a test event",
                    "40",
                    '2018-04-01T10:33',
                    {**session1, **session2},
                    '2'
            )
    assert(exe_info.type == SessionDataException)
    assert(exe_info.value.fieldname == 'session0_timeStart')

def test_post_seminar_invalid_ssession_endTime():
    session1 = createSession(0, 'test', '2005-06-01T13:33', '2005-06-02:33', 'This is a testSession', 'z5135008@unsw.net','4')
    session2 = createSession(1, 'testSession2', '2005-06-01T13:33', '2005-06-03T13:33', 'This is a testSession', 'z5135007@unsw.net','2')
    with pytest.raises(SessionDataException) as exe_info:
        test_seminar = createSeminar(
                    "test",
                    '2018-06-01T13:33', 
                    '2018-06-04T13:33',
                    '2018-06-01T10:33',
                    "This is a test event",
                    "40",
                    '2018-04-01T10:33',
                    {**session1, **session2},
                    '2'
            )
    assert(exe_info.type == SessionDataException)
    assert(exe_info.value.fieldname == 'session0_timeEnd')

def test_post_seminar_invalid_ssession_timeCom1():
    session1 = createSession(0, 'test', '2005-06-07T13:33', '2005-06-02T13:33', 'This is a testSession', 'z5135008@unsw.net','4')
    session2 = createSession(1, 'testSession2', '2005-06-01T13:33', '2005-06-03T13:33', 'This is a testSession', 'z5135007@unsw.net','2')
    with pytest.raises(SessionDataException) as exe_info:
        test_seminar = createSeminar(
                    "test",
                    '2018-06-01T13:33', 
                    '2018-06-04T13:33',
                    '2018-06-01T10:33',
                    "This is a test event",
                    "40",
                    '2018-04-01T10:33',
                    {**session1, **session2},
                    '2'
                )
    assert(exe_info.type == SessionDataException)
    assert(exe_info.value.fieldname == 'session0_timeEnd')

def test_post_seminar_invalid_ssession_des():
    session1 = createSession(0, 'test', '2005-06-01T13:33', '2005-06-02T13:33', '', 'z5135008@unsw.net','4')
    session2 = createSession(1, 'testSession2', '2005-06-01T13:33', '2005-06-03T13:33', 'This is a testSession', 'z5135007@unsw.net','2')
    with pytest.raises(SessionDataException) as exe_info:
        test_seminar = createSeminar(
                    "test",
                    '2018-06-01T13:33', 
                    '2018-06-04T13:33',
                    '2018-06-01T10:33',
                    "This is a test event",
                    "40",
                    '2018-04-01T10:33',
                    {**session1, **session2},
                    '2'
            )
    assert(exe_info.type == SessionDataException)
    assert(exe_info.value.fieldname == 'session0_description')

def test_post_seminar_invalid_ssession_email():
    session1 = createSession(0, 'test', '2005-06-01T13:33', '2005-06-02T13:33', 'desc', 'z5135008@unsw.net','4')
    session2 = createSession(1, 'testSession2', '2005-06-01T13:33', '2005-06-03T13:33', 'This is a testSession', 'z5135007unsw.net','2')
    with pytest.raises(SessionDataException) as exe_info:
        test_seminar = createSeminar(
                    "test",
                    '2018-06-01T13:33', 
                    '2018-06-04T13:33',
                    '2018-06-01T10:33',
                    "This is a test event",
                    "40",
                    '2018-04-01T10:33',
                    {**session1, **session2},
                    '2'
            )
    assert(exe_info.type == SessionDataException)
    assert(exe_info.value.fieldname == 'session1_presenter')

def test_post_seminar_invalid_ssession_capacity():
    session1 = createSession(0, 'test', '2005-06-01T13:33', '2005-06-02T13:33', 'desc', 'z5135008@unsw.net','4')
    session2 = createSession(1, 'testSession2', '2005-06-01T13:33', '2005-06-03T13:33', 'This is a testSession', 'z5135007@unsw.net','-1')
    with pytest.raises(SessionDataException) as exe_info:
        test_seminar = createSeminar(
                    "test",
                    '2018-06-01T13:33', 
                    '2018-06-04T13:33',
                    '2018-06-01T10:33',
                    "This is a test event",
                    "40",
                    '2018-04-01T10:33',
                    {**session1, **session2},
                    '2'
            )
    assert(exe_info.type == SessionDataException)
    assert(exe_info.value.fieldname == 'session1_capacity')


