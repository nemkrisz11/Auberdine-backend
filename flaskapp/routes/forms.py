from wtforms import Form, StringField, PasswordField, validators


class RegisterForm(Form):
    name = StringField("Name", validators=[
        validators.Length(min=2, max=25),
        validators.DataRequired(message="Please fill this field!")
    ])

    email = StringField("Email", validators=[
        validators.Email(message="Please enter a valid email address!")
    ])

    password = PasswordField("Password", validators=[
        validators.Length(min=6, max=128),
        validators.DataRequired(message="Please fill this field!"),
        validators.EqualTo(fieldname="confirm", message="Mismatching passwords!")
    ])

    confirm = PasswordField("Confirm Password", validators=[
        validators.Length(min=6, max=128),
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
