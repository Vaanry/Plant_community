from flask_wtf import FlaskForm
from wtforms import (
    EmailField,
    PasswordField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, EqualTo, Length


class UserForm(FlaskForm):
    username = StringField(
        "Имя пользователя",
        validators=[DataRequired(message="Обязательное поле"), Length(3, 20)],
    )
    email = EmailField("Введите email")
    password = PasswordField(
        "Введите пароль",
        validators=[DataRequired(message="Обязательное поле"), Length(6, 20)],
    )

    confirmPassword = PasswordField(
        "Повторите пароль",
        validators=[
            DataRequired(message="Обязательное поле"),
            EqualTo("password", message="Пароли должны совпадать"),
        ],
    )
    submit = SubmitField("Регистрация")


class LoginForm(FlaskForm):
    username = StringField("Имя пользователя")
    password = PasswordField("Введите пароль")
    submit = SubmitField("Войти")


class PrivateMessageForm(FlaskForm):
    text = TextAreaField("Введите ваше сообщение")
    submit = SubmitField("Отправить")


class CommentForm(FlaskForm):
    text = TextAreaField("Введите ваше сообщение")
    submit = SubmitField("Отправить")


class CSRFForm(FlaskForm):
    pass
