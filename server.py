from flask import Flask
from os.path import isfile
from sys import argv 
from config import config
from model.EMS import EMS
from flask_login import LoginManager


app = Flask(__name__, static_url_path='/static')
app.config.from_object(config)

# init login_manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(email):
    return ems.getUserByEmail(email)

# instantiate EMS 
ems = None

binFile = argv[1] if len(argv) > 1 else 'emsData.bin'
if len(argv) <= 1 and not isfile(binFile):
    ems = EMS(userCSV='user.csv', debug=type(config).__name__ == 'Development')
else:
    ems = EMS(binFile=binFile, debug=type(config).__name__ == 'Development')

