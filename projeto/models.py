# **********ARQUIVO DE CRIAÇÃO DOS MODELOS DE BANCO DE DADOS**********

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
    username =database.Column(database.String,nullable=False) 
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