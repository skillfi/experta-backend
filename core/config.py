import logging
from base64 import urlsafe_b64encode

from cryptography.fernet import Fernet
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_mail import Mail
from flask_pymongo import PyMongo
from flask_sqlalchemy import SQLAlchemy
from requests_oauthlib.oauth2_session import OAuth2Session

from .config_db import DB_HOST, DB_NAME, DB_PASSWORD, DB_USERNAME

app = Flask('expertapp')

config = {'DB_USERNAME': DB_USERNAME,
          'DB_PASSWORD': DB_PASSWORD,
          'DB_HOST': DB_HOST,
          'DB_NAME': DB_NAME,
          'DB_PORT': str(27017),
          'DATE_FORMAT': '%Y-%m-%d',
          'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S'}

oauth = OAuth2Session(client=None)


app.config['SECRET_KEY'] = 'fefe517cdbef408b9fb501c239fbbccbexpertaa'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
# app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True

app.config["MONGO_URI"] = 'mongodb+srv://' + config['DB_USERNAME'] + ':' + \
                                        config['DB_PASSWORD'] + '@' + \
                                        config['DB_HOST'] + '/'+ config['DB_NAME'] + '?retryWrites=true&w=majority'


encryption = Fernet(urlsafe_b64encode(app.config["SECRET_KEY"][:32].encode()))

logger = logging.getLogger(app.name)
c_format = logging.Formatter('(%(asctime)s) - [%(filename)s - %(lineno)s] - %(message)s')
c_handler = logging.StreamHandler()
c_handler.setLevel(logging.ERROR)
c_handler.setFormatter(c_format)
logger.addHandler(c_handler)

cors = CORS(app, supports_credentials=True)
db = PyMongo(app).db
bcrypt = Bcrypt(app)
mail = Mail(app)
