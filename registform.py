from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class RegistForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    repeat = PasswordField('Повторите пароль', validators=[DataRequired()])
    mail = StringField('Почта', validators=[DataRequired()])
    user_admin = PasswordField('если вы администратор, введите код, если пользователь, введите "buy"',
                               validators=[DataRequired()])
    regist = SubmitField('Регистрация')