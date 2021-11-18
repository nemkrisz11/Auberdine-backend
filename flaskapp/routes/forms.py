from wtforms import Form, StringField, PasswordField, validators


class RegisterForm(Form):
    name = StringField("Name", validators=[
        validators.Length(min=2, max=64),
        validators.DataRequired(message="Please fill this field!")
    ])

    email = StringField("Email", validators=[
        validators.Email(message="Please enter a valid email address!")
    ])

    password = PasswordField("Password", validators=[
        validators.Length(min=8, max=128),
        validators.DataRequired(message="Please fill this field!"),
        validators.EqualTo(fieldname="confirm", message="Mismatching passwords!")
    ])

    confirm = PasswordField("Confirm Password", validators=[
        validators.Length(min=8, max=128),
        validators.DataRequired(message="Please fill this field!")
    ])


class LoginForm(Form):
    email = StringField("Email", validators=[
        validators.Length(min=7, max=50),
        validators.DataRequired(message="Please fill this field!"),
    ])

    password = PasswordField("Password", validators=[
        validators.DataRequired(message="Please fill this field!"),
    ])


class PropertiesForm(Form):
    name = StringField("Name", validators=[
        validators.Length(min=2, max=64),
    ])

    new_password = PasswordField("Password", validators=[
        validators.Length(min=8, max=128),
        validators.EqualTo(fieldname="new_confirm", message="Mismatching passwords!")
    ])

    new_confirm = PasswordField("Confirm Password", validators=[
        validators.Length(min=8, max=128),
    ])

    password = PasswordField("Password", validators=[
        validators.Length(min=8, max=128),
        validators.DataRequired(message="Please fill this field!"),
    ])
