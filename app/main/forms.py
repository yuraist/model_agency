from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FileField, SubmitField, DateField, BooleanField
from wtforms.validators import DataRequired, Length


class AddManagerForm(FlaskForm):
    name = StringField('Имя менеджера', validators=[DataRequired(), Length(1, 64)])
    username = StringField('Никнейм', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('Пароль', validators=[DataRequired()])
    is_admin = BooleanField('Администратор', default=False)
    photo = FileField('Загрузить фото')
    submit = SubmitField('Добавить')


class AddModelForm(FlaskForm):
    full_name = StringField('ФИО', validators=[DataRequired(), Length(1, 140)])
    date_of_birth = DateField('Дата рождения', validators=[DataRequired()])
    city = StringField('Город', validators=[DataRequired(), Length(64)])
    phone = StringField('Телефон', validators=[Length(0, 14)])
    departure_date = DateField('Желаемая дата вылета')
    start_date = DateField('Дата начала работы')
    ticket_price = StringField('Цена билета')
    # club = SelectField('Клуб')
    # avatar = FileField('Загрузить аватар')
    # photos = MultipleFileField('Загрузить несколько фотографий')
    submit = SubmitField('Добавить')

    # def __init__(self, clubs=[]):
    #     self.club.choices = clubs


class AddClubForm(FlaskForm):
    name = StringField('Название клуба', validators=[DataRequired(), Length(1, 128)])
    submit = SubmitField('Добавить')
