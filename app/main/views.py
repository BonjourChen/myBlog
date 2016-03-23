from flask import render_template, redirect, url_for, flash, request
from flask.ext.login import login_user, logout_user, login_required, current_user
from . import main
from .. import db, login_manager
from ..models import User
from .forms import LoginForm

@main.route('/login', methods=['GET','POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user,form.remember_me.data)
			return redirect(request.args.get('next') or url_for('main.index'))
		flash('Invalid username or password.')
	elif form.username.data is None:
		flash('Please enter a username.')
	elif form.password.data is None:
		flash('Please enter the password.')
	return render_template('login.html', form=form)

@main.route('/')
def index():
	return render_template('index.html')

@main.route('/logout')
@login_required
def logout():
	logout_user()
	flash('You have been logged out.')
	return redirect(url_for('main.index'))

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))
