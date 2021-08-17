from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms import validators as v

class BuyForm(FlaskForm):
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
    submit = SubmitField('To Payment')