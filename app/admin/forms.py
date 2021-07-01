from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import validators as v

class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[
        v.DataRequired(), 
        v.Email(message=('Not a valid email address.')),
    ],
    render_kw={
        "label":"Provide Email"
    })
    password = PasswordField('Password',validators=[
        v.DataRequired(),
        v.Length(min=6, max=10),
        v.EqualTo('repeatpassword', message='Passwords must match'),
    ],
    render_kw={
        "label":"Set Password"
    })
    repeatpassword = PasswordField('Repeat Password')
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        v.DataRequired(), 
        v.Email(message=('Not a valid email address.'))
    ],
    render_kw={
        "label":"Account Email"
    })
    password = PasswordField('Password', validators=[v.DataRequired()],
    render_kw={
        "label":"Password"
    })
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')