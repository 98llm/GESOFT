from flask import ( # noqa
    Flask,
    session,
    render_template,
    request, url_for,
    flash,
    redirect)

from flask_sqlalchemy import SQLAlchemy

from flask_login import ( # noqa
    UserMixin,
    login_user,
    logout_user,
    LoginManager,
    login_required,
    current_user)

from werkzeug.security import generate_password_hash, check_password_hash
from markupsafe import escape # noqa
import psycopg2
from datetime import datetime

# Configure app
app = Flask(__name__)
app.config["SECRET_KEY"] = b"\x05\x19s\x8a\xd06\x07\xf8ofL0\xc5-\xc0"

# configure database
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:123@localhost:5432/teste" # noqa

db = SQLAlchemy(app)

login_manager = LoginManager(app)

login_manager.login_view = "login"

connection = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="123",
    dbname="teste"
)

cursor = connection.cursor()


class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    cargo = db.Column(db.String(50), nullable=False)

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
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    assunto = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.String(150), nullable=False)
    dt_anotacao = db.Column(db.String(50), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'))


class OP(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    codigo = db.Column(db.String(50), nullable=False)
    qtd_placas = db.Column(db.Integer, nullable=False)
    num_romaneio = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    dta_emissao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    id_cliente = db.Column(db.Integer, db.ForeignKey('cliente.id'))
    id_placa = db.Column(db.Integer, db.ForeignKey('placa.id'))


class Placa(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    codigo = db.Column(db.String, nullable=False)
    descricao = db.Column(db.String, nullable=False)
    modelo = db.Column(db.String, nullable=True)
    qtd_componente = db.Column(db.Integer, nullable=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('cliente.id'))
    # op = db.relationship('OP', backref='placas')


class Componente(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    codigo = db.Column(db.String, nullable=False)
    tipo = db.Column(db.String, nullable=False)
    nome = db.Column(db.String, nullable=False)
    referencia = db.Column(db.String, nullable=False)


class Placa_componente(db.Model):
    id_placa = db.Column(db.Integer, db.ForeignKey('placa.id'))
    id_componente = db.Column(db.Integer, db.ForeignKey('componente.id'))


class Cliente(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    cnpj = db.Column(db.String, nullable=False)
    nome = db.Column(db.String, nullable=False)
    # op = db.relationship('OP', backref='clientes')


class Telefone(db.Model):
    id_cliente = db.Column(db.Integer, db.ForeignKey('cliente.id'))
    telefone = db.Column(db.String, nullable=False)


class Endereco_cliente(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    logradouro = db.Column(db.String, nullable=False)
    numero = db.Column(db.String, nullable=False)
    bairro = db.Column(db.String, nullable=False)
    cep = db.Column(db.String, nullable=False)
    uf = db.Column(db.String, nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(user_id)


@app.route('/')
@login_required
def index():
    return render_template('home.html', user=current_user)


@app.route('/login', methods=['POST', 'GET'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = Usuario.query.filter_by(username=username).first()
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
