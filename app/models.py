from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from markdown import markdown
import bleach
from . import login_manager
from flask.ext.login import UserMixin


class User(UserMixin, db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), unique=True, index=True)
	password_hash = db.Column(db.String(128))

	@property
	def password(self):
	    raise AttributeError('password is not a readable attribute')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash,password)

	def __repr__(self):
		return '<User %r>' % self.username

class Post(db.Model):
	__tablename__ = 'posts'
	id = db.Column(db.Integer, primary_key=True)
	title=db.Column(db.Text)
	timestamp = db.Column(db.DateTime, index=True, default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
	body = db.Column(db.Text)
	body_html = db.Column(db.Text)
	summary = db.Column(db.Text)
	summary_html = db.Column(db.Text)

	@staticmethod
	def on_changed_body(target, value, oldvalue, initiator):
		allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i',
						'li', 'ol','pre', 'strong', 'ul', 'h1', 'h2', 'h3', 'p', 'img']
		attrs = { 
			'*': ['class'], 
			'a': ['href', 'rel'], 
			'img': ['src', 'alt']
			}
		target.body_html = bleach.linkify(bleach.clean(
			markdown(value, output_format='html'),
			tags=allowed_tags, attributes=attrs, strip=True))

	@staticmethod
	def on_changed_summary(target, value, oldvalue, initiator):
		allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i',
						'li', 'ol','pre', 'strong', 'ul', 'h1', 'h2', 'h3', 'p', 'img']
		attrs = { 
			'*': ['class'], 
			'a': ['href', 'rel'], 
			'img': ['src', 'alt']
			}
		target.summary_html = bleach.linkify(bleach.clean(
			markdown(value, output_format='html'),
			tags=allowed_tags, attributes=attrs, strip=True))

db.event.listen(Post.body, 'set', Post.on_changed_body)
db.event.listen(Post.summary, 'set', Post.on_changed_summary)