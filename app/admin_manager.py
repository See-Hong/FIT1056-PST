from app.models import db, User, Role
from flask import url_for
import requests
import os
import datetime as dt


def search_accounts(search=None, gender=None, role=None):
    """Returns a list of users filtered by search criteria."""
    query = db.select(User)

    # Search query conditions
    if search and search.strip():
        query = query.where(User.username.ilike(f"%{search.strip()}%"))
    if gender:
        query = query.where(User.gender == gender)
    if role is not None:
        query = query.where(User.role_level == role)

    accounts = db.session.execute(query).scalars().all()
    return accounts


def build_account_table_data(accounts):
    """Builds a list of dicts representing user info for table display."""
    account_list = []
    for account in accounts:
        role = Role(account.role_level).name.title()
        role_change_url = url_for("admin.role_management_page", user_id=account.id)

        # Only allows non admin roles to be changed
        if account.role_level < 4:
            btn = f"<a href='{role_change_url}' class='btn btn-primary btn-sm'>Change Role</a>"
        else:
            btn = f"<a href='{role_change_url}' class='btn btn-danger btn-sm disabled-link'>Not Allowed</a>"

        account_list.append({
            "name": account.username,
            "email": account.email,
            "gender": account.gender,
            "role": role,
            "change": btn,
        })
    return account_list


def change_user_role(user_id, new_role):
    """Updates a user's role and commits the change."""

    # Makes sure the user is in the db and isn't an admin
    user = db.session.get(User, user_id)
    if not user or user.role_level == 4:
        raise ValueError("User not found")

    # Checks role validity
    try:
        Role(new_role)
    except ValueError:
        raise ValueError("Role Invalid")

    user.role_level = new_role
    db.session.commit()
    return user

def build_feedback_table_data():
    """Builds a list of dicts representing user feedback for table display."""

    # SHEETY API get request
    api_endpoint = os.environ.get("SHEETY_ENDPOINT")
    result = requests.get(api_endpoint).json()
    feedback_list = []
    for record in result["feedback"]:
        if record["anonymous"]:
            name = "Patient"
            email = None
        else:
            name = record["name"]
            email = record["email"]
        feedback_list.append(
            {
                "timestamp": dt.datetime.fromisoformat(record["timestamp"]),
                "name": name,
                "email": email,
                "feedback_type": record["feedbackType"].title(),
                "rating": record["rating"],
                "category": record["category"],
                "message": record["message"],
            }
        )
    return feedback_list

