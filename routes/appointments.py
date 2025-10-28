from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user
from app.forms import CreateAppointmentForm
from app.appointment_manager import create_new_appointment, appointment_cancel

appointment_bp = Blueprint("appointment", __name__)

@appointment_bp.before_request
def check_access():

    if not current_user.is_authenticated:
        flash("You must be logged in to access this page.", "warning")
        return redirect(url_for("auth.login_page"))

    if not current_user.role_level == 0:
        flash("You don't have access for this page.", "warning")
        return redirect(request.referrer or url_for("home.home_page"))


@appointment_bp.route("/appointment")
def view_appointments_page():

    appointments = sorted(
        current_user.appointments,
        key=lambda a: (a.date, a.time),
        reverse=True
    )
    return render_template("appointments/appointments.html", appointments=appointments)

@appointment_bp.route("/appointment/create", methods=["GET","POST"])
def create_appointment_page():
    form = CreateAppointmentForm()
    if request.method == "POST" and form.validate_on_submit():
        if create_new_appointment(
            date=form.date.data,
            time=form.time.data,
            reason=form.reason.data,
            created_by=current_user.id,
            status="Pending",
            patient_id=current_user.id
        ):
            flash("Successfully booked an appointment", "success")
            return redirect(url_for("appointment.view_appointments_page"))
        else:
            flash("Something went wrong", "error")
    return render_template("appointments/create_appointment.html", form=form)

@appointment_bp.route("/appointments/<int:appointment_id>/cancel", methods=["POST"])
def cancel_appointment_button(appointment_id):
    if appointment_cancel(appointment_id):
        flash("Successfully cancelled appointment", "success")
    else:
        flash("Something went wrong", "error")
    return redirect(url_for("appointment.view_appointments_page"))