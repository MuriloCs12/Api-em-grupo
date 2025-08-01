from utils import db
from datetime import datetime

class Mensagem(db.Model):
    __tablename__ = "mensagem"
    id = db.Column(db.Integer, primary_key = True)
    titulo = db.Column(db.String(200), nullable = False)
    conteudo = db.Column(db.String(500), nullable = False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    comentarios = db.relationship("Comentario", backref="mensagem", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "conteudo": self.conteudo,
            "created_at": self.created_at.isoformat(),
            "id_usuario": self.id_usuario
        }