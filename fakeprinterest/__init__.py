from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)

# 🔹 Configurações básicas
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meubanco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SECRET_KEY"] = "9b2f9610da06841602fa28036d1b9448"
app.config["UPLOAD_FOLDER"] = "static/fotos_posts"

# 🔹 Extensões
database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "homepage"


# 🔹 Carregamento do usuário logado
@login_manager.user_loader
def load_user(user_id):
    from fakeprinterest.models import Usuario  # garante importação correta
    return Usuario.query.get(int(user_id))


# 🔹 Importa as outras rotas (login, feed, etc.)
from fakeprinterest import routes
