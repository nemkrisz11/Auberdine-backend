from wtforms import Form, StringField, PasswordField, validators


class RegisterForm(Form):
    name = StringField("Name", validators=[
        validators.Length(min=2, max=64, message="A név hossza 2-64 karakter lehet!"),
        validators.DataRequired(message="A név mező nem lehet üres!")
    ])

    email = StringField("Email", validators=[
        validators.Email(message="Adjon meg egy érvényes email címet!")
    ])

    password = PasswordField("Password", validators=[
        validators.Length(min=8, max=128, message="A jelszó minimum 8 karakter hosszú kell, hogy legyen!"),
        validators.DataRequired(message="A jelszó mező nem lehet üres!"),
        validators.EqualTo(fieldname="confirm", message="A megadott jelszavak nem egyeznek!")
    ])

    confirm = PasswordField("Confirm Password", validators=[])


class LoginForm(Form):
    email = StringField("Email", validators=[
        validators.DataRequired(message="Az email mező nem lehet üres!"),
    ])

    password = PasswordField("Password", validators=[
        validators.DataRequired(message="A jelszó mező nem lehet üres!"),
    ])


class PropertiesForm(Form):
    new_name = StringField("Name", validators=[
        validators.Optional(),
        validators.Length(min=2, max=64, message="A név hossza 2-64 karakter lehet!"),
    ])

    new_password = PasswordField("Password", validators=[
        validators.Optional(),
        validators.Length(min=8, max=128, message="Az új jelszó minimum 8 karakter hosszú kell, hogy legyen!"),
        validators.EqualTo(fieldname="new_confirm", message="A megadott új jelszavak nem egyeznek!")
    ])

    new_confirm = PasswordField("Confirm Password", validators=[])

    password = PasswordField("Password", validators=[
        validators.DataRequired(message="A jelszó mező nem lehet üres!"),
    ])
