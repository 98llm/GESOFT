from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import *
import psycopg2


# Flask init
app = Flask(__name__)

# Flask-login instance config
login_manager = LoginManager(app)
login_manager.login_view = "login"


# SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"]= DATABASE_CONNECTION_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = b"\x05\x19s\x8a\xd06\x07\xf8ofL0\xc5-\xc0"


# SQLAlchemy db instance
db = SQLAlchemy(app)

# Postgres connection config
connection = psycopg2.connect(
    host=host,
    user=user,
    password=password,
    dbname=database,
)

cursor = connection.cursor()
