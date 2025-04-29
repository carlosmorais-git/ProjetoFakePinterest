# **********ARQUIVO DE CRIAÇÃO PARA ROTAS DAS PAGINAS**********

from flask import render_template,url_for,flash,redirect,request,abort,jsonify,current_app
from projeto import app,bcrypt,database,logger
from sqlalchemy import or_
from flask_login import login_required,login_user,logout_user,current_user
from projeto.forms import CriarConta,FazerLogin,FormFoto
from projeto.models import Usuario, Foto,Salvo
import os
from werkzeug.utils import secure_filename
import random
from datetime import datetime
from PIL import Image
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



def salvar_imagem_upload(foto, pasta_upload_base, usuario_id):
    # Cria a subpasta se não existir
    pasta_usuario = os.path.join(pasta_upload_base, f"usuario_{usuario_id}")
    os.makedirs(pasta_usuario, exist_ok=True)  # cria a pasta se ainda não existe

    # Nome original seguro
    nome_original = secure_filename(foto.filename)

    # Se o nome estiver vazio, gera um nome padrão
    #.strftime('%Y%m%d%H%M%S') gera um timestamp para evitar duplicidade
    if not nome_original:
        nome_original = f"imagem_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"

    # Separa extensão
    #.splitext() separa o nome do arquivo da extensão
    nome_base, extensao = os.path.splitext(nome_original)
    extensao = extensao.lower()

    # Extensões permitidas
    extensoes_validas = ['.jpg', '.jpeg', '.png', '.gif', '.webp']

    # Se a extensão for suspeita tipo .jfif, .jiff, etc, corrige para .jpg
    # Converter para .jpg é mais seguro e compatível com a maioria dos navegadores
    if extensao not in extensoes_validas:
        extensao = '.jpg'

    # Gera nome único
    nome_seguro = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{usuario_id}{extensao}"

    # Caminho final
    caminho_final = os.path.join(pasta_usuario, nome_seguro)

    # Salvar imagem (com conversão se necessário)
    try:
        img = Image.open(foto)
        img.convert('RGB').save(caminho_final, format='JPEG')  # Sempre salva como JPEG para padronizar
    except Exception as e:
        print("Erro ao processar imagem:", e)
        # Se der erro ao abrir com PIL, salva bruto mesmo
        foto.save(caminho_final)

    # Retorna o caminho relativo para salvar no banco de dados
    caminho_relativo = os.path.join(f"usuario_{usuario_id}", nome_seguro).replace("\\", "/")  # Substitui as barras invertidas por barras normais para compatibilidade com URLs

    return caminho_relativo


    

# -------Rotas-------
@app.route('/',methods=['GET','POST'])
def home():

    # Verifica se o usuário já está autenticado. Se sim, redireciona para a página de perfil.
    if current_user.is_authenticated:
        return redirect(url_for('perfil', field=current_user.id))  # ou outro identificador

    # criando uma instancia do formulario Login
    formulario = FazerLogin()

    if formulario.validate_on_submit():
        # valor passado usuario ou email
        identificador = formulario.identificador.data
        # Usuario recuperado com letra minuscula
        identificador_recuperado = str(identificador).lower()
        usuario = None
        # Procurando o usuário pelo identificador (email ou username)
        # Para verificar se é email ou username, faço isso com único filter() usando 'or_' do SQLAlchemy. 
        usuario = Usuario.query.filter(
            or_(Usuario.email == identificador, Usuario.username == identificador_recuperado)
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
    # Criando uma instancia do formulario Criar Conta
    formulario = CriarConta()

    if formulario.validate_on_submit():
        # Criptografando minha senha e passa o '.decode('utf-8')' para funcionar em producao
        senha_criptrografada = bcrypt.generate_password_hash(formulario.senha.data).decode('utf-8')

        # Criar um usuário e adicionar no banco de dados
        # Convertendo o nome de usuário para minúsculas
        name = str(formulario.usuario.data).lower()
        usuario = Usuario(username=name,
                          email=formulario.email.data,
                          senha=senha_criptrografada)
        database.session.add(usuario)

        # salvo o novo usuario no banco de dados
        database.session.commit()

        # Logando no site após ser criado com sucesso
        # Remember=True pare lembrar que o usuario está logado
        login_user(usuario,remember=True)
        return redirect(url_for("perfil",field=usuario.id))

    return render_template('paginas/criar_conta.html',titulo='Criar Conta',formulario=formulario)

@app.route('/perfil/<field>', methods=['GET', 'POST'])
@login_required
def perfil(field):
    fotos_salvas = []    
    
    if int(field) == int(current_user.id):
        # Recupera fotos salvas se for o próprio perfil
        fotos_salvas = Salvo.query.filter_by(usuario_id=current_user.id).all()
        fotos_salvas_ids = {salvo.foto_id for salvo in fotos_salvas if salvo.ativo}
        
        formulario = FormFoto()
        # Formulario para upload de imagem
        if request.method == 'POST':
            if formulario.validate_on_submit():
                # Upload da imagem
                arquivo = formulario.foto.data
                
                caminho_relativo = salvar_imagem_upload(
                    arquivo, 
                    current_app.config['UPLOAD_FOLDER'], 
                    current_user.id
                )


                 # Salva no banco
                foto = Foto(imagem=caminho_relativo, id_usuario=current_user.id)
                database.session.add(foto)
                database.session.commit()

                # Responder Ajax se for requisição Ajax
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    url_imagem = url_for('static', filename=f"fotos_posts/{caminho_relativo}")
                    
                    return jsonify({"imagem": url_imagem})

                # Se não for Ajax, redireciona normal
                return redirect(url_for('perfil', field=current_user.id))

            else:
                # Se NÃO validou, mas é Ajax, tem que retornar erro!
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return jsonify({"erro": "Erro ao enviar foto."}), 400

        # Se for GET ou depois do POST
        return render_template('paginas/perfil.html',
                               titulo='Meu Perfil',
                               usuario=current_user,
                               formulario=formulario,
                               fotos_salvas=fotos_salvas,
                               fotos_salvas_ids=fotos_salvas_ids)

    else:
        # Visitando perfil de outro usuário (apenas leitura)
        field = Usuario.query.get(int(field))
        # verficar se o usuario que visita o perfil tem fotos ja salvas
        if field is None:
            # Se o usuário não existir, retorna 404
            abort(404)
        # Verifica se o usuário está autenticado e tem fotos salvas
        if current_user.is_authenticated:
            fotos_salvas = Salvo.query.filter_by(usuario_id=current_user.id).all()
            fotos_salvas_ids = {salvo.foto_id for salvo in fotos_salvas if salvo.ativo}
        else:
            fotos_salvas = []
            fotos_salvas_ids = set()
        # Renderiza o perfil do usuário

        return render_template('paginas/perfil.html',
                               titulo='Meu Perfil',
                               usuario=field,
                               fotos_salvas=fotos_salvas,
                               fotos_salvas_ids=fotos_salvas_ids,
                               formulario=None)

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
    fotos = Foto.query.order_by(Foto.data_criacao.desc()).all()
    fotos = random.sample(fotos, min(50, len(fotos)))  # Limita a 50 fotos aleatórias
    return render_template('paginas/feed.html',fotos=fotos)



@app.route('/foto/<int:field>/excluir', methods=["GET", "POST"])
@login_required# bloqueia a pagina caso nao faço login
def excluir_foto(field):
    foto = Foto.query.get_or_404(field)    

    # se sou o dono da foto posso excluir
    if current_user == foto.autor:
        try:
            # Caminho da imagem
            UPLOAD_FOLDER = current_app.config['UPLOAD_FOLDER']
        
            print(UPLOAD_FOLDER)
            caminho_imagem = os.path.join(UPLOAD_FOLDER, foto.imagem)
            

            # Primeiro tenta remover o arquivo
            if os.path.exists(caminho_imagem):
                os.remove(caminho_imagem)
                print(f"Arquivo {caminho_imagem} removido com sucesso!")
            else:
                print(f"Arquivo {caminho_imagem} não encontrado para exclusão.")

            # Agora sim deleta do banco
            database.session.delete(foto)
            database.session.commit()

            return jsonify({"status": "danger", "mensagem": "Foto Excluída"})

        except Exception as e:
            database.session.rollback()
            print(f"Erro ao excluir foto: {e}")
            return jsonify({"status": "danger", "mensagem": "Erro ao excluir a foto."})





@app.route('/foto/<int:id>')
def ver_foto(id):
    foto = Foto.query.get_or_404(id)
    fotos_autor = Foto.query.filter(Foto.autor == foto.autor,Foto.id != foto.id).all()
    fotos_autor = random.sample(fotos_autor, min(3, len(fotos_autor)))  # Limita a 3 fotos aleatórias do autor
    


    fotos_salvas_ids = set()
    if current_user.is_authenticated:
        fotos_salvas = Salvo.query.filter_by(usuario_id=current_user.id, ativo=True).all()
        fotos_salvas_ids = {salvo.foto_id for salvo in fotos_salvas}

    return render_template('paginas/ver_foto.html', fotos_autor=fotos_autor, foto=foto, fotos_salvas_ids=fotos_salvas_ids)


@app.route('/foto-salva/<int:foto_id>')
@login_required
def ver_salvar_foto(foto_id):
    salvo = Salvo.query.filter_by(usuario_id=current_user.id, foto_id=foto_id).first_or_404()
    foto = salvo.foto
    fotos_autor = Foto.query.filter(Foto.autor == foto.autor,Foto.id != foto.id).all()
    fotos_autor = random.sample(fotos_autor, min(3, len(fotos_autor)))  # Limita a 3 fotos aleatórias do autor
    


    fotos_salvas_ids = {salvo.foto_id} if salvo.ativo else set()

    return render_template('paginas/ver_foto.html', fotos_autor=fotos_autor ,foto=foto, fotos_salvas_ids=fotos_salvas_ids)



@app.route('/foto/<int:field>/salvar', methods=['POST'])
@login_required
def salvarImagem(field):
    foto = Foto.query.get_or_404(field)

    # Verifica se já foi salva
    ja_salva = Salvo.query.filter_by(usuario_id=current_user.id, foto_id=foto.id).first()

    if ja_salva:
        if ja_salva.ativo:
            # Se estava ativa, desativa e remove do banco
            database.session.delete(ja_salva)
            database.session.commit()
            return jsonify({
                "status": "danger",
                "mensagem": "Imagem removida!",
                "ativo": False
            })
        else:
            # Se estava inativa (teoricamente não deveria estar aqui), ativa
            ja_salva.ativo = True
            database.session.commit()
            return jsonify({
                "status": "success",
                "mensagem": "Imagem salva com sucesso!",
                "ativo": True
            })

    # Nunca foi salva → salva agora
    novo_salvo = Salvo(usuario_id=current_user.id, foto_id=foto.id, ativo=True)
    database.session.add(novo_salvo)
    database.session.commit()

    return jsonify({
        "status": "success",
        "mensagem": "Imagem salva com sucesso!",
        "ativo": True
    })



@app.route("/salvo/<int:salvo_id>/remover", methods=["POST"])
@login_required
def remover_salvo(salvo_id):
    # Excuir fotos da lista de salvas
    
    salvo = Salvo.query.get_or_404(salvo_id)
    if salvo.usuario_id != current_user.id:
        return jsonify({'mensagem': "Acesso negado.", 'status': 'danger'}), 403

    database.session.delete(salvo)
    database.session.commit()
    

    return jsonify({"status": "danger", "mensagem": "Imagem removida!"})


