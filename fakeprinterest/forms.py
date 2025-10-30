from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from flask_wtf.file import FileAllowed
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from fakeprinterest.models import Usuario


class FormLogin(FlaskForm):
    email = StringField ("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("senha", validators=[DataRequired()])
    botao_aleatorio = SubmitField("Fazer Login")


class FormConta(FlaskForm):
    email = StringField("E-mail",validators=[DataRequired(), Email()])
    senha = PasswordField ("Senha", validators= [DataRequired(), Length(6, 20)])
    username = StringField ("Username", validators= [DataRequired()])
    confirmacao_senha = PasswordField ("confirmacao de senha", validators=[DataRequired(),EqualTo("senha")])
    botao_aleatorio =  SubmitField("Criar Conta")


def validate_email(self, email):
    usuario = Usuario.query.filter_by(email=email.data).first()
    if usuario:
        return ValidationError("E-mail ja cadastrado, Faça login para continuar")

class FormFoto(FlaskForm):
    foto = FileField("Foto", validators=[DataRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Apenas imagens são permitidas!')])
    botao_confirmacao = SubmitField ("Enviar")
    descricao = StringField('Descrição da foto', validators=[DataRequired()])
