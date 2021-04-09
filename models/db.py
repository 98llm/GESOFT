import psycopg2
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import sys
sys.path.append('d:/Users/Leandro/Documents/facul/GESOFT/GESOFT/')
from app import database


class User(UserMixin, db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique = True, nullable = False)
    password = db.Column(db.String, nullable = False)
    name = db.Column(db.String, nullable = False)
    function = db.Column(db.String, nullable = False)

    def __init__(self, username, password):
        self.username = username
        self.password = password



connection = psycopg2.connect(
    host ="localhost",
    user = "postgres",
    password = "Kenny121",
    databasename = "teste"
)

connection.close()
