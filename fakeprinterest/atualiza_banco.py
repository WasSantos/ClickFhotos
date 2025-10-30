from fakeprinterest import database
from fakeprinterest.models import Foto

# Adiciona a coluna 'descricao' se não existir
if not hasattr(Foto, 'descricao'):
    database.engine.execute('ALTER TABLE foto ADD COLUMN descricao VARCHAR(200)')
    print("Coluna 'descricao' adicionada com sucesso!")
else:
    print("Coluna 'descricao' já existe.")
