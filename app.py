from flask import Flask, request, jsonify, make_response
from models.mensagens import mensagens

app = Flask(__name__)
app.json.sort_keys = False

@app.route('/mensagens', methods=['GET'])
def read_all_mensagens():
    return make_response(
        jsonify(mensagens)
    )

@app.route('/mensagens/<id>', methods=['GET'])
def read_one_mensagem(id):
    for mensagem in mensagens:
        if mensagem['id'] == id:
            return make_response(
                jsonify(mensagem)
            )

@app.route('/mensagens', methods=['POST'])
def create_mensagem():
    mensagem = request.json
    mensagens.append(mensagem)
    return make_response(
        jsonify(mensagens)
    )

@app.route('/mensagens/<id>', methods=['PUT'])
def update_mensagem(id):
    dados = request.json
    for mensagem in mensagens:
        if mensagem['id'] == id:
            mensagem['conteudo'] = dados.get('conteudo', mensagem['conteudo'])
            return make_response(
                jsonify(mensagens)
            )
        
@app.route('/mensagens/<id>', methods=['DELETE'])
def delete_mensagem(id):
    for mensagem in mensagens:
        if mensagem['id'] == id:
            mensagens.remove(mensagem)
            return make_response(
                jsonify(mensagens)
            )


if __name__ == '__main__':
    app.run(debug=True)

