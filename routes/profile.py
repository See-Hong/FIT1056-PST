from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user
from app.models import db, PatientLog, Role
from app.forms import EditProfileForm, PatientNoteForm, PatientProfileForm, PasswordChangeForm
from app.profile_manager import build_patient_log_table_data, patient_note_add, update_profile, patient_profile_create, patient_profile_edit
from app.auth_manager import change_user_password

profile_bp = Blueprint("profile", __name__)

EXEMPT_ROUTES = {"profile.user_profile_page", "profile.user_profile_editor_page", "profile.password_changer_page"}

@profile_bp.before_request
def check_access():
    if request.endpoint in EXEMPT_ROUTES:
        return

    if not current_user.is_authenticated:
        flash("You must be logged in to access this page.", "warning")
        return redirect(url_for("auth.login_page"))

    if not current_user.role_level == 0:
        flash("You don't have access for this page.", "warning")
        return redirect(request.referrer or url_for("home.home_page"))

@profile_bp.route("/profile")
def user_profile_page():
    role = Role(current_user.role_level).name
    patient_profile = current_user.patient_profile
    log_list = []
    if patient_profile:
        log_list = build_patient_log_table_data(patient_profile.patient_logs)
    titles = [
        ("date", "Date"),
        ("time", "Time"),
        ("created_by", "Created By"),
        ("medical", "Medical Observations"),
        ("emotional", "Emotional State"),
        ("notes", "Notes"),
        ("patient_note", "Patient Notes"),
        ("add", "#"),
    ]
    return render_template("profile/profile.html", role=role, patient_profile=patient_profile, log_list=log_list, titles=titles)

@profile_bp.route("/profile/log/<int:log_id>/add_note", methods=["GET", "POST"])
def patient_patient_notes_page(log_id):
    log = db.session.get(PatientLog, log_id)
    form = PatientNoteForm(note=log.patient_note)
    if request.method == "POST" and form.validate_on_submit():
        patient_note_add(log_id, form.note.data)
        flash("Successfully added patient note", "success")
        return redirect(url_for("profile.user_profile_page"))
    return render_template("profile/add_patient_note.html", form=form)

@profile_bp.route("/profile/edit", methods=["GET","POST"])
def user_profile_editor_page():
    form = EditProfileForm(
        name=current_user.username,
        gender=current_user.gender,
        dob=current_user.dob,
        tel=current_user.contact
    )
    if request.method == "POST" and form.validate_on_submit():
        if update_profile(current_user.id,
                       name=form.name.data,
                       gender=form.gender.data,
                       dob=form.dob.data,
                       contact=form.tel.data
                       ):
            flash("Successfully updated user profile", "success")
        else:
            flash("Something went wrong", "error")
        return redirect(url_for("profile.user_profile_page"))
    return render_template("profile/edit_user_profile.html", form=form)

@profile_bp.route("/profile/edit/password", methods=["GET", "POST"])
def password_changer_page():
    form = PasswordChangeForm()
    if request.method == "POST" and form.validate_on_submit():
        if change_user_password(current_user.id, form.old_pass.data, form.password.data):
            flash("Successfully changed password", "success")
            return redirect(url_for("profile.user_profile_page"))
        else:
            flash("Password Incorrect", "error")
            return redirect(url_for("profile.password_changer_page"))
    return render_template("profile/change_password.html", form=form)

@profile_bp.route("/profile/create", methods=["GET", "POST"])
def patient_profile_creation_page():
    form = PatientProfileForm()
    if request.method == "POST" and form.validate_on_submit():
        if patient_profile_create(
            cultural=form.cultural.data,
            dietary=form.dietary.data,
            allergens=form.allergens.data,
            medical_history=form.medical_history.data,
            user_id=current_user.id,
            risk_level="Low"
        ):
            flash("Successfully created patient profile", "success")
        else:
            flash("Something went wrong", "error")
        return redirect(url_for("profile.user_profile_page"))
    return render_template("profile/edit_patient_profile.html", form=form)

@profile_bp.route("/profile/patient/edit", methods=["GET", "POST"])
def patient_profile_editor_page():
    cur_profile = current_user.patient_profile
    form = PatientProfileForm(
        cultural=cur_profile.cultural,
        dietary=cur_profile.dietary,
        allergens=cur_profile.allergens,
        medical_history=cur_profile.medical_history
    )
    if request.method == "POST" and form.validate_on_submit():
        if patient_profile_edit(
            cur_profile.id,
            cultural=form.cultural.data,
            dietary=form.dietary.data,
            allergens=form.allergens.data,
            medical_history=form.medical_history.data
        ):
            flash("Successfully edited patient profile", "success")
        else:
            flash("Something went wrong", "error")
        return redirect(url_for("profile.user_profile_page"))
    return render_template("profile/edit_patient_profile.html", form=form, editing=True)