from flask import Flask, request, jsonify, make_response, render_templatem, LoginManager,login_user, logout_user, login_required, current_user
from models.mensagens import Mensagem
from utils import db, ma, lm
from flask_migrate import Migrate
from controllers.mensagens import bp_mensagens
from controllers.usuario import bp_usuarios
from marshmallow import ValidationError
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dados.db'
app.json.sort_keys = False

db.init_app(app)
migrate = Migrate(app, db)
ma.init_app(app)
lm.init_app(app)

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

@app.route('/registro')
def registrar():
    return render_template('registro.html')

register_error_handlers(app)

if __name__ == '__main__':
    with app.app_context():  
        db.create_all()  
    app.run(debug=True)

