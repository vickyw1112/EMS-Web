from server import app, ems
from flask import request, render_template, redirect, url_for, abort, send_from_directory, json, jsonify
from flask_login import login_required, login_user, current_user, logout_user
from model.event import Event, Status
from model.user import Staff, Guest
from parser import Parser, UserData
from utils import noException, Message, staff_required, roundMoney
from exceptions import *


"""
validate if the redirect url is within our domain
"""
def is_safe_url(url):
    return True

"""
Serve static files
"""
@app.route('/static/<path:file>')
def getStaticFile(file):
    return send_from_directory('static', file)


"""
Inject user view data into template as global
"""
@app.context_processor
def inject_user():
    if current_user.is_authenticated:
        return dict(
                user=current_user.parseToView, 
                Money=roundMoney, 
                eventColorMap=Event.COLOR_MAP,
                statusColorMap=Status.COLOR_MAP
                )
    else:
        return {
                'Money': roundMoney,
                'eventColorMap': Event.COLOR_MAP,
                'statusColorMap': Status.COLOR_MAP
                }


"""
Home page and list events by category
"""
@app.route('/', defaults={'type': 'all'})
@app.route('/category/<type>')
@login_required
def listOpenEvents(type):
    try:
        events = ems.getOpenEventsByCategory(type)
    # if request bad category
    except EMSException:
        abort(400)

    # parse Event Obj to eventData Obj for View
    data = [event.parseToView for event in events]  
    eventCategories = Event.ALL_CATEGORY.keys() 

    return render_template("index.html", category=type, name=current_user.name, 
            events=data, eventCategories=eventCategories)


"""
Login 
"""
@app.route('/login', methods = ['GET', 'POST'])
def login():
    msg = request.args.get('msg', False)
    if msg:
        msg = Message(msg, 'success')
    # redirect athenticated users
    if current_user.is_authenticated:
        return redirect(url_for('listOpenEvents'))

    # serve login page for GET request
    if request.method == 'GET':
        return render_template('login.html', msg=msg)

    # handle login for POST Request
    
    # ignore invalid request
    if not ('email' in request.form and 'password' in request.form):
        # bad request
        abort(400)

    user, msg_str = ems.login(request.form['email'], request.form['password'])
    if user:
        login_user(user)
        next = request.args.get('next')
        if not is_safe_url(next):
            return abort(400)

        return redirect(next or url_for('listOpenEvents'))
    else:
        msg = Message(msg_str, 'danger')
        return render_template('login.html', form=request.form, msg=msg)


"""
Logout
"""
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


"""
Events (detailed view)
"""
@app.route("/events/<eid>", methods = ['POST', 'GET'])
@login_required
def eventDetails(eid):
    try:
        event = ems.getEventById(int(eid))
    except Exception:
        abort(400)
    if not event:
        abort(404)

    viewData = event.parseToView
    canJoin = noException(event.joinCheck, current_user)
    canLeave = noException(event.leaveCheck, current_user)
    canChangeStatus = noException(event.changeStatusCheck, current_user)

    if request.method == 'GET':
        return render_template('event_details.html', event=viewData, name=current_user.name,
                canJoin=canJoin, canLeave=canLeave, canChangeStatus=canChangeStatus)

    # handle post request for join/leave event
    # and for admin to change status
    msg = False
    try:
        if request.form.get('action') == 'join':
            event.enrolUser(current_user, form=request.form)
            success_msg = "You have successfully joined this event"
            if current_user.isGuest and not event.hasPresenter(current_user):
                success_msg += ' for ${}'.format(event.currFee)
            msg = Message(success_msg, 'success')
        elif request.form.get('action') == 'leave':
            msg = Message("You have successfully left this event", 'success')
            event.unenrolUser(current_user)
        elif request.form.get('action') == 'changeStatus':
            status_str = request.form.get('status')
            if not status_str in Status.__members__:
                abort(400)
            status = Status[status_str.upper()]
            event.changeStatusCheck(current_user)
            current_user.changeEventStatus(event, status)
            if status == Status.CANCEL:
                # notify each user
                for u in ems.users.values():
                    if event.eid in [e.eid for e in u.events]:
                        u.addNotification('An event you have registered has been ' + 
                                'cancelled, click <a href="{}">here</a> for details'.format(
                                url_for('eventDetails', eid=event.eid)))

            msg = Message("You have successfully changed this event to the status: {}".format(status_str), 'success')
    except EventException as err:
        msg = Message(str(err), 'danger')

    # re-calculate everything after changes
    viewData = event.parseToView
    canJoin = noException(event.joinCheck, current_user)
    canLeave = noException(event.leaveCheck, current_user)
    return render_template('event_details.html', event=viewData, name=current_user.name, msg=msg,
                canJoin=canJoin, canLeave=canLeave, canChangeStatus=canChangeStatus)



@app.route('/post/<eventType>', methods=['POST', 'GET'])
@login_required
@staff_required
def postEvent(eventType):
    # see if given type is valid
    classname = eventType.capitalize()
    if not classname in Event.ALL_CATEGORY:
        abort(400)
    
    # serve corresponding post page for given type of event
    if request.method == 'GET':
        return render_template('post_{}.html'.format(eventType.lower()), 
            name=current_user.name)
    
    if request.method == 'POST':
        try:
            # instantiate a new obj of class of given classname
            eventData = Parser.ALL_DATA[classname].parseViewToModel(request.form.to_dict())
            # post event and retrieve the returned eid for the new event
            eid = current_user.postEvent(ems, classname, eventData)
        except (PostEventException, EventException) as err:
            msg = Message(str(err), 'danger')
            return render_template('post_{}.html'.format(eventType.lower()), 
                    msg=msg, name=current_user.name,
                    form=json.dumps(request.form))
        return redirect(url_for('eventDetails', eid=eid))


"""
Dashboard
"""
@app.route('/dashboard')
@login_required
def dashboard():
    myEvents = current_user.events
    eventCategories = Event.ALL_CATEGORY.keys() if current_user.isStaff else []
    return render_template('dashboard.html', eventCategories=eventCategories)


"""
Guest sign up
"""
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    # serve page on GET request
    if request.method == 'GET':
        return render_template('signup.html')

    # handle registration form
    try:
        userData = UserData.parseViewToModel(request.form)
        newGuest = Guest(userData)
        ems.addUser(newGuest)
    except Exception as err:
        msg = Message(str(err), 'danger')
        return render_template('signup.html', msg=msg, form=json.dumps(request.form))
    return redirect(url_for('login', msg='Successfully signed up'))


'''
All users profile
'''
@app.route('/profile', defaults={'uid': -1})
@app.route('/profile/<uid>')
@login_required
def profile(uid):
    if uid == -1:
        uid = current_user.uid
    user = ems.getUserById(int(uid))
    if not user:
        abort(404)

    userData = user.parseToView
    return render_template("profile.html", profile_user=userData)

'''
Clear user's notifications
'''
@app.route('/clearNotification', methods=['POST'])
@login_required
def clearNotification():
    current_user.clearNotification()
    return redirect(request.form.get('url'))

'''
API for session speaker auto complete
'''
@app.route('/api/users')
@login_required
@staff_required
def api_users():
    query = request.args.get('query')
    suggestions = []
    for user in ems.users.values():
        if query.lower() in user.name.lower() or query.lower() in user.email.lower():
            suggestions.append({
                'value': '{}<{}>'.format(user.name, user.email),
                'data': user.email
            })
    response = {
        'query': 'Unit',
        'suggestions': suggestions
    }
    return jsonify(response)
