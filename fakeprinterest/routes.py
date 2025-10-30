


from flask import render_template, url_for, redirect
from fakeprinterest import app, database, bcrypt
from flask_login import login_required, login_user, logout_user, current_user
from fakeprinterest.forms import FormLogin, FormConta, FormFoto
from fakeprinterest.models import Usuario, Foto
from werkzeug.utils import secure_filename
from os import path, mkdir
import os
from flask import request

# Defina a pasta de upload no app
app.config["UPLOAD_FOLDER"] = "static/fotos_posts"




@app.route("/", methods=["GET", "POST"])
def homepage():
    form_login = FormLogin()
    if form_login.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario)
            return redirect(url_for("perfil", id_usuario=usuario.id))
    return render_template("homepage.html", form=form_login)


@app.route("/criarconta", methods=["GET", "POST"])
def criarconta():
    form_criarconta = FormConta()
    if form_criarconta.validate_on_submit():
        senha = bcrypt.generate_password_hash(form_criarconta.senha.data).decode('utf-8')
        usuario = Usuario(
            username=form_criarconta.username.data,
            senha=senha,
            email=form_criarconta.email.data
        )
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember=True)
        return redirect(url_for("perfil", id_usuario=usuario.id))
    return render_template("formcriarconta.html", form=form_criarconta)


@app.route("/perfil/<id_usuario>", methods=["GET", "POST"])
@login_required
def perfil(id_usuario):
    usuario = Usuario.query.get(int(id_usuario))

    # Se for o próprio usuário
    if int(id_usuario) == int(current_user.id):
        form_foto = FormFoto()

        if form_foto.validate_on_submit():
            arquivo = form_foto.foto.data
            nome_seguro = secure_filename(arquivo.filename)

            # Caminho absoluto para salvar e garantir que a pasta exista
            UPLOAD_FOLDER = os.path.join(
                os.path.abspath(os.path.dirname(__file__)),
                app.config["UPLOAD_FOLDER"]
            )
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)

            caminho = os.path.join(UPLOAD_FOLDER, nome_seguro)
            arquivo.save(caminho) 

            # Salvar no banco de dados com descrição
            foto = Foto(
                imagem=nome_seguro,
                descricao=form_foto.descricao.data,
                id_usuario=current_user.id
            )
            database.session.add(foto)
            database.session.commit()

            return redirect(url_for("perfil", id_usuario=current_user.id))

        return render_template("perfil.html", usuario=current_user, form=form_foto)

    # Outro usuário: não mostra formulário
    else:
        return render_template("perfil.html", usuario=usuario, form=None)



@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage"))

@app.route("/feed")
@login_required
def feed():
    q = request.args.get("q", "").strip()  # pega o que foi digitado

    if q:
        # Busca fotos cujo username ou descrição contenha a palavra pesquisada
        fotos = Foto.query.join(Usuario).filter(
            (Usuario.username.ilike(f"%{q}%")) | (Foto.descricao.ilike(f"%{q}%"))
        ).order_by(Foto.data_criacao.desc()).all()
    else:
        # Se não houver pesquisa, mostra todas
        fotos = Foto.query.order_by(Foto.data_criacao.desc()).all()

    return render_template("feed.html", fotos=fotos)


@app.route("/deletar_foto/<int:foto_id>", methods=["POST"])
@login_required
def deletar_foto(foto_id):
    # Busca a foto no banco de dados
    foto = Foto.query.get_or_404(foto_id)

    # Verifica se a foto pertence ao usuário logado
    if foto.id_usuario != current_user.id:
        return redirect(url_for("feed"))

    # Caminho absoluto da foto
    caminho_foto = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        app.config["UPLOAD_FOLDER"],
        foto.imagem
    )

    # Deleta o arquivo físico se existir
    if os.path.exists(caminho_foto):
        os.remove(caminho_foto)

    # Deleta do banco de dados
    database.session.delete(foto)
    database.session.commit()

    return redirect(url_for("feed"))
