from fakeprinterest import database, app
from fakeprinterest.models import Usuario, Foto

with app.app_context():
    # Cria todas as tabelas que ainda não existem
    database.create_all()

    # Verifica se a coluna 'descricao' existe
    insp = database.inspect(database.engine)
    colunas = [c['name'] for c in insp.get_columns('foto')]

    if 'descricao' not in colunas:
        # Executa comando SQL para adicionar a coluna
        database.engine.execute("ALTER TABLE foto ADD COLUMN descricao TEXT")
        print("Coluna 'descricao' adicionada com sucesso!")
    else:
        print("Coluna 'descricao' já existe.")
