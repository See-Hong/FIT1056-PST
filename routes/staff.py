from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user
from app.models import db, Appointment, User, PatientLog
from app.forms import SearchPatientForm, CreatePatientLogForm, PatientProfileForm, StaffPatientProfileForm, CreateAppointmentForm
import datetime as dt
from app.staff_manager import search_patients, build_patient_table_data, build_log_table_data, log_edit, patient_log_create
from app.profile_manager import patient_profile_create, patient_profile_edit
from app.appointment_manager import create_new_appointment, appointment_cancel, appointment_accept, appointment_complete

staff_bp = Blueprint("staff", __name__)

def check_access():
    if not current_user.is_authenticated:
        flash("You must be logged in to access this page.", "warning")
        return redirect(url_for("auth.login_page"))

    if not current_user.role_level > 0:
        flash("You don't have access for this page.", "warning")
        return redirect(request.referrer or url_for("home.home_page"))

@staff_bp.route("/staff")
def staff_dashboard():
    return render_template("staff/staff_dashboard.html")

@staff_bp.route("/staff/patients", methods=["POST","GET"])
def staff_patient_management_page():
    form = SearchPatientForm()
    if request.method == "POST" and form.validate_on_submit():
        patients = search_patients(
            search=form.search.data,
            gender=form.gender.data,
            min_age=form.min_age.data,
            max_age=form.max_age.data,
            risk=form.risk_level.data
        )
    else:
        patients = search_patients()
    patient_list = build_patient_table_data(patients)
    titles = [
        ("name","Patient Name"),
        ("dob", "DOB"),
        ("gender", "Gender"),
        ("risk_level", "Risk Level"),
        ("profile", "#")
    ]
    return render_template("staff/patient_list.html", form=form, patient_list=patient_list, titles=titles)

@staff_bp.route("/staff/patients/<int:patient_id>")
def staff_patient_details_page(patient_id):
    result = db.session.execute(db.select(User).where(User.id == patient_id, User.role_level == 0)).scalar()
    log_list = build_log_table_data(patient_id)
    titles = [
        ("date", "Date"),
        ("time", "Time"),
        ("created_by", "Created By"),
        ("medical", "Medical Observations"),
        ("emotional", "Emotional State"),
        ("notes", "Notes"),
        ("patient_note", "Patient Notes"),
        ("edit", "#"),
    ]
    return render_template("staff/view_patient_profile.html", patient=result, log_list=log_list, titles=titles)

@staff_bp.route("/staff/patients/<int:patient_id>/log/<int:log_id>/edit", methods=["GET", "POST"])
def staff_log_editor_page(patient_id, log_id):
    log = db.session.get(PatientLog, log_id)
    form = CreatePatientLogForm(
        medical= log.medical,
        emotional= log.emotional,
        note= log.note,
    )
    if request.method == "POST" and form.validate_on_submit():
        if log_edit(log.id,
            medical= form.medical.data,
            emotional=form.emotional.data,
            note=form.note.data
                    ):
            flash("Successfully updated patient log", "success")
        else:
            flash("Something went wrong", "error")
        return redirect(url_for("staff.staff_patient_details_page", patient_id=patient_id))
    return render_template("staff/create_patient_log.html", form=form, edit=True)

@staff_bp.route("/staff/patients/<int:patient_id>/create", methods=["GET","POST"])
def staff_patient_profile_creation_page(patient_id):
    form = PatientProfileForm()
    if request.method == "POST" and form.validate_on_submit():
        if patient_profile_create(
            cultural=form.cultural.data,
            dietary=form.dietary.data,
            allergens=form.allergens.data,
            medical_history=form.medical_history.data,
            user_id=patient_id,
            risk_level="Low"
        ):
            flash("Successfully created patient profile", "success")
        else:
            flash("Something went wrong", "error")
        return redirect(url_for("staff.staff_patient_details_page", patient_id=patient_id))
    return render_template("profile/edit_patient_profile.html", form=form)

@staff_bp.route("/staff/patients/<int:patient_id>/edit", methods=["GET","POST"])
def staff_patient_profile_editor_page(patient_id):
    cur_profile = db.session.get(User, patient_id).patient_profile
    form = StaffPatientProfileForm(
        cultural=cur_profile.cultural,
        dietary=cur_profile.dietary,
        allergens=cur_profile.allergens,
        medical_history=cur_profile.medical_history,
        risk=cur_profile.risk_level
    )
    if request.method == "POST" and form.validate_on_submit():
        if patient_profile_edit(
            cur_profile.id,
            cultural=form.cultural.data,
            dietary=form.dietary.data,
            allergens=form.allergens.data,
            medical_history=form.medical_history.data,
            risk=form.risk.data
        ):
            flash("Successfully edited patient profile", "success")
        else:
            flash("Something went wrong", "error")

        return redirect(url_for("staff.staff_patient_details_page", patient_id=patient_id))
    return render_template("profile/edit_patient_profile.html", form=form, editing=True)

@staff_bp.route("/staff/patients/<int:patient_id>/log/create", methods=["GET", "POST"])
def staff_patient_log_creation_page(patient_id):
    form = CreatePatientLogForm()
    if request.method == "POST" and form.validate_on_submit():
        if patient_log_create(
                date=dt.date.today(),
                time=dt.datetime.today().time(),
                medical=form.medical.data,
                emotional=form.emotional.data,
                note=form.note.data,
                created_by=current_user.username,
                profile_id=db.session.get(User, patient_id).patient_profile.id
        ):
            flash("Successfully added a patient log", "success")
        else:
            flash("Something went wrong", "error")
        return redirect(url_for("staff.staff_patient_details_page", patient_id=patient_id))
    return render_template("staff/create_patient_log.html", form=form, patient_id=patient_id)

@staff_bp.route("/staff/appointments")
def staff_view_appointments_page():
    user_appointments = db.session.execute(db.select(Appointment).where(Appointment.doctor_id == current_user.id)).scalars().all()
    pending_appointments = db.session.execute(db.select(Appointment).where(Appointment.doctor_id.is_(None), Appointment.status == "Pending")).scalars().all()
    return render_template("staff/staff_appointments.html", user_appointments=user_appointments, pending_appointments=pending_appointments)

@staff_bp.route("/staff/appointments/<int:appointment_id>/accept", methods=["POST"])
def staff_appointment_confirmation_button(appointment_id):
    if appointment_accept(appointment_id, current_user.id):
        flash("Marked appointment as scheduled", "success")
    else:
        flash("Something went wrong", "error")
    return redirect(url_for("staff.staff_view_appointments_page"))

@staff_bp.route("/staff/appointments/<int:appointment_id>/complete", methods=["POST"])
def staff_appointment_completion_button(appointment_id):
    if appointment_complete(appointment_id):
        flash("Marked appointment as complete", "success")
    else:
        flash("Something went wrong", "error")
    return redirect(url_for("staff.staff_view_appointments_page"))

@staff_bp.route("/staff/appointments/<int:appointment_id>/cancel", methods=["POST"])
def staff_appointment_cancellation_button(appointment_id):
    if appointment_cancel(appointment_id):
        flash("Marked appointment as cancelled", "success")
    else:
        flash("Something went wrong", "error")
    return redirect(url_for("staff.staff_view_appointments_page"))

@staff_bp.route("/staff/patients/<int:patient_id>/appointment/create", methods=["GET", "POST"])
def staff_appointment_creation_page(patient_id):
    form = CreateAppointmentForm()
    if request.method == "POST" and form.validate_on_submit():
        if current_user.role_level == 3:
            status = "Scheduled"
            doctor_id = current_user.id
        else:
            status = "Pending"
            doctor_id = None
        if create_new_appointment(
            date=form.date.data,
            time=form.time.data,
            reason=form.reason.data,
            created_by=current_user.id,
            status=status,
            patient_id=patient_id,
            doctor_id=doctor_id
        ):
            flash("Successfully booked an appointment", "success")
        else:
            flash("Something went wrong", "error")
        return redirect(url_for("staff.staff_patient_details_page", patient_id=patient_id))
    return render_template("appointments/create_appointment.html", form=form, patient_id=patient_id)