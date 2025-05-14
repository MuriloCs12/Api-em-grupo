from flask import Flask, request, jsonify, make_response
from models.mensagens import Mensagem
from utils import db
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dados.db'
app.json.sort_keys = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/mensagens', methods=['GET'])
def read_all_mensagens():
    mensagens = Mensagem.query.all()
    lista_mensagens = []
    for mensagem in mensagens:
        lista_mensagens.append({
            'id': mensagem.id,
            'conteudo': mensagem.conteudo,
        })
    return jsonify(lista_mensagens)
    
@app.route('/mensagens/<int:id>', methods=['GET'])
def read_one_mensagem(id):
    mensagem = Mensagem.query.(id, description="Nenhuma mensagem com esse ID foi encontrada.")
    return jsonify({
        'id': mensagem.id,
        'conteudo': mensagem.conteudo
    })

@app.route('/mensagens', methods=['POST'])
def criar_mensagem():
    conteudo = request.form.get('conteudo')
    nova_mensagem = Mensagem(conteudo=conteudo)

    db.session.add(nova_mensagem)
    db.session.commit()
    return jsonify({
        'id': nova_mensagem.id,
        'conteudo': nova_mensagem.conteudo
    })

@app.route('/mensagens/<int:id>', methods=['PUT'])
def update_mensagens(id):
    novo_conteudo = request.form.get('conteudo')
    mensagem = Mensagem.query.get_or_404(id, description="Nenhuma mensagem com esse ID foi encontrada.")
    mensagem.conteudo = novo_conteudo
    db.session.commit()
    return jsonify({
        'id': mensagem.id,
        'conteudo': mensagem.conteudo
    })

@app.route('/mensagens/<int:id>', methods=['DELETE'])
def delete_mensagens(id):
    mensagem = Mensagem.query.get_or_404(id, description="Nenhuma mensagem com esse ID foi encontrada.")
    db.session.delete(mensagem)
    db.session.commit()
    return jsonify({'mensagem':'Sua mensagem foi deletada com sucesso!'})

if __name__ == '__main__':
    with app.app_context():  
        db.create_all()  
    app.run(debug=True)

