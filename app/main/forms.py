from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, PasswordField, BooleanField,TextAreaField
from wtforms.validators import Required, Length
from flask.ext.pagedown.fields import PageDownField

class LoginForm(Form):
	username = StringField('Username', validators = [Required(), Length(1,64)])
	password = PasswordField('Password', validators = [Required()])
	remember_me = BooleanField('Keep me logged in')
	submit = SubmitField('LOGIN')

class PostForm(Form):
	title=StringField("TITLE",validators=[Required()])
	body = TextAreaField("BODY", validators=[Required()])
	# body=PageDownField("BODY",validators=[Required()])
	# summary=PageDownField('SUMMARY',validators=[Required()])
	summary=TextAreaField("SUMMARY", validators=[Required()])
	category=StringField("CATEGORY",validators=[Required()])
	tags=StringField("TAGS",validators=[Required()])
	submit=SubmitField('update')