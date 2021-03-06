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


class Follow_user_followers_Form(BaseForm):
	users = TextAreaField('users')


class Follow_by_list_Form(BaseForm):
	users = TextAreaField('users')


class Like_by_tag_Form(BaseForm):
	tags = TextAreaField('tags')


class Like_by_feed_Form(BaseForm):
	pass


class unfollow_by_list_Form(BaseForm):
	users = TextAreaField('users')
	unfollow_after = IntegerField('unfollow_after')



class unfollow_non_followers(BaseForm):
	unfollow_after = IntegerField('unfollow_after')


class unfollow_all(BaseForm):
	unfollow_after = IntegerField('unfollow_after')


class Comment_by_tag_Form(BaseForm):
	tags = TextAreaField('tags')
	comments = TextAreaField('comments')
	percentage = IntegerField('percentage')


class Comment_by_feed_Form(BaseForm):
	comments = TextAreaField('comments')
	percentage = IntegerField('percentage')


class accept_requests_Form(BaseForm):
	pass



