from flask import Flask, request, jsonify, make_response, render_template
from models.mensagens import Mensagem
from models.usuario import Usuario
from utils import db, ma, lm
from flask_migrate import Migrate
from controllers.mensagens import bp_mensagens
from controllers.usuario import bp_usuarios
from marshmallow import ValidationError
from werkzeug.exceptions import HTTPException, NotFound
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, get_jwt_identity, jwt_required, set_access_cookies, get_jwt
from datetime import datetime, timezone, timedelta
from werkzeug.security import check_password_hash


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dados.db'
app.config["JWT_SECRET_KEY"] = "senhascrt"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
app.json.sort_keys = False

db.init_app(app)
migrate = Migrate(app, db)
ma.init_app(app)
CORS(app)
jwt = JWTManager(app)

app.register_blueprint(bp_mensagens, url_prefix="/mensagens")
app.register_blueprint(bp_usuarios, url_prefix = '/usuarios')


def register_error_handlers(app):

    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        return jsonify({
            "error": "Validation Error",
            "mensagem": error.messages
        }), 400

    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        return jsonify({
            "error": error.name,
            "mensagem": error.description
        }), error.code

    @app.errorhandler(Exception)
    def handle_generic_exception(error):
        return jsonify({
            "error": "Internal Server Error",
            "mensagem": str(error)
        }), 500

    @app.errorhandler(NotFound)
    def handle_not_found_error(e):
        description = getattr(e, 'description', 'Recurso não encontrado')

        if isinstance(description, dict):
            return jsonify(description), 404
        
        return jsonify({"error": description}), 404

register_error_handlers(app)

@jwt.expired_token_loader
def token_expirado_callback(jwt_header, jwt_payload):
    tipo = jwt_payload.get("type", "access")
    return jsonify({"error": f"{tipo} token inválido ou expirado"}), 401

@app.route("/auth/login", methods=["POST"])
def login():
    nome = request.json.get("nome", None)
    senha = request.json.get("senha", None)
    user = Usuario.query.filter_by(nome = nome).first()

    if not nome or not senha:
        return jsonify({"errors": {"nome": ["Campo obrigatório."], "senha": ["Campo obrigatório."]}}), 422
    if not user or not check_password_hash(user.senha, senha):
        return jsonify({"error": "Credenciais inválidas"}), 401

    access_token = create_access_token(identity=str(user.id), fresh=True, additional_claims={"admin": user.admin})
    refresh_token = create_refresh_token(identity=str(user.id))
    return jsonify(access_token=access_token, refresh_token=refresh_token)


@app.route("/auth/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity, fresh=False)
    return jsonify(access_token=access_token)

    


if __name__ == '__main__':
    with app.app_context():  
        db.create_all()  
    app.run(debug=True)

