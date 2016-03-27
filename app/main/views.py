from flask import render_template, redirect, url_for, flash, request
from flask.ext.login import login_user, logout_user, login_required, current_user
from . import main
from .. import db, login_manager
from ..models import User,Post
from .forms import LoginForm, PostForm

POSTS_PER_PAGE = 10

@main.route('/login', methods=['GET','POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user,form.remember_me.data)
			return redirect(request.args.get('next') or url_for('main.edit'))
		flash('Invalid username or password.')
	return render_template('login.html', form=form)

@main.route('/')
def index():
	page = request.args.get('page', 1, type=int)
	pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
		page, per_page=POSTS_PER_PAGE, error_out=False)
	posts = pagination.items
	return render_template('index.html', posts=posts, pagination=pagination)

@main.route('/post/<int:id>')
def post(id):
	post = Post.query.get_or_404(id)
	return render_template('post.html', post=post)

@main.route('/logout')
@login_required
def logout():
	logout_user()
	flash('You have been logged out.')
	return redirect(url_for('main.index'))

@main.route('/write', methods=['GET', 'POST'])
@login_required
def write():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(title=form.title.data, body=form.body.data, summary=form.summary.data)
		db.session.add(post)
		flash('Success add an article!')
		return redirect(url_for('main.index'))
	return render_template('write.html',form=form)

@main.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
	page = request.args.get('page', 1, type=int)
	pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
		page, per_page=POSTS_PER_PAGE, error_out=False)
	posts = pagination.items
	return render_template('edit.html', posts=posts, pagination=pagination)

@main.route('/delete/<string:id>')
def delete(id):
	post = Post.query.filter_by(id=id).first()
	db.session.delete(post)
	db.session.commit()
	page = request.args.get('page', 1, type=int)
	pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
		page, per_page=POSTS_PER_PAGE, error_out=False)
	posts = pagination.items
	return render_template('edit.html', posts=posts, pagination=pagination)

@main.route('/editpage/<string:id>')
def editpage(id):
	post = Post.query.filter_by(id=id).first()
	return render_template('edit.html',post=post)


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))
