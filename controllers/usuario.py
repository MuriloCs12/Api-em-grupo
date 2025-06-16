from flask import Blueprint, jsonify, request
from models.usuario import Usuario
from utils import db, lm
from schemas.mensagem_schema import MensagemSchema

bp_usuarios = Blueprint("usuarios", __name__, template_folder='templates')

@lm.user_loader
def load_user(id):
	usuario = Usuario.query.filter_by(id = id).first()
	return usuario

@bp_usuarios.route('/', methods=['POST'])
def create_usuario():
    nome = request.form.get('nome')
    email = request.form.get('email')
    senha = request.form.get('senha')
    senha_hash = hashlib.sha256(senha.encode())
    csenha = request.form.get('csenha')
    
    username_existente = Usuario.query.filter_by(username=username).first()
    if username_existente:
        flash('Nome de usuário já está em uso')
        return redirect('/registrar')
    
    if senha == csenha:
        usuario = Usuario(username, email, senha_hash.hexdigest())
        db.session.add(usuario)
        db.session.commit()
        flash ('Dados cadastrados com sucesso')
        return redirect('/entrar')
    else:
        flash ('Erro. Senhas não correspondentes')
        return redirect('/registrar')

@bp_usuarios.route('/auth', methods=['POST'])
def autenticar_usuario():
    login = request.form.get('login')
    senha = request.form.get('senha')

    user = Usuario.query.filter((Usuario.nome == login) | (Usuario.email == login)).first()

    if user and user.senha == hashlib.sha256(senha.encode()).hexdigest():
        login_user(user)
        return redirect('/r')
    
  
    flash('Usuário ou senha inválidos.', 'danger')
    return redirect('/entrar')