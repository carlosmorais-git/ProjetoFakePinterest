# **********ARQUIVO DE CRIAÇÃO PARA ROTAS DAS PAGINAS**********

from flask import render_template,url_for,flash,redirect,request
from projeto import app
from flask_login import login_required
from projeto.forms import CriarConta,FazerLogin

# render_template - renderiza uma pagina html para uma rota
# url_for - permite que recupero url das funcoes de maneira dinamica em vez de escreve elas assim '/caminho'
# flash - mensagem de alerta
# redirect - redirecionar para uma pagina
# login_user - loga o usuario no site
# bcrypt - usa quando for criptrografar uma senha
# logout_user - deslogar usuario
# current_user - verfica se o usuario esta autenticado e controla a exibição dele na pagina
# request - faz requisição na url da pagina

@app.route('/',methods=['GET','POST'])
def home():
    # criando uma instancia do formulario Login
    formulario = FazerLogin()
    return render_template('home.html',titulo='Pagina inicial',formulario=formulario)

@app.route('/criar-conta',methods=['GET','POST'])
def criar_conta():
    # criando uma instancia do formulario Criar Conta
    formulario = CriarConta()
    return render_template('criar_conta.html',titulo='Criar Conta',formulario=formulario)

@app.route('/perfil/<field>',methods=['GET','POST'])
@login_required  
def perfil(field):
    return render_template('perfil.html',titulo='Meu Perfil',usuario = field)
