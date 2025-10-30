from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os

# 🔹 Cria a aplicação Flask
app = Flask(__name__)

# 🔹 Configurações básicas
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://")

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["UPLOAD_FOLDER"] = "static/fotos_posts"
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "uma_chave_padrao_para_testes")  # CSRF funciona

# 🔹 Inicializa extensões
database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "homepage"

# 🔹 Carrega o usuário logado
@login_manager.user_loader
def load_user(user_id):
    from fakeprinterest.models import Usuario
    return Usuario.query.get(int(user_id))

# 🔹 Importa rotas
from fakeprinterest import routes

# 🔹 Cria tabelas automaticamente (somente se não existirem)
with app.app_context():
    from fakeprinterest import models
    database.create_all()
