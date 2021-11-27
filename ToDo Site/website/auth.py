from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.engine import url
from sqlalchemy.sql.expression import true
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash

authPage = Blueprint("authPage", __name__)

@authPage.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        userName = request.form.get("userName")
        password = request.form.get("password")

        user = User.query.filter_by(userName = userName).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category = "success")
                login_user(user, remember = True)
                return redirect(url_for("homePage.home"))
            else:
                flash("Incorrect password, try again please.", category = "error")
        else:
            flash("Username does not exist.", category = "error")
    return render_template("login.html", user = current_user)

@authPage.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("authPage.login"))

@authPage.route("/sign-up", methods = ["GET", "POST"])
def sign_up():
    if request.method == "POST":
        userName = request.form.get("userName")
        password = request.form.get("password")
        passwordConfirm = request.form.get("passwordConfirm")

        user = User.query.filter_by(userName = userName).first()
        
        if user:
            flash("Username already exists.", category = "error")
        elif len(userName) < 4:
            flash("Username cannot be under 4 characters.", category = "error")
        elif len(userName) > 16:
            flash("Username cannot exceed 16 characters.", category = "error")
        elif len(password) < 6:
            flash("Password cannot be under 6 characters.", category = "error")
        elif len(password) > 24:
            flash("Password must be at least 24 characters.", category = "error")
        elif password != passwordConfirm:
            flash("Passwords do not match.", category = "error")
        else:
            new_user = User(userName = userName, password = generate_password_hash(password, method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Account Created!", category = "success")
            return redirect(url_for("homePage.home"))

    return render_template("sign_up.html", user = current_user)