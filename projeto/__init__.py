# **********ARQUIVO DE INICIALIZAÇÃO DO MEU PROJETO**********

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
import logging
import secrets

# Configuração de logs
'''
Controle de Nível : Permite categorizar mensagens por gravidade, como:

DEBUG: Para mensagens enviadas, usadas durante o desenvolvimento.
INFO: Para mensagens informativas, como notificações de que algo foi concluído com sucesso.
WARNING: Para avisos de possíveis problemas.
ERROR: Para erros que impedem a execução de uma funcionalidade.
CRITICAL: Para falhas graves que comprometem a aplicação.

'''
logging.basicConfig(level=logging.INFO) # Define o nível de detalhe (INFO e superiores)
logger = logging.getLogger(__name__) # Cria um logger específico para o módulo atual


# Inicializando o aplicativo Flask
app = Flask(__name__)
app.config['SECRET_KEY'] ='df0d7fb5941ebf58ddfbf746575a630389c45eb3' 
# logger.info(secrets.token_hex(20))

# Configuração do banco de dados
if os.getenv('DATABASE_URL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')  # Banco de dados no servidor
    logger.info("Banco de dados configurado para produção.")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bancoDB.db'  # Banco de dados local
    logger.info("Banco de dados configurado para desenvolvimento local.")


# Inicializando extensões
database = SQLAlchemy(app)  # Instância do banco de dados
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
# dizer qual pagina irar gerenciar o meu login
login_manager.login_view = 'home'

# Função para verificar e inicializar o banco de dados
def verificar_banco():
    engine = sqlalchemy.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    inspector = sqlalchemy.inspect(engine)

    # Verifica se a tabela "usuario" existe
    if not inspector.has_table("usuario"):
        with app.app_context():
            database.create_all()
            logger.info("Banco de dados criado com as tabelas necessárias.")
    else:
        logger.info("Banco de dados já existe.")

# Executa a verificação do banco de dados
verificar_banco()

# Importando rotas e modelos
from projeto import models
from projeto import routes



