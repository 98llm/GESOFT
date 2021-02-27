from flask import Flask, session, render_template, request, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, logout_user, LoginManager, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from markupsafe import escape
import psycopg2

#Configure app
app = Flask(__name__)
app.config["SECRET_KEY"] = b"\x05\x19s\x8a\xd06\x07\xf8ofL0\xc5-\xc0"

#configure database
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:123@localhost:5432/teste"

db = SQLAlchemy(app)


login_manager = LoginManager(app)

login_manager.login_view = "login"

connection = psycopg2.connect(
    host ="localhost",
    user = "postgres",
    password = "123",
    dbname = "teste"
)

cursor = connection.cursor()


class User(db.Model, UserMixin):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, autoincrement = True ,primary_key=True)
    username = db.Column(db.String, unique = True, nullable = False)
    password = db.Column(db.String, nullable = False)
    name = db.Column(db.String, nullable = False)
    function = db.Column(db.String, nullable = False)

    def __repr__(self):
        return f'<user: {self.username}>'

    def __init__(self, username, password, name, function):
        self.username = username
        self.password = generate_password_hash(password, "sha256")
        self.name = name
        self.function = function

    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)

class Anotacao(db.Model, UserMixin):
    __tablename__ = 'anotacoes'
    id = db.Column(db.Integer, autoincrement = True ,primary_key=True)
    notes = db.Column(db.String, unique = True, nullable = False)
    name = db.Column(db.Integer, nullable = False, db.ForeignKey('User.id'))
    
class Endereco(db.Model, UserMixin):
    street = db.Column(db.String, nullable = False)
    cep = db.Column(db.String, nullable = False)
    number = db.Column(db.String, nullable = False)
    UF = db.Column(db.String, nullable = False)

class Entrega(db.Model, UserMixin):
    date = db.Column(db.String, nullable = False)
    status = db.Column(db.String, nullable = False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/')
@login_required
def index():
    return render_template('home.html', user= current_user)

@app.route('/login', methods = ['POST','GET'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(username = username).first()
    if user:
        if user and check_password_hash(user.password, password):
            login_user(user)
            session['username'] = user.username
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
