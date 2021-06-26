from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import validators as v

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[
        v.DataRequired(), 
        v.Email(message=('Not a valid email address.')),
    ],)
    password = PasswordField('Password', validators=[
        v.DataRequired(),
        v.Length(min=6, max=10),
        v.EqualTo('repeatpassword', message='Passwords must match'),
    ])
    repeatpassword = PasswordField('Password')
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        v.DataRequired(), 
        v.Email(message=('Not a valid email address.'))
    ])
    password = PasswordField('Password', validators=[v.DataRequired()])
    submit = SubmitField('Sign In')