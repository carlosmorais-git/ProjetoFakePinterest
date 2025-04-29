# **********ARQUIVO DE CRIAÇÃO DOS MODELOS DE BANCO DE DADOS**********
"""
❗❗ MIGRAÇÕES COM FLASK-MIGRATE (como no Django)

Comandos principais (executar no terminal, na raiz do projeto):

1. Inicializar (só uma vez no projeto):
   flask --app projeto db init

2. Criar nova migração ao alterar models:
   flask --app projeto db migrate -m "descrição da alteração"
   ou
   flask db migrate -m "adiciona campo nome na tabela salvo"

3. Aplicar a migração ao banco:
   flask --app projeto db upgrade
   ou
   flask db upgrade

❗❗ Dica: 
- Toda vez que criar/editar um model, execute os passos 2 e 3.
- O diretório 'migrations/' guarda o histórico de alterações.
- Isso evita apagar o banco sempre que fizer mudanças.

❗❗ Recriar o banco (em dev):
- Apagar bancoDB.db e pasta migrations/
- Repetir os passos acima

"""

from projeto import database,login_manager
from datetime import datetime
# O metodo UserMixin diz qual é a classe que gerenciar a estrutura de login
from flask_login import UserMixin

# Para dizer ao login_manager que essa funcao
# carregar um usuario, verificando seu id
@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))


# database.Model é que permite que o database entendi essa classe 
class Usuario(database.Model,UserMixin):
    __tablename__ = 'usuario'
    id = database.Column(database.Integer, primary_key=True)
    username =database.Column(database.String,nullable=False,unique=True) 
    email = database.Column(database.String,nullable=False,unique=True)
    senha = database.Column(database.String,nullable=False)

    # Diz que será uma relação entre tabelas
    # CLASS - AUTOR (chave estrangeira) - lazy= melhorar desempenho do banco de dados
    fotos = database.relationship('Foto', backref='autor',lazy=True)

class Foto(database.Model):

    id = database.Column(database.Integer, primary_key=True)
    imagem = database.Column(database.String,default='default.png')
    data_criacao = database.Column(database.DateTime,nullable=False, default=datetime.now())
    # chave estrangeira ForeignKey
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'),nullable=False)


class Salvo(database.Model):
    id = database.Column(database.Integer, primary_key=True)    
    # Chave estrangeira para a tabela Usuario
    # Este campo é o id do usuario que salvou a foto
    usuario_id = database.Column(database.Integer, database.ForeignKey('usuario.id'))
    # Este campo é o id da foto que foi salva
    foto_id = database.Column(database.Integer, database.ForeignKey('foto.id'))
    foto = database.relationship('Foto', backref='salvos')
    # Ativo ou não o salvamento da foto
    ativo = database.Column(database.Boolean, default=False)

