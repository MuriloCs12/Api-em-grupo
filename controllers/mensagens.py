from flask import Blueprint, jsonify, request
from models.mensagens import Mensagem
from models.comentario import Comentario
from utils import db
from flask_login import current_user, login_required
from schemas.mensagem_schema import MensagemSchema
from schemas.comentario_schema import ComentarioSchema

bp_mensagens = Blueprint('mensagem', __name__)
mensagem_schema = MensagemSchema()
mensagens_schema = MensagemSchema(many=True)
comentario_schema = ComentarioSchema()

@bp_mensagens.route('/', methods=['GET'])
def read_all_mensagens():
    messages = Mensagem.query.all()
    return jsonify([msg.to_dict() for msg in messages]), 200
    
@bp_mensagens.route('/<int:id>', methods=['GET'])
@jwt_required()
def read_one_mensagem(id):
    mensagem = Mensagem.query.get_or_404(id, description="Nenhuma mensagem com esse ID foi encontrada.")
    return jsonify(mensagem.to_dict())

@bp_mensagens.route('/', methods=['POST'])
@jwt_required()
def criar_mensagem():
    mensagem = mensagem_schema.load(request.get_json())
    if not request.json.get("conteudo"):
        return jsonify({'mensagem': 'Campo conteúdo não preenchido'}), 400

    db.session.add(mensagem)
    db.session.commit()
    return jsonify(mensagem.to_dict()), 201

@bp_mensagens.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_mensagens(id):
    mensagem = Mensagem.query.get_or_404(id, description="Nenhuma mensagem com esse ID foi encontrada.")
    dados_mensagem = mensagem_schema.load(request.get_json())
    novo_conteudo = request.json.get("conteudo")

    if not novo_conteudo:
        return jsonify({'mensagem': 'Campo conteúdo precisa ser preenchido.'}), 400
    
    mensagem.conteudo = novo_conteudo
   
    db.session.commit()
    return jsonify(mensagem.to_dict()), 200

@bp_mensagens.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_mensagens(id):
    mensagem = Mensagem.query.get_or_404(id, description="Nenhuma mensagem com esse ID foi encontrada.")
    db.session.delete(mensagem)
    db.session.commit()
    return jsonify({'mensagem':'Sua mensagem foi deletada com sucesso!'})


@bp_mensagens.route('/<int:id>/comentarios', methods=['POST'])
@jwt_required()
def create_comentario(id):
    comentario = comentario_schema.load(request.get_json())
    if not request.json.get("conteudo"):
        return jsonify({'mensagem': 'Campo conteúdo não preenchido'}), 400
    
    comentario.id_mensagem = id

    db.session.add(comentario)
    db.session.commit()
    return comentario_schema.jsonify(comentario), 201

@bp_mensagens.route('/<int:id>/comentarios', methods=['GET'])
@jwt_required()
def listar_comentarios(id):
    comentarios = Comentario.query.filter_by(id_mensagem=id)
    return jsonify([cmt.to_dict() for cmt in comentarios]), 200

@bp_mensagens.route('/<int:id>/comentarios/<int:id_comt>', methods=['GET'])
@jwt_required()
def read_one_comentario(id, id_comt):
    comentario = Comentario.query.filter_by(id=id_comt, id_mensagem=id).first()

    if not comentario:
        return jsonify({"erro":"Algum ID inexistente recebido"})
    
    return comentario_schema.jsonify(comentario)

@bp_mensagens.route('/<int:id>/comentarios/<int:id_comt>', methods=['PUT'])
@jwt_required()
def update_comentario(id, id_comt):
    comentario = Comentario.query.filter_by(id=id_comt, id_mensagem=id).first()
    
    dados_comentario = comentario_schema.load(request.get_json())
    novo_conteudo = request.json.get("conteudo")

    if not novo_conteudo:
        return jsonify({'mensagem': 'Campo conteúdo precisa ser preenchido.'}), 400
    
    comentario.conteudo = novo_conteudo
   
    db.session.commit()
    return comentario_schema.jsonify(comentario), 200

@bp_mensagens.route('/<int:id>/comentarios/<int:id_comt>', methods=['DELETE'])
@jwt_required()
def delete_comentario(id, id_comt):
    comentario = Comentario.query.filter_by(id=id_comt, id_mensagem=id).first()

    if not comentario:
        return jsonify({"erro":"Algum ID inexistente recebido"})

    db.session.delete(comentario)
    db.session.commit()
    return jsonify({'mensagem':'Seu comentario foi deletado com sucesso!'})
