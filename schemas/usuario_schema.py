from utils import ma
from marshmallow import fields, validates, validate, validates_schema, ValidationError
from models.usuario import Usuario
import re

class UsuarioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        load_instance = True  
        fields = ("id", "nome", "email", "senha")
    id = fields.Int(dump_only=True)
    nome = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    email = fields.Email(required=True)
    senha = fields.Str(required=True)

    @validates('nome')
    def validar_nome_unico(self, value, **kwargs):
        user_id = self.context.get("id")
        nome_existe = Usuario.query.filter_by(nome=value).first()
        if nome_existe:
            raise ValidationError("Nome já existe.")

    @validates("email")
    def validar_email_unico(self, value, **kwargs):
        user_id = self.context.get("id")
        email_existe = Usuario.query.filter_by(email=value).first()
        if email_existe:
            raise ValidationError("Email já está em uso.")

    @validates('senha')
    def validar_senha_complexa(self, senha, **kwargs):
        regular_expression = r'^(?=.*[0-9])(?=.*[A-Z])(?=.*[a-z])(?=.*[@!%*?&]).{8,}$'
        if not re.match(regular_expression, senha):
            raise ValidationError(
                "A senha deve ter pelo menos 8 caracteres, "
                "conter pelo menos um dígito, uma letra maiúscula, "
                "uma letra minúscula e um caractere especial (@!%*?&)."
            )