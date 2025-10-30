#estrutura de banco de dados
from fakeprinterest import database, login_manager
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from flask_login import UserMixin

default = datetime.now(timezone.utc)


@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))


class Usuario(database.Model, UserMixin):
    __tablename__ = "usuario"

    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    fotos = relationship("Foto", backref="usuario", lazy=True)


class Foto(database.Model):
    __tablename__ = "foto"
    __table_args__ = {"extend_existing": True}  # evita erro de redefinição

    id = database.Column(database.Integer, primary_key=True)
    imagem = database.Column(database.String, default="default.png")
    data_criacao = database.Column(
        database.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    id_usuario = database.Column(database.Integer, database.ForeignKey("usuario.id"), nullable=False)
    descricao = database.Column(database.String(200))  # novo campo adicionado
