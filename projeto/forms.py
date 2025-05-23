# ********** ARQUIVO DE CRIAÇÃO DOS FORMULARIOS **********

#  FlaskForm - para criar formulario
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField
from wtforms.validators import DataRequired,Length,Email,EqualTo ,ValidationError
from projeto.models import Usuario
from sqlalchemy import or_
from projeto import bcrypt


class CriarConta(FlaskForm):
    usuario = StringField('Usuário',validators=[DataRequired()])
    email = StringField('E-mail',validators=[DataRequired(),Email()])
    senha = PasswordField('Senha',validators=[DataRequired(),Length(6,20)])
    confirmacao_senha = PasswordField('Confirmação da Senha',validators=[DataRequired(),EqualTo('senha')])
    botao_submit = SubmitField('Criar Conta')

    # Este método precisa começar com o prefixo 'validate_' para o 'validate_on_submit()' verificar automatico e 
    # funcionar como um validador, pois esse é o padrão sugerido.
    # Ele verifica se o e-mail fornecido já está em uso. 
    # Caso esteja, lança uma exceção utilizando 'raise' da classe 'ValidationError'.

    def validate_usuario(self, usuario):
        usuario_lower = str(usuario.data).lower()
        usuario_sugerido = Usuario.query.filter_by(username=usuario_lower).first()
        if usuario_sugerido:
            raise ValidationError('Nome não disponível. Tente outro.')
   
    # Para funcionar precisa lembra de instalar pip install email-validator
    def validate_email(self, email):
        email_sugerido = Usuario.query.filter_by(email=email.data).first()
        if email_sugerido:
            raise ValidationError('E-mail já cadastrado. Cadastre-se com outro e-mail ou faça login para continuar.')
   
  


class FazerLogin(FlaskForm):
    # Fazer login tanto com usuario ou email
    identificador = StringField('Usuário ou E-mail', validators=[DataRequired()])
    senha = PasswordField('Senha',validators=[DataRequired(),Length(6,20)])
    botao_submit = SubmitField('Login')

    
    def validate_identificador(self, identificador):

        usuario_recuperado = str(identificador.data).lower()
        # Verifica se o identificador (e-mail ou usuário) existe no banco de dados
        usuario = Usuario.query.filter(
            (Usuario.email == identificador.data) | (Usuario.username == usuario_recuperado)
        ).first()

        if not usuario:
            raise ValidationError('E-mail ou usuário não encontrado.')
  

class FormFoto(FlaskForm):
    foto = FileField('foto', validators=[DataRequired()])# caminho do arquivo
    botao_submit = SubmitField('Enviar')

    
    