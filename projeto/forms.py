# ********** ARQUIVO DE CRIAÇÃO DOS FORMULARIOS **********

#  FlaskForm - para criar formulario
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired,Length,Email,EqualTo ,ValidationError
from projeto.models import Usuario


class CriarConta(FlaskForm):
    usuario = StringField('Usuário',validators=[DataRequired()])
    email = StringField('E-mail',validators=[DataRequired(),Email()])
    senha = PasswordField('Senha',validators=[DataRequired(),Length(6,20)])
    confirmacao_senha = PasswordField('Confirmação da Senha',validators=[DataRequired(),EqualTo('senha')])
    botao_submit = SubmitField('Criar Conta')


    # Ele verifica se o usuario fornecido já está em uso. 
    # Caso esteja, lança uma exceção utilizando 'raise' da classe 'ValidationError'.
    def validate_usuario(self, usuario):
        usuario_sugerido = Usuario.query.filter_by(email=usuario.data).first()
        if usuario_sugerido:
            raise ValidationError('Usuario não disponível.')

    # Este método precisa começar com o prefixo 'validate_' para o 'validate_on_submit()' verificar automatico e 
    # funcionar como um validador, pois esse é o padrão sugerido.
    # Ele verifica se o e-mail fornecido já está em uso. 
    # Caso esteja, lança uma exceção utilizando 'raise' da classe 'ValidationError'.

    def validate_email(self, email):
        email_sugerido = Usuario.query.filter_by(email=email.data).first()
        if email_sugerido:
            raise ValidationError('E-mail já cadastrado. Cadastre-se com outro e-mail ou faça login para continuar.')
   


class FazerLogin(FlaskForm):
    usuario = StringField('Usuário',validators=[DataRequired()])
    email = StringField('E-mail',validators=[DataRequired(),Email()])
    senha = PasswordField('Senha',validators=[DataRequired(),Length(6,20)])
    botao_submit = SubmitField('Login')