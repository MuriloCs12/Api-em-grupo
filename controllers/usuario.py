from flask import Blueprint, jsonify, request
from models.usuario import Usuario
from utils import db, lm
from flask_login import current_user, login_required
from schemas.usuario_schema import UsuarioSchema
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, verify_jwt_in_request, get_jwt
from werkzeug.security import generate_password_hash
from datetime import datetime, timezone, timedelta
from functools import wraps
import hashlib

bp_usuarios = Blueprint("usuarios", __name__, template_folder='templates')

usuario_schema = UsuarioSchema()
usuarios_schema = UsuarioSchema(many=True)

def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if not claims.get("admin", False):
            return jsonify({"msg": "Acesso negado: administrador apenas."}), 403
        return func(*args, **kwargs)
    return wrapper

@bp_usuarios.route('/', methods=['GET'])
@jwt_required()
@admin_required
def get_usuarios():
    usuarios = Usuario.query.all()
    return usuarios_schema.jsonify([user.to_dict() for user in usuarios]), 200

@bp_usuarios.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_usuario(id):
    usuario_observado = Usuario.query.get_or_404(id, description="Usuário não encontrado.")
    usuario_atual = Usuario.query.get_or_404(int(get_jwt_identity()), description="Usuário não encontrado.")

    if id != usuario_atual.id and not usuario_atual.admin:
        return jsonify({"error": "Você não tem permissão para acessar este usuário"}), 403

    return jsonify(usuario_observado.to_dict())
    
    
@bp_usuarios.route('/', methods=['POST'])
def create_usuario():
    data = request.get_json()
    if not data.get('nome') or not data.get('email') or not data.get('senha'):
        return jsonify({"errors": {"nome":["Campo obrigatório."], "email": ["Campo obrigatório."], "senha": ["Campo obrigatório."]}}), 422

    schema = UsuarioSchema()
    usuario = schema.load(request.get_json())

    usuario.senha = generate_password_hash(usuario.senha)

    db.session.add(usuario)
    db.session.commit()

    return jsonify({"mensagem": "Usuário criado com sucesso."}), 201


@bp_usuarios.route("/<int:id>", methods=["DELETE"])
@jwt_required()
@admin_required
def excluir_usuario(id):
    usuario = Usuario.query.get_or_404(id, description="Usuário não encontrado.")

    db.session.delete(usuario)
    db.session.commit()
    return jsonify({"mensagem": f"Usuário {usuario.nome} foi excluído com sucesso."}), 200


@bp_usuarios.route('/<int:id>', methods=['PATCH'])
@jwt_required()
def atualizar_dados(id):
    usuario = Usuario.query.get_or_404(id, description="Usuário não encontrado.")

    user = Usuario.query.get_or_404(int(get_jwt_identity()), description="Usuário não encontrado.")
    if user.id != id and not user.admin:
        return jsonify({"error": "Você não tem permissão para alterar este usuário"}), 403

    dados = request.get_json()
    
    schema = UsuarioSchema()
    schema.context = {"id": id}
    dados_alterados = schema.load(dados, partial=True)

    if request.json.get("nome"):
        usuario.nome = dados_alterados.nome
    if request.json.get("email"):
        usuario.email = dados_alterados.email
    if request.json.get("senha"):
        usuario.senha = generate_password_hash(dados_alterados.senha)

    db.session.commit()

    return jsonify({"mensagem": "Dados atualizados com sucesso."}), 200


@bp_usuarios.route("<int:id>/promover", methods=["PATCH"])
@jwt_required()
@admin_required
def promover_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    usuario.admin = True
    db.session.commit()
    return jsonify({"msg": f"Usuário {usuario.nome} promovido a admin."})