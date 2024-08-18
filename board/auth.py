from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db

auth = Blueprint('auth', __name__)
"""
Login
"""
@auth.route('/login')
def login()->str:
    """
    redirects to login page
    """
    return render_template('auth/login.html')

@auth.route('/login', methods=['POST'])
def login_post()->str:
    """
    testing the input information in the login process to redirect to the right landing page
    """
    #Taking email and passwort
    email = request.form.get('email')
    password = request.form.get('password')
    remember = request.form.get('remember', 'false').lower() == 'true'

    #Fetch the user based on the email
    user = User.query.filter_by(email=email).first()
    #Check if user exists
    if not user:
        flash(f"No user found with email: {email}")
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))
    #Check if password matches
    if not check_password_hash(user.password, password):
        flash("Password check failed.")
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))
    #Log the user in
    login_user(user, remember=remember)
    #Ensure role is processed correctly
    user_role = user.role.strip().lower()
    flash(f"Processed user role: {user_role}")
    #Redirect based on user role
    if user_role == 'student':
        flash("Redirecting to student landing page.")
        return redirect(url_for('student.landing'))  # Redirect to student landing page
    elif user_role == 'teacher':
        flash("Redirecting to teacher landing page.")
        return redirect(url_for('teacher.landing'))  # Redirect to teacher landing page
    else:
        flash("Unknown role for user, redirecting to login.")
        return redirect(url_for('auth.login'))

"""
Sign up
"""
@auth.route('/signup')
def signup()->str:
    """
    Pass to the sign up page
    """
    return render_template('auth/signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post()->str:
    """
    Takes email, name, surname, school, passwort and role (hidden)
    tests whether user already exists
    If not, creates new user
    """
    email = request.form.get('email')
    name = request.form.get('name')
    surname = request.form.get('surname')
    school = request.form.get('school')
    password = request.form.get('password')
    role = request.form.get('role')

    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    new_user = User(email=email, name=name, surname=surname, school=school, password=generate_password_hash(password, method='pbkdf2:sha256'), role=role)
    db.session.add(new_user)
    db.session.commit()

    flash(f"New user created: {email} with role: {role}")
    return redirect(url_for('auth.login'))

"""
Logout
"""
@auth.route('/logout')
@login_required
def logout()->str:
    """
    Logs out the user and redirects to the main page
    """
    logout_user()
    return redirect(url_for('pages.home'))