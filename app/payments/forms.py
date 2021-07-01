from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField
from wtforms import validators as v

class BuyForm(FlaskForm):
    quantity = StringField('Quantity', validators=[
        v.DataRequired(message=None),
    ])
    sizes = StringField('Sizes', validators=[
        v.DataRequired(message=None),
    ])
    firstname = StringField('First Name', validators=[
        v.DataRequired(message=None),
    ])
    lastname = StringField('Last Name', validators=[
        v.DataRequired(message=None),
    ])
    email = StringField('Email', validators=[
        v.DataRequired(message=None), 
        v.Email(message=('Invalid email')),
    ])
    street = StringField('Street', validators=[
        v.DataRequired(message=None),
    ])
    country = StringField('Country', validators=[
        v.DataRequired(message=None),
    ])
    country = StringField('Country', validators=[
        v.DataRequired(message=None),
    ])
    state = StringField('State', validators=[
        v.DataRequired(message=None),
    ])
    city = StringField('City', validators=[
        v.DataRequired(message=None),
    ])
    postcode = IntegerField('Postcode', validators=[
        v.DataRequired(message=None),
    ])
    submit = SubmitField('Create')

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