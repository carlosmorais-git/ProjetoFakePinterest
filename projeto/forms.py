# ********** ARQUIVO DE CRIAÇÃO DOS FORMULARIOS **********

#  FlaskForm - para criar formulario
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField
from wtforms.validators import DataRequired,Length,Email,EqualTo ,ValidationError
from projeto.models import Usuario


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

    # Para funcionar precisa lembra de instalar pip install email-validator
    def validate_email(self, email):
        email_sugerido = Usuario.query.filter_by(email=email.data).first()
        if email_sugerido:
            raise ValidationError('E-mail já cadastrado. Cadastre-se com outro e-mail ou faça login para continuar.')
   
    def validate_user(self, usuario):
        usuario_sugerido = Usuario.query.filter_by(usuario=usuario.data).first()
        if usuario_sugerido:
            raise ValidationError('Nome não disponível. Tente outro.')
   

class FazerLogin(FlaskForm):
    # Fazer login tanto com usuario ou email
    identificador = StringField('Usuário ou E-mail', validators=[DataRequired()])
    senha = PasswordField('Senha',validators=[DataRequired(),Length(6,20)])
    botao_submit = SubmitField('Login')


class FormFoto(FlaskForm):
    foto = FileField('foto', validators=[DataRequired()])# caminho do arquivo
    botao_submit = SubmitField('Enviar')