from app import app
from flask import Flask, render_template, flash, redirect, url_for, request
from app.forms import LoginForm
from flask_login import current_user, login_user
from flask_login import logout_user
from flask_login import login_required
from app.models import User, Task
from app import db
from app.forms import RegistrationForm
from werkzeug.urls import url_parse
from app.tasksSpecified import getTasks
from flask import jsonify

@app.route('/')
@app.route('/tasks')
@login_required
def index():
	tasks = Task.query.all()
	return render_template('home.html',tasks=tasks)

@app.route('/profile')
def profile():
	return render_template('profile.html')

@app.route('/login',  methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect('/')
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('login')
		return redirect(next_page)
	return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('profile'))
    return render_template('register.html', title='Register', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

@app.route('/tasksSpecified', methods=['POST', 'GET'])
@login_required
def gettasks():
	return jsonify(getTasks(request.form['type']))

