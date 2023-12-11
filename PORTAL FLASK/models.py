from main import db
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import pytz

class Pings(db.Model):
    id_programa = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_vantive = db.Column(db.String(30), nullable=False)
    cliente = db.Column(db.String(120), nullable=False)
    ip = db.Column(db.String(30), nullable=False)
    situacao = db.Column(db.Boolean, nullable=False)
    tipo_cliente = db.Column(db.String(30), nullable=False)
    sla = db.Column(db.String(7), nullable=True)
    vezes_off = db.Column(db.Integer, nullable=False)
    grupo = db.Column(db.String(20), nullable=True)
    vip = db.Column(db.String(20), nullable=True)
    ponta = db.Column(db.String(10), nullable=True)
    id_associado = db.Column(db.String(30), nullable=True)

    def __repr__(self):
        return '<Name %r>' % self.name

class Horarios(db.Model):
    id_horario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ultimo_ping = db.Column(db.String(30), nullable=True)
    tipo_cliente = db.Column(db.String(30), nullable=True)

    def __repr__(self):
        return '<Name %r>' % self.name

class Excluidos(db.Model):
    id_programa = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_vantive = db.Column(db.String(30), nullable=False)
    cliente = db.Column(db.String(120), nullable=False)
    ip = db.Column(db.String(30), nullable=False)
    situacao = db.Column(db.Boolean, nullable=True)
    tipo_cliente = db.Column(db.String(30), nullable=True)
    sla = db.Column(db.String(7), nullable=True)
    vezes_off = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return '<Name %r>' % self.name
    
class Usuarios(db.Model):
    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(30), nullable=False)
    re = db.Column(db.String(30), nullable=False, unique=True)
    senha = db.Column(db.String(8), nullable=False)
    permissao = db.Column(db.String(30), nullable=False)
    
    def __repr__(self):
        return '<Name %r>' % self.name
    
class Dados(db.Model):
    id_prog = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ip = db.Column(db.String(15), nullable=False)
    id_vantive = db.Column(db.String(50), nullable=True)
    usuario = db.Column(db.String(100), nullable=False)
    nome = db.Column(db.String(30), nullable=False)
    dia = db.Column(db.DateTime, default=datetime.now(pytz.timezone('America/Sao_Paulo')))
    
    def __repr__(self):
        return '<Name %r>' % self.name