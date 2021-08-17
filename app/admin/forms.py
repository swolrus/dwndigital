from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, BooleanField, SubmitField, BooleanField, SelectField
from flask_wtf.file import FileField, FileRequired
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

class SetItemForm(FlaskForm):
    ref = StringField('Reference', 
    validators=[
        v.DataRequired(message=None),
    ])
    name = StringField('Name',
    validators=[
        v.DataRequired(message=None),
    ])
    description = StringField('Description', 
    validators=[
        v.DataRequired(message=None),
    ])
    img = FileField('Photo', 
    validators=[
        FileRequired('File was empty!')
    ])
    price = IntegerField('Price', 
    validators=[
        v.DataRequired(message=None),
    ])
    active = BooleanField('Active?')
    submit = SubmitField('Create')

class DeleteItemForm(FlaskForm):
    name = SelectField('Items', validators=[
        v.DataRequired(message="Required field")
    ],
    choices=[],
    render_kw={
        "label":"Activate/Deactivate or Delete"
    })
    activate = SubmitField('Activate')
    deactivate = SubmitField('Deactivate')
    delete = SubmitField('Delete')