from flask import Blueprint, jsonify, request
from models.usuario import Usuario
from utils import db, lm
from flask_login import current_user, login_required
from schemas.usuario_schema import UsuarioSchema

bp_usuarios = Blueprint("usuarios", __name__, template_folder='templates')

usuario_schema = UsuarioSchema()

@lm.user_loader
def load_user(id):
	usuario = Usuario.query.filter_by(id = id).first()
	return usuario

@bp_usuarios.route('/', methods=['POST'])
def create_usuario():
    dados = usuario_schema.load(request.get_json())  # se for inválido, Marshmallow levanta erro 400 automaticamente

    senha_hash = hashlib.sha256(dados['senha'].encode()).hexdigest()

    novo_usuario = Usuario(
        nome=dados['nome'],
        email=dados['email'],
        senha=senha_hash
    )

    db.session.add(novo_usuario)
    db.session.commit()

    return jsonify({"mensagem": "Usuário criado com sucesso."}), 201

@bp_usuarios.route('/auth', methods=['POST'])
def autenticar_usuario():
    dados = request.get_json()
    email = dados.get('email')
    senha = dados.get('senha')

    if not email or not senha:
        return jsonify({"erro": "Email e senha são obrigatórios."}), 400

    usuario = Usuario.query.filter_by(email=email).first()
    senha_hash = hashlib.sha256(senha.encode()).hexdigest()

    if not usuario or usuario.senha != senha_hash:
        return jsonify({"erro": "Email ou senha incorretos."}), 401

    login_user(usuario)
    return jsonify({"mensagem": f"Bem-vindo, {usuario.nome}!"}), 200
    