from app import app
from flask import Flask, render_template, flash, redirect, url_for, request, send_from_directory
from app.forms import LoginForm
from flask_login import current_user, login_user
from flask_login import logout_user
from flask_login import login_required
from app.models import User, Task, AwardRequest
from app import db
from app.forms import RegistrationForm, SendRequestForm
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from app.tasksSpecified import getTasks
from flask import jsonify
from flask_uploads import UploadSet, configure_uploads, IMAGES
import os


@app.route('/', methods=['POST', 'GET'])
@app.route('/tasks', methods=['POST', 'GET'])
@login_required
def index():
	form = SendRequestForm()
	return render_template('new_home.html', form=form)


@app.route('/profile')
@login_required
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
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@login_required
@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

@app.route('/tasksSpecified', methods=['POST', 'GET'])
@login_required
def gettasks():
	return jsonify(getTasks(request.form['type']))
@login_required
@app.route('/rating')
def rating():
	return render_template('rating.html')

@login_required
@app.route('/tournament')
def tournament():
	return render_template('tournament.html')

@app.route('/godspanel')
def panel():
	requests = AwardRequest.query.all()
	awards = Task.query.all()
	return render_template('godspanel.html', requests=requests, awards=awards)

#upload photos/videos

@app.route('/upload', methods=['POST', 'GET'])
def upload():
	if request.method == 'POST':
		required_award = request.form.get('award_title')
		files = request.files.getlist("file")
		files_names = ''
		for f in files:
			filename = secure_filename(f.filename)
			files_names += filename + '/'
			f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		files_names = files_names[0:-1]
		award_request = AwardRequest(
			message=request.form.get('message'),
			user_id=current_user.id,
			file_name=files_names,
			required_award=required_award)
		db.session.add(award_request)
		db.session.commit()
		return redirect(url_for('index'))
	return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('static/img', filename)