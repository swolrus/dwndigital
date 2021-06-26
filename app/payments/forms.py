from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField
from wtforms import validators as v

class SetItemForm(FlaskForm):
    ref = StringField('Reference', validators=[
        v.DataRequired(),
    ])
    name = StringField('Name', validators=[
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