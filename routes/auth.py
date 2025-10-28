from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import login_user, logout_user, login_required
from app.forms import RegisterForm, LoginForm
from app.validators import not_logged_in
from app.auth_manager import register_user, verify_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
@not_logged_in
def register_page():
    form = RegisterForm()
    if request.method == "POST" and form.validate_on_submit():
        try:
            new_user = register_user(
                form.name.data, form.email.data, form.gender.data,
                form.dob.data, form.tel.data, form.password.data
            )
            login_user(new_user)
            session.permanent = True
            flash("Successfully created account", "success")
            return redirect(url_for("home.home_page"))
        except ValueError as e:
            flash(str(e), "error")
    return render_template("auth/account_register.html", form=form, type="register")

@auth_bp.route("/login", methods=["GET", "POST"])
@not_logged_in
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        account = verify_user(form.email.data, form.password.data)
        if account:
            login_user(account)
            session.permanent = True
            flash("Successfully logged in", "success")
            return redirect(url_for("home.home_page"))
        else:
            flash("Invalid Credentials", "error")
    return render_template("auth/account_login.html", form=form, type="login")

@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout_button():
    flash("Successfully logged out of account", "success")
    logout_user()
    return redirect(url_for("home.home_page"))