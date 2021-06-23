from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms import validators as v

class SetItemForm(FlaskForm):
    name = StringField('Name', [
        v.DataRequired(),
    ])
    price = IntegerField('Price', [
        v.DataRequired(),
    ])
    displayname = StringField('Display Name', [
        v.DataRequired(),
    ])
    description = StringField('Description', [
        v.DataRequired(),
    ])
    submit = SubmitField('Create')