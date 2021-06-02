from __init__ import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class Usuario(db.Model, UserMixin):
    id = db.Column(
        db.Integer,
        autoincrement=True,
        primary_key=True
    )
    username = db.Column(
        db.String,
        unique=True,
        nullable=False
    )
    password = db.Column(
        db.String,
        nullable=False
    )
    nome = db.Column(
        db.String(50),
        nullable=False
    )
    img_file = db.Column(
        db.String(20),
        nullable=False,
        default='default.jpg'
    )
    cargo = db.Column(
        db.String(50),
        nullable=False
    )
    anotacoes = db.relationship(
        'Anotacao',
        backref='autor',
        lazy=True
    )
    ops = db.relationship(
        'OP',
        backref='responsavel',
        lazy=True
    )

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
    id = db.Column(
        db.Integer,
        autoincrement=True,
        primary_key=True
    )
    titulo = db.Column(
        db.String(20),
        nullable=False
    )
    descricao = db.Column(db.String(150), nullable=False)
    dt_anotacao = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )
    id_usuario = db.Column(
        db.Integer,
        db.ForeignKey('usuario.id')
    )


class OP(db.Model):
    id = db.Column(
        db.Integer,
        autoincrement=True,
        primary_key=True
    )
    qtd_placas = db.Column(
        db.Integer,
        nullable=False
    )
    num_romaneio = db.Column(
        db.String,
        nullable=False
    )
    status = db.Column(
        db.String(20),
        nullable=False,
        default='Em andamento'
    )
    dta_emissao = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime
    )
    id_usuario = db.Column(
        db.Integer,
        db.ForeignKey('usuario.id')
    )
    id_cliente = db.Column(
        db.Integer,
        db.ForeignKey('cliente.id')
    )
    id_placa = db.Column(
        db.Integer,
        db.ForeignKey('placa.id')
    )


class Placa(db.Model):
    id = db.Column(
        db.Integer,
        autoincrement=True,
        primary_key=True
    )
    codigo = db.Column(
        db.String,
        nullable=False,
        unique=True
    )
    descricao = db.Column(
        db.String,
        nullable=False
    )
    modelo = db.Column(
        db.String,
        nullable=True
    )
    qtd_componentes = db.Column(
        db.Integer,
        nullable=True
    )
    id_cliente = db.Column(
        db.Integer,
        db.ForeignKey('cliente.id')
    )
    ops = db.relationship(
        'OP',
        backref='placa_op',
        lazy=True
    )
    componentes = db.relationship(
        'Placa_componente',
        backref='relacao_componentes',
        lazy=True
    )


class Componente(db.Model):
    id = db.Column(
        db.Integer,
        autoincrement=True,
        primary_key=True
    )
    codigo = db.Column(
        db.String,
        nullable=False,
        unique=True
    )
    tipo = db.Column(
        db.String,
        nullable=False
    )
    nome = db.Column(
        db.String,
        nullable=False
    )
    referencia = db.Column(
        db.String,
        nullable=False
    )


class Placa_componente(db.Model):
    id_placa = db.Column(
        db.Integer,
        db.ForeignKey('placa.id'),
        primary_key=True
    )
    id_componente = db.Column(
        db.Integer,
        db.ForeignKey('componente.id'),
        primary_key=True
    )


class Cliente(db.Model):
    id = db.Column(
        db.Integer,
        autoincrement=True,
        primary_key=True
    )
    cnpj = db.Column(
        db.String,
        nullable=False
    )
    nome = db.Column(
        db.String,
        nullable=False
    )
    ops = db.relationship(
        'OP',
        backref='cliente'
    )
    endereco = db.relationship(
        'Endereco_cliente',
        backref='endereco',
        uselist=False
    )
    telefones = db.relationship(
        'Telefone',
        backref='cliente',
        lazy=True
    )
    placas = db.relationship(
        'Placa',
        backref='cliente',
        lazy=True
    )

    def __repr__(self):
        return f'<cliente: {self.nome}>'


class Telefone(db.Model):
    id = db.Column(
        db.Integer,
        autoincrement=True,
        primary_key=True
    )
    id_cliente = db.Column(
        db.Integer,
        db.ForeignKey('cliente.id')
    )
    telefone = db.Column(
        db.String,
        nullable=False
    )


class Endereco_cliente(db.Model):
    id = db.Column(
        db.Integer,
        autoincrement=True,
        primary_key=True
    )
    id_cliente = db.Column(
        db.Integer,
        db.ForeignKey('cliente.id')
    )
    logradouro = db.Column(
        db.String,
        nullable=False
    )
    numero = db.Column(
        db.String,
        nullable=False
    )
    bairro = db.Column(
        db.String,
        nullable=False
    )
    cep = db.Column(
        db.String(9),
        nullable=False
    )
    uf = db.Column(
        db.String(2),
        nullable=False
    )
