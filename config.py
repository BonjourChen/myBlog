import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard_to_guess'
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://gdnoc:123456Qw!@localhost/myBlog'
	DEBUG = True

	@staticmethod
	def init_app(app):
		pass