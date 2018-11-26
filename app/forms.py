from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User


#HANDLES LOGIN WEBPAGE INPUT AND VERIFICATION
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


#HANDLES REGISTRATION PAGE INPUT AND VERIFICATION
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    #AVOID DUPILCATE USERS
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    #AVOID DUPLICATE EMAILS
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


#HANDLES INPUT FROM FIND MOVIES WEBPAGE
class SearchForm(FlaskForm):
    genre = StringField('Genre', validators=[])
    actor = StringField('Actor/Actress', validators=[])
    rating = StringField('Above Rating', validators=[])
    director = StringField('Director', validators=[])

    submit = SubmitField('Search')


#DISPLAYS RESULTS
class ResultsForm(FlaskForm):
    #PLACEHOLDER -- DELETE THIS
    username = 'a'

