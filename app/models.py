from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
    
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    requests = db.relationship('AwardRequest', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username) 

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), index=True)
    container = db.Column(db.String(500), index=True)
    task_type = db.Column(db.String(128), index=True)
    price = db.Column(db.Integer, index=True)

    def __repr__(self):
        return '<Task {}>'.format(self.title)
class AwardRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    required_award = db.Column(db.String(100), index=True)
    file_name = db.Column(db.String(500), index=True)
    message = db.Column(db.String(500), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __repr__(self):
        return '<UserRequest {}>'.format(self.message)