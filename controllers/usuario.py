from flask import Blueprint, jsonify, request
from models.usuario import Usuario
from utils import db, lm
from flask_login import current_user, login_required
from schemas.usuario_schema import UsuarioSchema
import hashlib

bp_usuarios = Blueprint("usuarios", __name__, template_folder='templates')

usuario_schema = UsuarioSchema()
usuarios_schema = UsuarioSchema(many=True)

@lm.user_loader
def load_user(id):
	usuario = Usuario.query.filter_by(id = id).first()
	return UsuarioSchema

@bp_usuarios.route('/', methods=['GET'])
def get_usuarios():
    usuarios = Usuario.query.all()
    return usuarios_schema.jsonify([user.to_dict() for user in usuarios]), 200

@bp_usuarios.route('/', methods=['POST'])
def create_usuario():
    schema = UsuarioSchema()
    schema.context = {}
    usuario = schema.load(request.get_json())

    usuario.senha = hashlib.sha256(usuario.senha.encode()).hexdigest()

    db.session.add(usuario)
    db.session.commit()

    return jsonify({"mensagem": "Usuário criado com sucesso."}), 201

@bp_usuarios.route('/<int:id>', methods=['PATCH'])
def atualizar_dados(id):
    usuario = Usuario.query.get_or_404(id, description="Nenhum usuário com esse ID foi encontrado.")
    dados = request.get_json()
    
    schema = UsuarioSchema()
    schema.context = {"id": id}
    dados_alterados = schema.load(dados, partial=True)

    if request.json.get("nome"):
        usuario.nome = dados_alterados.nome
    if request.json.get("email"):
        usuario.email = dados_alterados.email
    if request.json.get("senha"):
        usuario.senha = hashlib.sha256(dados_alterados.senha.encode()).hexdigest()
    
    nova_senha = dados.get('senha')
    if nova_senha:
        usuario.senha = hashlib.sha256(nova_senha.encode()).hexdigest()

    db.session.commit()

    return jsonify({"mensagem": "Dados atualizados com sucesso."}), 200


    