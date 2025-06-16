from utils import db
from flask_login import UserMixin

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(200), nullable = False)
    email = db.Column(db.String(100), unique = True)

    __init__(self, nome, email):
        self.nome = nome
        self.email = email