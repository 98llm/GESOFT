import psycopg2
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import sys
sys.path.append('d:/Users/Leandro/Documents/facul/GESOFT/GESOFT/')
from app import database


class Users(UserMixin, db.Model):
    __tablename__ = 'Users'
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, unique = True, nullable = False)
    password = database.Column(database.String, nullable = False)

    def __init__(self, username, password):
        self.username = username
        self.password = password


connection = psycopg2.connect(
    host ="localhost",
    user = "postgres",
    password = "123",
    databasename = "teste"
)

connection.close()
