from flask import Blueprint, jsonify, request
from models.mensagens import Mensagem
from models.usuario import Usuario
from models.comentario import Comentario
from controllers.usuario import admin_required
from utils import db
from flask_login import current_user, login_required
from schemas.mensagem_schema import MensagemSchema
from schemas.comentario_schema import ComentarioSchema
from flask_jwt_extended import jwt_required, get_jwt_identity

bp_mensagens = Blueprint('mensagem', __name__)
mensagem_schema = MensagemSchema()
mensagens_schema = MensagemSchema(many=True)
comentario_schema = ComentarioSchema()
comentarios_schema = ComentarioSchema(many=True)

@bp_mensagens.route('/', methods=['GET'])
def read_all_mensagens():
    messages = Mensagem.query.all()
    return mensagens_schema.jsonify([msg.to_dict() for msg in messages]), 200
    
@bp_mensagens.route('/<int:id>', methods=['GET'])
@jwt_required()
def read_one_mensagem(id):
    mensagem = Mensagem.query.get_or_404(id, description="Nenhuma mensagem com esse ID foi encontrada.")
    return jsonify(mensagem.to_dict_com_comentarios())

@bp_mensagens.route('/', methods=['POST'])
@jwt_required()
def criar_mensagem():
    mensagem = mensagem_schema.load(request.get_json())
    usuario = Usuario.query.get_or_404(int(get_jwt_identity()), description="Usuário não encontrado.")

    if not request.json.get("conteudo") or not request.json.get("titulo"):
        return jsonify({'erro': 'Algum campo não preenchido'}), 400 

    mensagem.id_usuario = usuario.id

    db.session.add(mensagem)
    db.session.commit()
    return jsonify(mensagem.to_dict()), 201

@bp_mensagens.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_mensagens(id):
    usuario = Usuario.query.get_or_404(int(get_jwt_identity()), description="Usuário não encontrado.")
    mensagem = Mensagem.query.get_or_404(id, description="Nenhuma mensagem com esse ID foi encontrada.")
    if mensagem.id_usuario != usuario.id and not usuario.admin:
        return jsonify({"erro":"Você não tem permissão para atualizar esta mensagem."}), 403
    
    dados_mensagem = mensagem_schema.load(request.get_json())
    novo_titulo = request.json.get("titulo")
    novo_conteudo = request.json.get("conteudo")

    if not novo_titulo or not novo_conteudo:
        return jsonify({'mensagem': 'Título e conteúdo são obrigatórios.'}), 400
    
    mensagem.titulo = novo_titulo
    mensagem.conteudo = novo_conteudo
   
    db.session.commit()
    return jsonify(mensagem.to_dict()), 200

@bp_mensagens.route('/<int:id>', methods=['PATCH'])
@jwt_required()
def update_parcial(id):
    usuario = Usuario.query.get_or_404(int(get_jwt_identity()), description="Usuário não encontrado.")
    mensagem = Mensagem.query.get_or_404(id, description="Nenhuma mensagem com esse ID foi encontrada.")
    if mensagem.id_usuario != usuario.id and not usuario.admin:
        return jsonify({"mensagem":"Erro. Você não tem permissão para atualizar esta mensagem."}), 403
    
    dados = request.get_json()
    
    schema = MensagemSchema()
    schema.context = {"id": id}
    dados_alterados = schema.load(dados, partial=True)

    if request.json.get("titulo"):
        mensagem.titulo = dados_alterados.titulo
    if request.json.get("conteudo"):
        mensagem.conteudo = dados_alterados.conteudo

    db.session.commit()
    return jsonify({"mensagem": "Dados atualizados com sucesso."}), 200

@bp_mensagens.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_mensagens(id):
    mensagem = Mensagem.query.get_or_404(id, description="Nenhuma mensagem com esse ID foi encontrada.")

    usuario = Usuario.query.get_or_404(int(get_jwt_identity()), description="Usuário não encontrado.")

    if mensagem.id_usuario != usuario.id and not usuario.admin:
        return jsonify({'erro': 'Você não tem permissão para deletar esta mensagem.'}), 403

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
    comentario.id_usuario = int(get_jwt_identity())

    db.session.add(comentario)
    db.session.commit()
    return comentario_schema.jsonify(comentario), 201

@bp_mensagens.route('/<int:id>/comentarios', methods=['GET'])
@jwt_required()
def listar_comentarios(id):
    comentarios = Comentario.query.filter_by(id_mensagem=id)
    return jsonify([cmt.to_dict() for cmt in comentarios]), 200


@bp_mensagens.route('/<int:id>/comentarios/<int:id_comt>', methods=['PUT'])
@jwt_required()
def update_comentario(id, id_comt):
    comentario = Comentario.query.filter_by(id=id_comt, id_mensagem=id).first()
    usuario = Usuario.query.get_or_404(int(get_jwt_identity()), description="Usuário não encontrado.")

    if not comentario:
        return jsonify({"erro":"Algum ID inexistente recebido"})

    
    if comentario.id_usuario != usuario.id and not usuario.admin:
        return jsonify({'erro': 'Você não tem permissão para atualizar este comentário.'}), 403

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

    usuario = Usuario.query.get_or_404(int(get_jwt_identity()), description="Usuário não encontrado.")

    if not comentario:
        return jsonify({"erro":"Algum ID inexistente recebido"})

    if comentario.id_usuario != usuario.id and not usuario.admin:
        return jsonify({'erro': 'Você não tem permissão para deletar este comentário.'}), 403

    db.session.delete(comentario)
    db.session.commit()
    return jsonify({'mensagem':'Seu comentario foi deletado com sucesso!'})
