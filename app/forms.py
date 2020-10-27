from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, SelectMultipleField, TextAreaField, IntegerField
from wtforms.validators import DataRequired

class AccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Add')



class BaseForm(FlaskForm):
	accounts = SelectMultipleField(u'Accounts')
	amount = IntegerField('amout', default=0)
	delay = IntegerField('delay', default=60)
	randomize = BooleanField()
	submit = SubmitField('run')

class Follow_by_tag_Form(BaseForm):
	tags = TextAreaField('tags')