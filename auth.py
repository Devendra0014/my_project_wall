# ✅ Final cleaned auth.py — Signup, Login, Logout with Blueprint
from flask import Blueprint, render_template, request, redirect, flash, session
from flask_login import login_user, logout_user,login_required
from models import User
from peewee import IntegrityError
import hashlib

auth_bp = Blueprint('auth', __name__)

# ✅ Signup
@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        if not User.get_or_none(User.email == email):
            hashed_password = hashlib.sha256(request.form['password'].encode()).hexdigest()
            avatar_url = f"https://api.dicebear.com/7.x/initials/svg?seed={username}"

            try:
                User.create(
                    name=request.form['name'],
                    username=username,
                    email=email,
                    password=hashed_password,
                    dob=request.form['dob'],
                    program=request.form['program'],
                    course=request.form['course'],
                    avatar_url=avatar_url
                )
                flash("Signup successful! Please login.", "success")
                return redirect('/login')
            except IntegrityError:
                flash("Email or username already exists.", "danger")
                return redirect('/signup')
        else:
            flash("Email already registered.", "warning")
            return redirect('/signup')
    return render_template('signup.html')

# ✅ Login
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        user = User.get_or_none(User.email == email)
        if user and user.password == hashed_password:
            login_user(user)
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['avatar'] = user.avatar_url
            flash(f"Welcome back, {user.name}!", "success")
            return redirect('/dashboard')
        else:
            flash("Invalid email or password!", "danger")
            return redirect('/login')
    return render_template('login.html')

# ✅ Logout
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash("You have been logged out.", "info")
    return redirect('/')