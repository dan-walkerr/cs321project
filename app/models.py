from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask_login import UserMixin


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


#USE THIS TO STORE USERS FOR NEWSCENE
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    preferences = db.relationship('Preference', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

#STORES PREFERENCES FOR EACH USER
class Preference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String(140))
    actor = db.Column(db.String(140))
    rating = db.Column(db.String(140))
    director = db.Column(db.String(140))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Preference {}>'.format(self.body)

