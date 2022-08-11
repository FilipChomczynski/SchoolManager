from wtforms import Form, StringField, SelectField, PasswordField, validators, IntegerField


class RegistrationForm(Form):
    name = StringField('Name', [validators.Length(min=3, max=70), validators.DataRequired()])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match'),
        validators.Length(min=8, max=30)
    ])
    confirm = PasswordField('Repeat Password')


class LoginForm(Form):
    name = StringField("Name", [
        validators.DataRequired(),
        validators.Length(min=2, max=30)
    ])
    password = PasswordField("Password", [validators.DataRequired()])

class CreateTeacherForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=70), validators.DataRequired()])
    surname = StringField('Name', [validators.Length(min=1, max=70), validators.DataRequired()])
    birth_date = StringField('Birth date', [validators.DataRequired()])
    salary = IntegerField('Salary', [validators.DataRequired()])
    date_of_employment = StringField('Date of employment', [validators.DataRequired()])
    address = StringField('Address', [validators.DataRequired()])


class CreateClassForm(Form):
    choices = list()
    name = StringField('Name', [validators.DataRequired()])
    supervising_teacher = SelectField('Supervising teacher', choices=choices, validators=[validators.DataRequired()])


class CreateStudentForm(Form):
    name = StringField('Name', [validators.DataRequired()])
    surname = StringField('Surname', [validators.DataRequired()])
    birth_date = StringField('Birth date', [validators.DataRequired()])
    address = StringField('Address', [validators.DataRequired()])
    class_ = SelectField('Class', choices=[], validators=[validators.DataRequired()])
