from flask import Blueprint, render_template, redirect, url_for, request, flash
from app.models import db, User
from app.forms import SearchAccountForm, RoleForm
from flask_login import current_user
from app.admin_manager import search_accounts, build_account_table_data, change_user_role, build_feedback_table_data

admin_bp = Blueprint("admin", __name__)

@admin_bp.before_request
def check_access():

    if not current_user.is_authenticated:
        flash("You must be logged in to access this page.", "warning")
        return redirect(url_for("auth.login_page"))

    if not current_user.role_level == 4:
        flash("You don't have access for this page.", "warning")
        return redirect(request.referrer or url_for("home.home_page"))

@admin_bp.route("/admin")
def admin_dashboard():
    return render_template("admin/admin_dashboard.html")

@admin_bp.route("/admin/manage-staff", methods=["GET", "POST"])
def staff_management_page():
    form = SearchAccountForm()

    if request.method == "POST" and form.validate_on_submit():
        accounts = search_accounts(form.search.data, form.gender.data, form.role.data)
    else:
        accounts = search_accounts()

    account_list = build_account_table_data(accounts)

    titles = [
        ("name", "Account Name"),
        ("email", "Email"),
        ("gender", "Gender"),
        ("role", "Role"),
        ("change", "#")
    ]

    return render_template("admin/user_list.html", form=form, account_list=account_list, titles=titles)


@admin_bp.route("/admin/manage-staff/<int:user_id>/change", methods=["GET", "POST"])
def role_management_page(user_id):
    user = db.session.get(User, user_id)
    form = RoleForm(role=user.role_level)
    if request.method == "POST" and form.validate_on_submit():
        try:
            change_user_role(user_id, form.role.data)
            flash("Role updated successfully", "success")
        except ValueError:
            flash("User not found", "error")
        return redirect(url_for("admin.staff_management_page"))

    return render_template("admin/role_changer.html", form=form)

import requests

@admin_bp.route("/admin/user-feedback")
def user_feedback_page():
    feedback_list = build_feedback_table_data()
    build_feedback_table_data()
    titles = [("name", "Name"),
              ("email", "Email"),
              ("feedback_type", "Type"),
              ("rating", "Rating"),
              ("category", "Category"),
              ("message", "Message")
              ]
    return render_template("admin/user_feedback.html", feedback_list=feedback_list, titles=titles)


