from utils import ma
from marshmallow import fields, validate
from models.comentario import Comentario

class ComentarioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Comentario
        load_instance = True  
        fields = ("id", "conteudo", "created_at", "id_usuario", "id_mensagem")
    id = fields.Int(dump_only=True)
    conteudo = fields.Str(required=True, validate=validate.Length(min=1, max=500))
    created_at = fields.DateTime(dump_only=True)
    id_usuario = fields.Int(dump_only=True)
    id_mensagem = fields.Int(dump_only=True)