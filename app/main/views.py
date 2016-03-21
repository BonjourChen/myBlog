from flask import render_template, redirect, url_for, flash
from flask.ext.login import login_user, logout_user, login_required
from . import main
from .. import db
from ..models import User
from .forms import LoginForm

@main.route('/', methods=['GET','POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user,form.remember_me.data)
			return redirect(request.args.get('next') or url_for('.index'))
		flash('Invalid username or password.')
	return render_template('index.html', form=form)

@main.route('/logout')
@login_required
def logout():
	logout_user()
	flash('You have been logged out.')
	return redirect(url_for('.login'))

