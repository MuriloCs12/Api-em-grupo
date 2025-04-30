from utils import db

class Mensagem(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    conteudo = db.Column(db.String(500), nullable = False)

    def __init__(self, conteudo):
        self.conteudo = conteudo
