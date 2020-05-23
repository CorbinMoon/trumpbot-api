from wtforms import Form, StringField, PasswordField, validators


class RegistrationForm(Form):
    username = StringField('username', [
        validators.Length(min=8, max=25)
    ])
    password = PasswordField('password', [
        validators.data_required(),
        validators.Length(min=10)
    ])
