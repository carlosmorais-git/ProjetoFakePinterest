# **********ARQUIVO DE CRIAÇÃO PARA ROTAS DAS PAGINAS**********

from flask import render_template,url_for,flash,redirect,request
from projeto import app,bcrypt,database,logger
from sqlalchemy import or_
from flask_login import login_required,login_user,logout_user,current_user
from projeto.forms import CriarConta,FazerLogin,FormFoto
from projeto.models import Usuario, Foto
import os
from werkzeug.utils import secure_filename

# render_template - renderiza uma pagina html para uma rota
# url_for - permite que recupero url das funcoes de maneira dinamica em vez de escreve elas assim '/caminho'
# flash - mensagem de alerta
# redirect - redirecionar para uma pagina
# login_user - loga o usuario no site
# bcrypt - usa quando for criptrografar uma senha
# logout_user - deslogar usuario
# current_user - verfica se o usuario esta autenticado e controla a exibição dele na pagina
# request - faz requisição na url da pagina
# werkzeug.utils - modifica um nome de arquivo para ficar seguro

@app.route('/',methods=['GET','POST'])
def home():

    # criando uma instancia do formulario Login
    formulario = FazerLogin()

    if formulario.validate_on_submit():
        # valor passado usuario ou email
        identificador = formulario.identificador.data
        usuario = None
        # Procurando o usuário pelo identificador (email ou username)
        # Para verificar se é email ou username, faço isso com único filter() usando 'or_' do SQLAlchemy. 
        usuario = Usuario.query.filter(
            or_(Usuario.email == identificador, Usuario.username == identificador)
        ).first()


        # Verificando a senha criptografada (senha do banco de dados, senha que digitei no formulario)
        # seu o email e a senha for a correta desse usuario o login será feito com sucesso
        if usuario and bcrypt.check_password_hash(usuario.senha, formulario.senha.data):
            # logando o usuario
            login_user(usuario)
            return redirect(url_for('perfil',field=usuario.id))
    # else:
    #     # Exibir os erros
    #     logger.info("Erros no formulário:", form_login.errors)

    return render_template('home.html',titulo='Pagina inicial',formulario=formulario)

@app.route('/criar-conta',methods=['GET','POST'])
def criar_conta():
    # criando uma instancia do formulario Criar Conta
    formulario = CriarConta()

    if formulario.validate_on_submit():
        # criptografando minha senha
        senha_criptrografada = bcrypt.generate_password_hash(formulario.senha.data)

        # criar um usuario e adicionar no banco
        usuario = Usuario(username=formulario.usuario.data,email=formulario.email.data,senha=senha_criptrografada)
        database.session.add(usuario)

        # salvo o novo usuario no banco de dados
        database.session.commit()

        # logando no site após ser criado com sucesso
        # remember=True pare lembrar que o usuario está logado
        login_user(usuario,remember=True)
        return redirect(url_for("perfil",field=usuario.id))

    return render_template('criar_conta.html',titulo='Criar Conta',formulario=formulario)

@app.route('/perfil/<field>',methods=['GET','POST'])
@login_required# bloqueia a pagina caso nao faço login 
def perfil(field):

    if int(field) == int(current_user.id):
        # irei passar o controle para o usuario logado
        formulario = FormFoto()
        if formulario.validate_on_submit():

            # recuperando o caminho da foto passada pelo usuario
            arquivo = formulario.foto.data

            # deixa o nome do arquivo seguro para salvar
            nome_seguro = secure_filename(arquivo.filename)

            # configuração do caminho onde irei salvar as fotos
            caminho_pasta_projeto = os.path.abspath(os.path.dirname(__file__))
            caminho = os.path.join(caminho_pasta_projeto, 
                              app.config["UPLOAD_FOLDER"], 
                              nome_seguro)
            arquivo.save(caminho)

            # salvar uma nova foto no banco de dados
            foto = Foto(imagem=nome_seguro,id_usuario=current_user.id)
            database.session.add(foto)            
            database.session.commit()
        
        return render_template('perfil.html',titulo='Meu Perfil',usuario = current_user,formulario=formulario)

    else:
        # terá permissão de só ler as fotos do perfil
        field = Usuario.query.get(int(field))
        return render_template('perfil.html',titulo='Meu Perfil',usuario = field,formulario=None)


# -------Deslogar da conta logada-------
@app.route('/sair')
@login_required# bloqueia a pagina caso nao faço login
def sair():

    # Deslogar um usuario
    logout_user()
    return redirect(url_for('home'))


# -------Feed-------
@app.route('/feed')
@login_required# bloqueia a pagina caso nao faço login
def feed():
    fotos = Foto.query.order_by(Foto.data_criacao.desc()).all()[:20]# limitar as 20 primeiras fotos
    return render_template('feed.html',fotos=fotos)