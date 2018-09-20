from sample.events import Sample_Events
from sample.seminars import Sample_Seminars
from sample.users import users
import requests

SERVER_ADDR = 'http://127.0.0.1:5000'


# user registrations

events = Sample_Events().events
seminars = Sample_Seminars().seminars

i = 0
for user in users:
    r = requests.post(SERVER_ADDR + '/signup', data=user)
    if r.status_code == requests.codes.ok:
        print('[{}] new user - {}<{}>'.format(i, user['name'], user['email']))
    i += 1


# simulate login
print('Starting a new session')
s = requests.Session()
data = {'email': 'i@bopa.ng', 'password': 'samplepass'}
r = s.post(SERVER_ADDR + '/login', data=data)
if r.status_code == requests.codes.ok:
    print("Successfully logged in as a Staff")
cookies = r.cookies

i = 0
for e in events:
    r = s.post(SERVER_ADDR + '/post/course', data=e, cookies=cookies)
    if r.status_code == requests.codes.ok:
        print('[{}] new Course - {}'.format(i, e['title']))
    i += 1

for seminar in seminars:
    r = s.post(SERVER_ADDR + '/post/seminar', data=seminar, cookies=cookies)
    if r.status_code == requests.codes.ok:
        print('[{}] new Seminar - {}'.format(i, seminar['title']))
    i += 1
