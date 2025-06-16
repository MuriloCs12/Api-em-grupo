from utils import db

class Mensagem(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    conteudo = db.Column(db.String(500), nullable = False)

    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'))

    def __init__(self, conteudo):
        self.conteudo = conteudo
