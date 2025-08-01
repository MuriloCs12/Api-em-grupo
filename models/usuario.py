from utils import db
from flask_login import UserMixin

class Usuario(db.Model, UserMixin):
    __tablename__ = "usuario"
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(200), nullable = False)
    email = db.Column(db.String(100), unique = True)
    senha = db.Column(db.String(100), nullable = False)
    admin = db.Column(db.Boolean, default = False)

    mensagens = db.relationship("Mensagem", backref="usuario")
    comentarios = db.relationship("Comentario", backref="usuario")

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email
        }