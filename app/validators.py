from functools import wraps
from flask_login import current_user
from flask import abort, flash, redirect, url_for, request

def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.role_level != 4:
            flash("You don't have access for this page.", "warning")
            return redirect(request.referrer or url_for("home.home_page"))

        # Otherwise continue with the route function
        return f(*args, **kwargs)

    return decorated_function

def not_logged_in(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.is_authenticated:
            flash("You are not allowed on this page.", "warning")
            return redirect(request.referrer or url_for("home.home_page"))
        # Otherwise continue with the route function
        return f(*args, **kwargs)

    return decorated_function

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if not current_user.is_authenticated:
            flash("You must be logged in to enter this page.", "warning")
            return redirect(url_for("auth.login_page"))
        # Otherwise continue with the route function
        return f(*args, **kwargs)

    return decorated_function