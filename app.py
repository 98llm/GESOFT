from flask import Flask, session, render_template, request, url_for, redirect, jsonify # noqa

from flask_sqlalchemy import SQLAlchemy

from flask_login import (
    UserMixin,
    login_user,
    logout_user,
    LoginManager,
    login_required,
    current_user)

from werkzeug.security import generate_password_hash, check_password_hash
from markupsafe import escape   # noqa
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
    anotacoes = db.relationship('Anotacao', backref='autor', lazy=True)
    ops = db.relationship('OP',
                          backref='responsavel',
                          lazy=True)

    def __repr__(self):
        return f'<user: {self.username}>'

    def __init__(self, username, password, nome, cargo):
        self.username = username
        self.password = generate_password_hash(password, "sha256")
        self.nome = nome
        self.cargo = cargo

    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)


class Anotacao(db.Model, UserMixin):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    assunto = db.Column(db.String(20), nullable=False)
    descricao = db.Column(db.String(150), nullable=False)
    dt_anotacao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) # noqa
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'))


class OP(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    qtd_placas = db.Column(db.Integer, nullable=False)
    num_romaneio = db.Column(db.String, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Em andamento')
    dta_emissao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow()) # noqa
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    id_cliente = db.Column(db.Integer, db.ForeignKey('cliente.id'))
    id_placa = db.Column(db.Integer, db.ForeignKey('placa.id'))


class Placa(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    codigo = db.Column(db.String, nullable=False, unique=True)
    descricao = db.Column(db.String, nullable=False)
    modelo = db.Column(db.String, nullable=True)
    qtd_componentes = db.Column(db.Integer, nullable=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('cliente.id'))
    ops = db.relationship('OP',
                          backref='placa_op',
                          lazy=True)
    componentes = db.relationship('Placa_componente',
                                  backref='relacao_componentes',
                                  lazy=True)


class Componente(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    codigo = db.Column(db.String, nullable=False, unique=True)
    tipo = db.Column(db.String, nullable=False)
    nome = db.Column(db.String, nullable=False)
    referencia = db.Column(db.String, nullable=False)


class Placa_componente(db.Model):
    id_placa = db.Column(db.Integer,
                         db.ForeignKey('placa.id'),
                         primary_key=True)
    id_componente = db.Column(db.Integer,
                              db.ForeignKey('componente.id'),
                              primary_key=True) # noqa


class Cliente(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    cnpj = db.Column(db.String, nullable=False)
    nome = db.Column(db.String, nullable=False)
    ops = db.relationship('OP',
                          backref='cliente')
    endereco = db.relationship('Endereco_cliente',
                               backref='endereco',
                               uselist=False)
    telefones = db.relationship('Telefone',
                                backref='cliente',
                                lazy=True)
    placas = db.relationship('Placa',
                             backref='cliente',
                             lazy=True)

    def __repr__(self):
        return f'<cliente: {self.nome}>'


class Telefone(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('cliente.id'))
    telefone = db.Column(db.String, nullable=False)


class Endereco_cliente(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('cliente.id'))
    logradouro = db.Column(db.String, nullable=False)
    numero = db.Column(db.String, nullable=False)
    bairro = db.Column(db.String, nullable=False)
    cep = db.Column(db.String(9), nullable=False)
    uf = db.Column(db.String(2), nullable=False)


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


@app.route('/cliente', methods=['GET'])
@login_required
def cliente():
    clientes = Cliente.query.all()
    return render_template(
                            'cliente.html',
                            user=current_user,
                            clientes=clientes
    )


@app.route('/cliente/adicionar', methods=['POST', 'GET'])
@login_required
def add_cliente():
    if request.method == 'POST':
        new_entity = Cliente(
                    nome=request.form['nome_cliente'],
                    cnpj=request.form['cnpj']
        )
        db.session.add(new_entity)
        db.session.commit()

        new_telefone = Telefone(
                    telefone=request.form['telefone'],
                    id_cliente=new_entity.id  # fk
        )
        new_endereco = Endereco_cliente(
                    logradouro=request.form['logradouro'],
                    numero=request.form['numero'],
                    bairro=request.form['bairro'],
                    cep=request.form['cep'],
                    uf=request.form['uf'],
                    id_cliente=new_entity.id  # fk
        )
        db.session.add(new_telefone)
        db.session.add(new_endereco)
        db.session.commit()
        return redirect(url_for('cliente'))
    return render_template('adiciona_cliente.html', user=current_user)


# rota para vizualizacao das OPs| Define pagina 1 como padrao
@app.route('/op', methods=['GET', 'POST'], defaults={'page_num': 1})
@app.route('/op/<int:page_num>', methods=['GET', 'POST'])
@login_required
def op(page_num):
    ops = OP.query.paginate(per_page=5, page=page_num, error_out=True)
    total = ops.total
    return render_template('op.html', user=current_user, ops=ops, total=total)


@app.route('/op/adicionar', methods=['POST', 'GET'])
@login_required
def add_op():
    clientes = Cliente.query.all()
    # retorna uma lista com todas as placas de um determinado cliente
    # [(cliente.placas) for cliente in Cliente.query.filter_by(id = 1)]
    if request.method == 'POST':
        new_op = OP(
                    qtd_placas=request.form['qtd_placas'],
                    num_romaneio=request.form['num_romaneio'],
                    dta_emissao=datetime.utcnow(),# noqa
                    id_usuario=current_user.id,  # fk
                    id_cliente=request.form.get('cliente'),
                    id_placa=request.form.get('placa'),
        )
        db.session.add(new_op)
        db.session.commit()
        return redirect(url_for('op'))
    return render_template('adicionar_op.html',
                           user=current_user,
                           clientes=clientes)


@app.route('/placa', methods=['POST', 'GET'])
@login_required
def consultar_placas():
    placas = Placa.query.all()
    return render_template('placa.html', placas=placas, user=current_user)


@app.route('/placa/add', methods=['POST', 'GET'])
@login_required
def adicionar_placas():
    clientes = Cliente.query.all()
    if request.method == 'POST':
        placa = Placa(
                      codigo=request.form['codigo'],
                      descricao=request.form['descricao'],
                      modelo=request.form['modelo'],
                      qtd_componentes=request.form['qtd_componentes'],
                      id_cliente=request.form['id_cliente']
                    )
        db.session.add(placa)
        db.session.commit()
        return redirect(url_for('consultar_placas'))
    return render_template('adiciona_placa.html',
                           clientes=clientes,
                           user=current_user)


@app.route('/api/cliente/<int:id_cliente>')
@login_required
def api_placas(id_cliente):
    cliente = Cliente.query.get(id_cliente)
    clienteDict = {}
    clienteDict['id'] = cliente.id
    clienteDict['nome'] = cliente.nome
    clienteDict['placas'] = []
    '''
    Para cada placa do cliente informado,
    adiciona as informações da mesma em um
    dict
    '''
    for placa in cliente.placas:
        placas_cliente = {}
        placas_cliente['id'] = placa.id
        placas_cliente['codigo'] = placa.codigo
        placas_cliente['descricao'] = placa.descricao
        placas_cliente['modelo'] = placa.modelo
        clienteDict['placas'].append(placas_cliente)
    return jsonify({'cliente': clienteDict})


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
