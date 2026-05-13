from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    TextAreaField,
    DateTimeField,
    SelectField,
    IntegerField,
)
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_wtf.file import FileField, FileAllowed


class RegistrationForm(FlaskForm):
    username = StringField(
        "Имя пользователя", validators=[DataRequired(), Length(min=3, max=80)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Подтвердите пароль", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Зарегистрироваться")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    submit = SubmitField("Войти")


class EventForm(FlaskForm):
    title = StringField("Название события", validators=[DataRequired()])
    description = TextAreaField("Описание", validators=[DataRequired()])

    # Календарь с выбором даты и времени
    date = DateTimeField(
        "Дата и время",
        format="%Y-%m-%dT%H:%M",
        validators=[DataRequired()],
        render_kw={"type": "datetime-local"},
    )

    location = StringField("Место проведения", validators=[DataRequired()])
    category = SelectField(
        "Категория",
        choices=[
            ("meetup", "Встреча"),
            ("sport", "Спорт"),
            ("game", "Игры"),
            ("study", "Обучение"),
            ("party", "Вечеринка"),
            ("other", "Другое"),
        ],
    )
    image = FileField(
        "Изображение", validators=[FileAllowed(["jpg", "png", "jpeg", "gif"])]
    )
    submit = SubmitField("Создать событие")


class EventRegistrationForm(FlaskForm):
    full_name = StringField("ФИО", validators=[DataRequired()])
    age = IntegerField("Возраст", validators=[DataRequired()])
    submit = SubmitField("Зарегистрироваться на событие")
