from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField
from wtforms import validators as v

class SetItemForm(FlaskForm):
    name = StringField('Name', [
        v.DataRequired(),
    ])
    description = StringField('Description', validators=[
        v.DataRequired(),
    ])
    img = FileField('Photo', validators=[FileRequired('File was empty!')])
    price = IntegerField('Price', validators=[
        v.DataRequired(),
    ])
    submit = SubmitField('Create')

class DeleteItemForm(FlaskForm):
    name = SelectField('Item to delete', choices=[])
    submit = SubmitField('Delete')

class PurchaseItemForm(FlaskForm):
    name = StringField('Name', validators=[
        v.DataRequired(),
    ])
    email = IntegerField('Email', validators=[
        v.DataRequired(),
    ])
    displayname = StringField('Display Name', validators=[
        v.DataRequired(),
    ])
    description = StringField('Description', validators=[
        v.DataRequired(),
    ])
    submit = SubmitField('Create')