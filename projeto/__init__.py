# ********** ARQUIVO DE INICIALIZAÇÃO DO MEU PROJETO **********

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
import logging
import secrets
import sqlalchemy


# ---------------------- Configuração de Logs ----------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------------- Inicializando o Flask ----------------------

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ce4a8b123dc22d762d3086ffe953071a'
CAMINHO_DIR = os.path.abspath(os.path.dirname(__file__)) 
app.config['UPLOAD_FOLDER'] = os.path.join(CAMINHO_DIR,'static', 'fotos_posts')

# ---------------------- Gerenciar pasta 'instance' ----------------------
caminho_dir = os.path.abspath(os.path.dirname('main.py'))
pasta_instance = os.path.join(caminho_dir, 'instance')
if not os.path.exists(pasta_instance):
    os.makedirs(pasta_instance)

# ---------------------- Configuração do Banco ----------------------
if os.getenv('DATABASE_URL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    logger.info("Banco de dados configurado para produção.")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(pasta_instance, 'bancoDB.db')}"
    logger.info("Banco de dados configurado para desenvolvimento local.")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # evita warning do SQLAlchemy

# ---------------------- Inicialização das Extensões ----------------------
database = SQLAlchemy(app)
migrate = Migrate(app, database)  # Integração do Flask-Migrate
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'home'

# ---------------------- Verificar se o banco existe (desnecessário com Migrate, mas útil) ----------------------
def verificar_banco():
    engine = sqlalchemy.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    inspector = sqlalchemy.inspect(engine)

    with app.app_context():
        if not inspector.has_table("usuario"):
            database.create_all()
            logger.info("Banco de dados criado com as tabelas necessárias.")
        else:
            logger.info("Banco de dados já existe.")

# ---------------------- Importações finais ----------------------
from projeto import models
from projeto import routes

verificar_banco()
