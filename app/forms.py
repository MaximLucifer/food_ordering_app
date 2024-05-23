from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FloatField, TextAreaField, IntegerField, FileField, DecimalField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileAllowed
from app.models import User
from flask_login import current_user

class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Подтвердите пароль', validators=[DataRequired(), EqualTo('password')])
    role = StringField('Роль (пользователь/админ)', default='пользователь')  # Add role field
    submit = SubmitField('Регистрация')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Это имя пользователя занято. Пожалуйста, выберите другое.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Этот Email занят. Пожалуйста, введиет другой.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class UpdateAccountForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Обновить фотографию профиля', validators=[FileAllowed(['jpg', 'png', 'avif', 'gif'])])
    submit = SubmitField('Обновить')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Это имя пользователя занято. Пожалуйста, выберите другое.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Этот Email занят. Пожалуйста, введите другой.')

class MenuItemForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    price = FloatField('Цена', validators=[DataRequired()])
    description = TextAreaField('Описание')
    picture = FileField('Установить фотографию', validators=[FileAllowed(['jpg', 'png', 'avif'])])
    submit = SubmitField('Добавить')

class OrderForm(FlaskForm):
    menu_item_id = IntegerField('ID меню', validators=[DataRequired()])
    quantity = IntegerField('Количество', validators=[DataRequired()])
    submit = SubmitField('Заказать')