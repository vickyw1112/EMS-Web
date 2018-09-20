from functools import wraps
from flask_login import current_user
from flask import abort

"""
Return true if there's no exception when running
func with args
"""
def noException(func, *args):
    try:
        func(*args)
        return True
    except:
        return False


'''
Message for bootstrap alert
'''
class Message:
    def __init__(self, msg, cls):
        self.msg = msg
        self.cls = cls

    def __str__(self):
        return self.msg
    

"""
Func decorator for admin required route
"""
def staff_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.isStaff:
            abort(404)
        return f(*args, **kwargs)
    return decorated_function

"""
Convert a float value to money format
"""
def roundMoney(value):
    return '${:.2f}'.format(round(value, 2)) 
