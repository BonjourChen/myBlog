from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.pagedown import PageDown
from flask.ext.login import LoginManager
from config import Config
from flask.ext.bootstrap import Bootstrap

db = SQLAlchemy()
pagedown = PageDown()
login_manager = LoginManager()

def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(Config)
	Config.init_app(app)
	db.init_app(app)
	pagedown.init_app(app)
	login_manager.init_app(app)
	login_manager.session_protection = 'strong'
	login_manager.login_view = 'main.login'
	bootstrap = Bootstrap(app)

	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)
	
	return app