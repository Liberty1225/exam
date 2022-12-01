from app import app
from flask_wtf import FlaskForm
import wtforms as ws
from .models import *


class UserForm(FlaskForm):
    username = ws.StringField('Имя пользователя', validators=[
        ws.validators.DataRequired(),
        ws.validators.Length(min=4, max=20)
    ])
    password = ws.PasswordField('Пароль', validators=[
        ws.validators.DataRequired(),
        ws.validators.Length(min=8)
    ])


class EmployeeForm(FlaskForm):
    fullname = ws.StringField('ФИО', validators=[ws.validators.DataRequired()])
    phone_number = ws.StringField('Номер телефона', validators=[
        ws.validators.DataRequired(),
        ws.validators.Length(min=13, max=13, message="Номер телефона состоит из 13 значений"),
    ])
    short_info = ws.TextAreaField('Краткая информация', validators=[ws.validators.DataRequired()])
    experience = ws.IntegerField('Опыт работы', validators=[ws.validators.DataRequired()])
    preferred_position = ws.StringField('Предпочитаемая позиция', validators=[ws.validators.DataRequired()])
    user_id = ws.SelectField('Пользователь', choices=[])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username_choices = []
        with app.app_context():
            for username in User.query.all():
                self.username_choices.append((username.id, username.username))
        self._fields['user_id'].choices = self.username_choices

    def validate(self):
        if not super().validate():
            return False

        error_counter = 0

        def check_fullname(fullname):
            for i in fullname.replace(" ", ""):
                if not i.isalpha():
                    if i == " ":
                        continue
                    return True
            return False

        if check_fullname(self.fullname.data):
            self.fullname.errors.append("ФИО может состоять только из букв и пробела")
            error_counter += 1

        if error_counter == 0:
            return True
        else:
            return False
