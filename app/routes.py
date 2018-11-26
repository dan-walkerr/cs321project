from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user
from app.models import User, Preference
from flask_login import logout_user
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse
from app import db
from app.forms import RegistrationForm, SearchForm, ResultsForm


#ROUTE FOR HOME PAGE
@app.route('/')
@app.route('/index')
@login_required
def index():
    #FIX
    preferences = [
        {
            'user': {'username': 'John'},
            'body': 'Some text.'
        },
        {
            'user': {'username': 'Susan'},
            'body': 'Some more text.'
        }
    ]
    return render_template('index.html', title='Home', user=user, preferences=preferences)


#ROUTE FOR LOGIN PAGE
@app.route('/login', methods=['GET', 'POST'])
def login():
    #IF YOU'RE LOGGED IN, SENDS YOU TO HOMEPAGE
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    #VALIDATES INPUT DATA
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)


#ROUTE FOR LOGOUT MENU BUTTON
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


#ROUTE FOR REGISTRATION PAGE
@app.route('/register', methods=['GET', 'POST'])
def register():
    #IF CURRENT USER, SEND BACK TO HOME
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    #ADDS NEW USER TO DATABASE
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)


#PROFILE PAGE, NOT REALLY USED
@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()

    #CAN IGNORE THIS SHIT
    preferences = [
        {'user': user, 'body': 'Test post 1'},
        {'user': user, 'body': 'Test post 2'}
    ]
    return render_template('user.html', user=user, preferences=preferences)


#ROUTE FOR PREFERENCE SELECTION PAGE
@app.route('/user/findmovies', methods=['GET', 'POST'])
@login_required
def findmovies():
    form = SearchForm()

    #STORES USER PREFERENCES IN DATABASE
    if form.validate_on_submit():
        preference = Preference(
            genre=form.genre.data, actor=form.actor.data, rating=form.rating.data, director=form.director.data)
        db.session.add(preference)
        db.session.commit()

        return redirect(url_for('showresults'))
    return render_template('findmovies.html', user=user, form=form)


#ROUTE FOR THE RESULTS PAGE
@app.route('/user/findmovies/showresults')
@login_required
def showresults():
    form = ResultsForm()



    return render_template('showresults.html', user=user, form=form)

