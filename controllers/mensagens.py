from flask import Blueprint, jsonify
from models.mensagens import Mensagem

bp_mensagens = Blueprint

@bp_mensagens.route('/', methods=['GET'])
def read_all_mensagens():
    mensagens = Mensagem.query.all()
    lista_mensagens = []
    for mensagem in mensagens:
        lista_mensagens.append({
            'id': mensagem.id,
            'conteudo': mensagem.conteudo,
        })
    return jsonify(lista_mensagens)
    
@bp_mensagens.route('/<int:id>', methods=['GET'])
def read_one_mensagem(id):
    mensagem = Mensagem.query.(id, description="Nenhuma mensagem com esse ID foi encontrada.")
    return jsonify({
        'id': mensagem.id,
        'conteudo': mensagem.conteudo
    })

@bp_mensagens.route('/', methods=['POST'])
def criar_mensagem():
    conteudo = request.form.get('conteudo')
    nova_mensagem = Mensagem(conteudo=conteudo)

    db.session.add(nova_mensagem)
    db.session.commit()
    return jsonify({
        'id': nova_mensagem.id,
        'conteudo': nova_mensagem.conteudo
    })

@bp_mensagens.route('/<int:id>', methods=['PUT'])
def update_mensagens(id):
    novo_conteudo = request.form.get('conteudo')
    mensagem = Mensagem.query.get_or_404(id, description="Nenhuma mensagem com esse ID foi encontrada.")
    mensagem.conteudo = novo_conteudo
    db.session.commit()
    return jsonify({
        'id': mensagem.id,
        'conteudo': mensagem.conteudo
    })

@bp_mensagens.route('/<int:id>', methods=['DELETE'])
def delete_mensagens(id):
    mensagem = Mensagem.query.get_or_404(id, description="Nenhuma mensagem com esse ID foi encontrada.")
    db.session.delete(mensagem)
    db.session.commit()
    return jsonify({'mensagem':'Sua mensagem foi deletada com sucesso!'})