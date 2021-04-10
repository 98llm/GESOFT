from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import psycopg2

# cria instancia flask
app = Flask(__name__)



# configura secrect key para sessão
app.config["SECRET_KEY"] = b"\x05\x19s\x8a\xd06\x07\xf8ofL0\xc5-\xc0"

# configura banco postgree URL
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:123@localhost:5432/teste" # noqa

# instancia gerenciador de login
login_manager = LoginManager(app)
# atribui a roda login como padrao para usuarios nao logados
login_manager.login_view = "login"

# atribui parametros do banco de dados
connection = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="123",
    dbname="teste"
)

# vincula PostgreSQL em uma sessao de banco
cursor = connection.cursor()
