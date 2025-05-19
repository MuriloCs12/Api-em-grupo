from flask import Flask, request, jsonify, make_response
from models.mensagens import Mensagem
from utils import db
from flask_migrate import Migrate
from utils import ma
from controllers.mensagens import bp_mensagem

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dados.db'
app.json.sort_keys = False

db.init_app(app)
migrate = Migrate(app, db)
ma.init_app(app)

app.register_blueprint(bp_mensagens, url_prefix="/mensagens")


if __name__ == '__main__':
    with app.app_context():  
        db.create_all()  
    app.run(debug=True)

