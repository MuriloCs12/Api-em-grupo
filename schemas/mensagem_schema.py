from utils import ma
from marshmallow import fields, validate
from models.mensagens import Mensagem

class MensagemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mensagem
        load_instance = True  
        fields = ("id", "conteudo", "created_at", "id_usuario")
    id = fields.Int(dump_only=True)
    conteudo = fields.Str(required=True, validate=validate.Length(min=1, max=500))
    created_at = fields.DateTime(dump_only=True)
    id_usuario = fields.Int(dump_only=True)
