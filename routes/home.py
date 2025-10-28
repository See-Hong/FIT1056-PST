from flask import Blueprint, render_template, redirect, url_for, request, flash
import datetime as dt
from app.forms import FeedbackForm
import os
from dotenv import load_dotenv
import requests

load_dotenv(".env")
SHEETY_ENDPOINT = os.environ.get("SHEETY_ENDPOINT")

home_bp = Blueprint("home", __name__)

@home_bp.route("/")
def home_page():
    return render_template("home/home.html")

@home_bp.route("/about")
def about_page():
    return render_template("home/about.html")

@home_bp.route("/feedback", methods=["GET", "POST"])
def feedback_page():
    form = FeedbackForm()
    if request.method == "POST" and form.validate_on_submit():
        new_row = {
            "feedback": {
                "timestamp": dt.datetime.now().isoformat(),
                "name": form.name.data,
                "email": form.email.data,
                "feedbackType": form.feedback_type.data,
                "rating": form.rating.data,
                "category": form.category.data,
                "message": form.message.data,
                "anonymous": form.anonymous.data,
            }
        }
        requests.post(SHEETY_ENDPOINT, json=new_row)
        flash("Successfully sent feedback", "success")
        return redirect(url_for("home.feedback_page"))
    return render_template("home/feedback.html", form=form)