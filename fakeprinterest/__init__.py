from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os  # 👈 importa o os pra ler variáveis de ambiente

app = Flask(__name__)

# 🔹 Configurações básicas
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")  # 👈 pega a URL do Render
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL").replace("postgresql://", "postgresql+psycopg://")
  # 👈 pega a chave do Render
app.config["UPLOAD_FOLDER"] = "static/fotos_posts"

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

# 🔹 Cria tabelas no banco (só se não existirem)
with app.app_context():
    from fakeprinterest import models
    database.create_all()
