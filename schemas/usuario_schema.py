import re
from utils import ma
from marshmallow import fields, validates, ValidationError
from models.usuario import Usuario

class UsuarioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        load_instance = True
        fields = ("id", "nome", "email", "senha")

    id = fields.Int(dump_only=True)
    nome = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    email = fields.Email(required=True)
    senha = fields.Str(required=True, validate=validate.Length(min=8, max=16))