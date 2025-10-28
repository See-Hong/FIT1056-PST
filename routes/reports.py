from flask import Blueprint, render_template, redirect, url_for, flash, request
from sqlalchemy import func
from app.models import db, Appointment, User, PatientLog, PatientProfile
import datetime as dt
from flask_login import current_user

report_bp = Blueprint("report", __name__)

@report_bp.before_request
def check_access():

    if not current_user.is_authenticated:
        flash("You must be logged in to access this page.", "warning")
        return redirect(url_for("auth.login_page"))

    if not current_user.role_level > 0:
        flash("You don't have access for this page.", "warning")
        return redirect(request.referrer or url_for("home.home_page"))


@report_bp.route("/staff/reports")
def reports_page():
    total_patients = db.session.query(User).where(User.role_level == 0).count()
    total_appointments = db.session.query(Appointment).where(Appointment.status != "Cancelled").count()
    total_logs = db.session.query(PatientLog).count()
    high_risk = db.session.query(User).join(User.patient_profile).where(User.role_level == 0).filter_by(risk_level="High").count()

    appointments_per_month_query = (
        db.session.query(
            func.strftime("%Y-%m", Appointment.date).label("month"),
            func.count(Appointment.id)
        )
        .group_by("month")
        .order_by("month")
        .all()
    )

    appointments_per_month = {
        dt.datetime.strptime(month, "%Y-%m").strftime("%b %Y"): count
        for month, count in appointments_per_month_query
    }

    risk_distribution = {
        "Low": db.session.query(User).join(User.patient_profile).where(User.role_level == 0).filter_by(risk_level="Low").count(),
        "Moderate": db.session.query(User).join(User.patient_profile).where(User.role_level == 0).filter_by(risk_level="Moderate").count(),
        "High": db.session.query(User).join(User.patient_profile).where(User.role_level == 0).filter_by(risk_level="High").count()
    }

    today = dt.date.today()
    seven_days_ago = today - dt.timedelta(days=6)

    logs_over_time_query = (
        db.session.query(
            func.strftime("%Y-%m-%d", PatientLog.date).label("day"),
            func.count(PatientLog.id)
        )
        .filter(PatientLog.date.between(seven_days_ago, today))
        .group_by("day")
        .order_by("day")
        .all()
    )

    logs_over_time = {
        dt.datetime.strptime(day, "%Y-%m-%d").strftime("%d %b"): count
        for day, count in logs_over_time_query
    }

    doctors = db.session.query(User).where(User.role_level == 3)
    doctor_activity = {
        doctor.username: db.session.query(PatientLog).where(PatientLog.created_by == doctor.id).count() for doctor in doctors
    }
    #
    # # 5️⃣ Attachments Uploaded Over Time (past 6 months)
    # attachments_per_month = {
    #     (datetime.now() - timedelta(days=i * 30)).strftime("%b %Y"): random.randint(10, 50)
    #     for i in reversed(range(6))
    # }
    #
    # return render_template("staff_reports.html",
    #                        appointments_per_month=appointments_per_month,
    #                        risk_distribution=risk_distribution,
    #                        logs_over_time=logs_over_time,
    #                        doctor_activity=doctor_activity,
    #                        attachments_per_month=attachments_per_month
    #                        )

    return render_template("staff/staff_reports.html",
                           total_patients=total_patients,
                           total_appointments=total_appointments,
                           total_logs=total_logs,
                           high_risk=high_risk,
                           appointments_per_month=appointments_per_month,
                           risk_distribution=risk_distribution,
                           logs_over_time=logs_over_time,
                           doctor_activity=doctor_activity,
                           )

@report_bp.route("/staff/risk-dashboard")
def risk_dashboard():
    # Get risk level counts
    risk_data = (
        db.session.query(PatientProfile.risk_level, func.count(PatientProfile.id))
        .group_by(PatientProfile.risk_level)
        .all()
    )

    risk_distribution = {level or "Unknown": count for level, count in risk_data}

    risk_patients = {
        "High": PatientProfile.query.filter_by(risk_level="High").all(),
        "Medium": PatientProfile.query.filter_by(risk_level="Moderate").all(),
        "Low": PatientProfile.query.filter_by(risk_level="Low").all(),
    }

    total_patients = sum(risk_distribution.values())
    high_risk = risk_distribution.get("High", 0)
    medium_risk = risk_distribution.get("Moderate", 0)
    low_risk = risk_distribution.get("Low", 0)

    return render_template(
        "staff/risk_dashboard.html",
        risk_distribution=risk_distribution,
        total_patients=total_patients,
        high_risk=high_risk,
        medium_risk=medium_risk,
        low_risk=low_risk,
        risk_patients=risk_patients
    )