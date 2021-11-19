from wtforms import Form, StringField, PasswordField, validators


class RegisterForm(Form):
    name = StringField("Name", validators=[
        validators.Length(min=2, max=64),
        validators.DataRequired(message="A név mező nem lehet üres!")
    ])

    email = StringField("Email", validators=[
        validators.Email(message="Adjon meg egy érvényes email címet!")
    ])

    password = PasswordField("Password", validators=[
        validators.Length(min=8, max=128),
        validators.DataRequired(message="A jelszó mező nem lehet üres!"),
        validators.EqualTo(fieldname="confirm", message="A megadott jelszavak nem egyeznek!")
    ])

    confirm = PasswordField("Confirm Password", validators=[
        validators.Length(min=8, max=128),
        validators.DataRequired(message="A jelszó mező nem lehet üres!")
    ])


class LoginForm(Form):
    email = StringField("Email", validators=[
        validators.Length(min=7, max=50),
        validators.DataRequired(message="Az email mező nem lehet üres!"),
    ])

    password = PasswordField("Password", validators=[
        validators.DataRequired(message="A jelszó mező nem lehet üres!"),
    ])


class PropertiesForm(Form):
    name = StringField("Name", validators=[
        validators.Length(min=2, max=64),
    ])

    new_password = PasswordField("Password", validators=[
        validators.Length(min=8, max=128),
        validators.EqualTo(fieldname="new_confirm", message="A megadott jelszavak nem egyeznek!")
    ])

    new_confirm = PasswordField("Confirm Password", validators=[
        validators.Length(min=8, max=128),
    ])

    password = PasswordField("Password", validators=[
        validators.Length(min=8, max=128),
        validators.DataRequired(message="A jelszó mező nem lehet üres!"),
    ])
