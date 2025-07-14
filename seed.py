from utils import db
from models.usuario import Usuario
from werkzeug.security import generate_password_hash
from app import app

with app.app_context():
    email_admin = "adm@gmail.com"
    
    admin_existente = Usuario.query.filter_by(email=email_admin).first()
    
    if admin_existente:
        print(f"Admin com email '{email_admin}' já existe.")
    else:
        admin = Usuario(
            nome="Admin1",
            email=email_admin,
            senha=generate_password_hash("senha123"),
            admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print("Usuário admin criado com sucesso.")