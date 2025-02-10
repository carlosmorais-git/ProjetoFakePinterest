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
app.config['SECRET_KEY'] = 'ce4a8b123dc22d762d3086ffe953071a'

# # Define a pasta de uploads, verificando primeiro se há uma variável de ambiente
# # Se a variável UPLOAD_FOLDER estiver definida, usa esse valor
# # Caso contrário, usa "static/fotos_posts" como padrão

# UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/fotos_posts"))

# # Garante que a pasta de uploads existe no ambiente de produção e local
# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = "static/fotos_posts"



'''Configuração da Pasta 'instance' criada automaticamente.'''

caminho_dir = os.path.abspath(os.path.dirname('main.py'))  # Caminho do diretório main
pasta_instance = os.path.join(caminho_dir, 'instance')  # Caminho completo para 'instance'

# Verifica se a pasta 'instance' existe
if not os.path.exists(pasta_instance):
    os.makedirs(pasta_instance)  # Cria a pasta


# Configuração do banco de dados
if os.getenv('DATABASE_URL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')  # Banco de dados no servidor
    logger.info("Banco de dados configurado para produção.")
else:
 
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(caminho_dir, 'instance', 'bancoDB.db')}"
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bancoDB.db'  # Banco de dados local
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

    with app.app_context():
        if not inspector.has_table("usuario"):
            database.create_all()  # Cria as tabelas
            logger.info("Banco de dados criado com as tabelas necessárias.")
        else:
            logger.info("Banco de dados já existe.")



# Importando rotas e modelos
from projeto import models
from projeto import routes

# Executa a verificação do banco de dados
verificar_banco()




