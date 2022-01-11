# It became a __package__ cuz of it's name
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager #, login_manager

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crypto.db' #Uniform Resource Identifier
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.config['SECRET_KEY'] = 'c57fa793145800760a696639'
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page" #for login required authentication
login_manager.login_message_category = 'info' #same^
from crypto_package import routes

#DONE change db $ position change it to integer and go to market.html