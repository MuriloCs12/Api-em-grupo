from flask import Blueprint, jsonify, request
from models.mensagens import Mensagem
from utils import db
from schemas.mensagem_schema import MensagemSchema

bp_mensagens = Blueprint('mensagem', __name__)
mensagem_schema = MensagemSchema()
mensagens_schema = MensagemSchema(many=True)

@bp_mensagens.route('/', methods=['GET'])
def read_all_mensagens():
    messages = Mensagem.query.all()
    return mensagens_schema.jsonify(messages), 200
    
@bp_mensagens.route('/<int:id>', methods=['GET'])
def read_one_mensagem(id):
    mensagem = Mensagem.query.get_or_404(id, description="Nenhuma mensagem com esse ID foi encontrada.")
    return mensagem_schema.jsonify(mensagem)

@bp_mensagens.route('/', methods=['POST'])
def criar_mensagem():
    conteudo = request.form.get('conteudo')
    if not conteudo:
        return jsonify({'mensagem': 'Campo conteúdo não preenchido'}), 400

    nova_mensagem = Mensagem(conteudo=conteudo)

    db.session.add(nova_mensagem)
    db.session.commit()
    return mensagem_schema.jsonify(nova_mensagem), 201

@bp_mensagens.route('/<int:id>', methods=['PUT'])
def update_mensagens(id):
    novo_conteudo = request.form.get('conteudo')
    mensagem = Mensagem.query.get_or_404(id, description="Nenhuma mensagem com esse ID foi encontrada.")
    
    if not novo_conteudo:
        return jsonify({'mensagem': 'Campo conteúdo precisa ser preenchido.'}), 400
    
    mensagem.conteudo = novo_conteudo
   
    db.session.commit()
    return mensagem_schema.jsonify(mensagem), 200

@bp_mensagens.route('/<int:id>', methods=['DELETE'])
def delete_mensagens(id):
    mensagem = Mensagem.query.get_or_404(id, description="Nenhuma mensagem com esse ID foi encontrada.")
    db.session.delete(mensagem)
    db.session.commit()
    return jsonify({'mensagem':'Sua mensagem foi deletada com sucesso!'})