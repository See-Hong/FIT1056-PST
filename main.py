from datetime import date, time
import datetime as dt
from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean, Date, Text, Time
from flask_sqlalchemy import SQLAlchemy
from forms import RegisterForm, LoginForm, FeedbackForm, PatientProfileForm, SearchPatientForm, EditProfileForm, PasswordChangeForm, CreateAppointmentForm, CreatePatientLogForm, PatientNoteForm
from functools import wraps
from enum import IntEnum
from dotenv import load_dotenv
import os
import requests

load_dotenv(".env")
SHEETY_ENDPOINT = os.environ.get("SHEETY_ENDPOINT")

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap5(app)

class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy()
db.init_app(app)

class Role(IntEnum):
    PATIENT = 0
    RECEPTIONIST = 1
    NURSE = 2
    DOCTOR = 3
    ADMIN = 4

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    gender: Mapped[str] = mapped_column(String)
    dob: Mapped[date] = mapped_column(Date)
    contact: Mapped[str] = mapped_column(String)
    role_level: Mapped[int] = mapped_column(Integer, nullable=False)
    patient_profile = relationship("PatientProfile", back_populates="patient", uselist=False)
    appointments = relationship("Appointment", primaryjoin="or_(User.id==Appointment.doctor_id,"
                                                           "User.id==Appointment.patient_id)", viewonly=True)

class PatientProfile(db.Model):
    __tablename__ = "patients"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cultural: Mapped[str] = mapped_column(Text, nullable=True)
    dietary: Mapped[str] = mapped_column(Text, nullable=True)
    allergens: Mapped[str] = mapped_column(Text, nullable=True)
    medical_history: Mapped[str] = mapped_column(Text, nullable=True)
    user_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))
    risk_level: Mapped[str] = mapped_column(String, nullable=True)
    patient = relationship("User", back_populates="patient_profile")
    patient_logs = relationship("PatientLog", back_populates="patient")

class Appointment(db.Model):
    __tablename__ = "appointments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    time: Mapped[time] = mapped_column(Time, nullable=False)
    created_by: Mapped[int] = mapped_column(Integer)
    reason: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String)
    doctor_id: Mapped[int] = mapped_column(db.ForeignKey("users.id"), nullable=True)
    patient_id: Mapped[int] = mapped_column(db.ForeignKey("users.id"), nullable=True)
    doctor = relationship("User", foreign_keys=doctor_id)
    patient = relationship("User", foreign_keys=patient_id)

class PatientLog(db.Model):
    __tablename__ = "patient_logs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    time: Mapped[time] = mapped_column(Time, nullable=False)
    created_by: Mapped[int] = mapped_column(Integer)
    medical: Mapped[str] = mapped_column(Text, nullable=True)
    emotional: Mapped[str] = mapped_column(Text, nullable=True)
    note: Mapped[str] = mapped_column(Text, nullable=True)
    patient_note: Mapped[str] = mapped_column(Text, nullable=True)
    profile_id: Mapped[int] = mapped_column(db.ForeignKey("patients.id"))
    patient = relationship("PatientProfile", back_populates="patient_logs")


with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)

def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.role_level != Role.ADMIN:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)

    return decorated_function

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("You must be logged in to access this page", "warning")
            return redirect(url_for("login"))
        return f(*args, *kwargs)
    return decorated_function

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))



# HOME PAGES
@app.route("/test")
def test():
    return render_template("test.html")

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if request.method == "POST":
        if form.validate_on_submit():
            # Checks if email already exists.
            account = db.session.execute(db.select(User).where(User.email == form.email.data)).scalar()
            # If email exists
            if account:
                flash("That email is already registered. Try logging in instead.", "danger")
                return redirect(url_for("register"))
            else:
                new_user = User(
                    username=form.name.data,
                    email=form.email.data,
                    gender=form.gender.data,
                    dob=form.dob.data,
                    contact=form.tel.data,
                    password=generate_password_hash(form.password.data, salt_length=8),
                    role_level=Role.PATIENT
                )
                db.session.add(new_user)
                db.session.commit()

                login_user(new_user)
                flash("Successfully created account", "success")
                return redirect(url_for("home"))
    return render_template("account.html", form=form, type="register")

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        account = db.session.execute(db.select(User).where(User.email == form.email.data)).scalar()
        if account:
            if check_password_hash(account.password, form.password.data):
                login_user(account)
                flash("Successfully logged in", "success")
                return redirect(url_for("home"))
            else:
                flash("Invalid credentials", "error")
                return redirect(url_for("login"))
        else:
            flash("That email has not been registered. Try signing up instead.", "danger")
            return redirect(url_for("login"))
    return render_template("test.html", form=form, type="login")

@login_required
@app.route("/logout", methods=["POST"])
def logout():
    flash("Successfully logged out of account", "success")
    logout_user()
    return redirect(url_for("home"))

@login_required
@app.route("/profile")
def profile():
    role = Role(current_user.role_level).name
    patient_profile = current_user.patient_profile
    log_list = []
    if patient_profile:
        for log in patient_profile.patient_logs:
            log_list.append({
                "date": log.date,
                "time": log.time,
                "created_by": current_user.username,
                "medical": log.medical,
                "emotional": log.emotional,
                "notes": log.note,
                "patient_note": log.patient_note,
                "add": f"<a href='{url_for("add_patient_notes", log_id=log.id)}' class='btn btn-primary btn-sm'>Add Notes</a>",
            })
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
    return render_template("profile.html", role=role, patient_profile=patient_profile, log_list=log_list, titles=titles)

@app.route("/profile/log/<int:log_id>/add_note", methods=["GET", "POST"])
def add_patient_notes(log_id):
    log = db.session.get(PatientLog, log_id)
    form = PatientNoteForm(note=log.patient_note)
    if request.method == "POST" and form.validate_on_submit():
        log.patient_note = form.note.data
        db.session.commit()
        return redirect(url_for("profile"))
    return render_template("add_patient_note.html", form=form)


@app.route("/profile/edit", methods=["GET","POST"])
def edit_profile():
    form = EditProfileForm(
        name=current_user.username,
        gender=current_user.gender,
        dob=current_user.dob,
        tel=current_user.contact
    )
    if request.method == "POST" and form.validate_on_submit():
        current_user.name = form.name.data
        current_user.gender = form.gender.data
        current_user.dob = form.dob.data
        current_user.contact = form.tel.data
        db.session.commit()
    return render_template("edit_user_profile.html", form=form)

@app.route("/profile/edit/password", methods=["GET", "POST"])
def change_password():
    form = PasswordChangeForm()
    if request.method == "POST" and form.validate_on_submit():
        if check_password_hash(current_user.password, form.old_pass.data):
            current_user.password = generate_password_hash(form.password.data, salt_length=8)
            db.session.commit()
            flash("Successfully changed password", "success")
            return redirect(url_for("profile"))
        else:
            flash("Password Incorrect", "error")
    return render_template("change_password.html", form=form)

@app.route("/profile/create", methods=["GET", "POST"])
def create_patient_profile():
    form = PatientProfileForm()
    if request.method == "POST":
        if form.validate_on_submit():
            new_profile = PatientProfile(
                cultural = form.cultural.data,
                dietary = form.dietary.data,
                allergens = form.allergens.data,
                medical_history = form.medical_history.data,
                user_id = current_user.id
            )
            db.session.add(new_profile)
            db.session.commit()
            flash("Successfully created patient profile", "success")
        return redirect(url_for("profile"))
    return render_template("profile_edit.html", form=form)

@app.route("/profile/patient/edit", methods=["GET", "POST"])
def edit_patient_profile():
    cur_profile = current_user.patient_profile
    form = PatientProfileForm(
        cultural=cur_profile.cultural,
        dietary=cur_profile.dietary,
        allergens=cur_profile.allergens,
        medical_history=cur_profile.medical_history
    )
    if request.method == "POST":
        if form.validate_on_submit():
            cur_profile.cultural = form.cultural.data
            cur_profile.dietary = form.dietary.data
            cur_profile.allergens = form.allergens.data
            cur_profile.medical_history = form.medical_history.data
            flash("Successfully edited patient profile", "success")

            db.session.commit()
        return redirect(url_for("profile"))
    return render_template("profile_edit.html", form=form, editing=True)

@app.route("/appointment")
def appointment():
    return render_template("appointments.html")

@app.route("/appointment/create", methods=["GET","POST"])
def create_appointment():
    form = CreateAppointmentForm()
    if request.method == "POST" and form.validate_on_submit():
        new_appointment = Appointment(
                            date=form.date.data,
                            time=form.time.data,
                            reason=form.reason.data,
                            created_by=current_user.id,
                            status="Pending",
                            patient_id = current_user.id,
                        )
        db.session.add(new_appointment)
        db.session.commit()
        flash("Successfully booked an appointment", "success")
        return redirect(url_for("appointment"))
    return render_template("create_appointment.html", form=form)


@app.route("/about")
def about():
    pass

@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    form = FeedbackForm()
    if request.method == "POST":
        new_row = {
            "feedback": {
                "name": form.name.data,
                "email": form.email.data,
                "feedback_type": form.feedback_type.data,
                "rating": form.rating.data,
                "category": form.category.data,
                "message": form.message.data,
                "anonymous": form.anonymous.data,
            }
        }
        requests.post(SHEETY_ENDPOINT, json=new_row)
        return redirect(url_for("feedback"))
    return render_template("feedback.html", form=form)

@app.route("/staff/patients", methods=["POST","GET"])
def patient_page():
    form = SearchPatientForm()
    patients = db.select(User).where(User.role_level == 0)
    if request.method == "POST" and form.validate_on_submit():
        print(f"Searching: {form.search.data}")
        print(type(form.gender.data))
        print(form.min_age.data)
        print(form.max_age.data)
        print(form.risk_level.data)
        if form.search.data.strip() != "":
            patients = patients.where(User.username.ilike(f"%{form.search.data}%"))
        if form.gender.data:
            patients = patients.where(User.gender == form.gender.data)
        if form.min_age.data:
            patients = patients.where(User.dob <= dt.date.today() - dt.timedelta(form.min_age.data))
        if form.max_age.data:
            patients = patients.where(User.dob >= dt.date.today() - dt.timedelta(form.max_age.data))
        if form.risk_level.data:
            patients = patients.join(User.patient_profile).where(PatientProfile.risk_level == form.risk_level.data)
    patients = db.session.execute(patients).scalars().all()
    patient_list = []
    if patients:
        for patient in patients:
            if patient.patient_profile:
                risk = patient.patient_profile.risk_level
            else:
                risk = None
            profile_url = url_for("patient_details", patient_id=patient.id)
            patient_list.append(
                {
                    "name": patient.username,
                    "dob": patient.dob,
                    "gender": patient.gender,
                    "risk_level": risk,
                    "profile": f"<a href='{ profile_url }' class='btn btn-primary btn-sm'>Profile</a>"
                }
            )
    else:
        patient_list.append({}),
    titles = [
        ("name","Patient Name"),
        ("dob", "DOB"),
        ("gender", "Gender"),
        ("risk_level", "Risk Level"),
        ("profile", "#")
    ]


    return render_template("patient_list.html", form=form, patient_list=patient_list, titles=titles)

@app.route("/staff/patients/<int:patient_id>")
def patient_details(patient_id):
    result = db.session.execute(db.select(User).where(User.id == patient_id, User.role_level == 0)).scalar()
    patient_log = result.patient_profile.patient_logs
    log_list = []
    for log in patient_log:
        log_list.append({
            "date": log.date,
            "time": log.time,
            "created_by": current_user.username,
            "medical": log.medical,
            "emotional": log.emotional,
            "notes": log.note,
            "patient_note": log.patient_note,
            "edit": f"<a href='{ url_for("edit_log", patient_id=patient_id, log_id=log.id) }' class='btn btn-primary btn-sm'>Edit</a>",
        })
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
    return render_template("patient_profiles.html", patient=result, log_list=log_list, titles=titles)

@app.route("/staff/patients/<int:patient_id>/log/<int:log_id>/edit", methods=["GET", "POST"])
def edit_log(patient_id, log_id):
    log = db.session.get(PatientLog, log_id)
    form = CreatePatientLogForm(
        medical= log.medical,
        emotional= log.emotional,
        note= log.note,
    )
    if request.method == "POST" and form.validate_on_submit():
        log.medical = form.medical.data
        log.emotional = form.emotional.data
        log.note = form.note.data
        db.session.commit()
        return redirect(url_for("patient_details", patient_id=patient_id))
    return render_template("create_patient_log.html", form=form, edit=True)

@app.route("/staff/patients/<int:patient_id>/create", methods=["GET","POST"])
def create_profile_staff(patient_id):
    form = PatientProfileForm()
    if request.method == "POST":
        if form.validate_on_submit():
            new_profile = PatientProfile(
                cultural=form.cultural.data,
                dietary=form.dietary.data,
                allergens=form.allergens.data,
                medical_history=form.medical_history.data,
                user_id=patient_id
            )
            db.session.add(new_profile)
            db.session.commit()
        return redirect(url_for("patient_details", patient_id=patient_id))
    return render_template("profile_edit.html", form=form)

@app.route("/staff/patients/<int:patient_id>/log/create", methods=["GET", "POST"])
def create_patient_log(patient_id):
    form = CreatePatientLogForm()
    if request.method == "POST" and form.validate_on_submit():
        new_log = PatientLog(
            date=dt.date.today(),
            time=dt.datetime.today().time(),
            medical=form.medical.data,
            emotional=form.emotional.data,
            note=form.note.data,
            created_by=current_user.username,
            profile_id=db.session.get(User, patient_id).patient_profile.id
        )
        db.session.add(new_log)
        db.session.commit()
        flash("Successfully added a patient log", "success")
        return redirect(url_for("patient_details", patient_id=patient_id))
    return render_template("create_patient_log.html", form=form)


@app.route("/staff/reports")
def reports():
    pass

@app.route("/staff/risk-dashboard")
def risk_dashboard():
    pass

@app.route("/staff/alert-and-notes")
def alert_and_notes():
    pass

@app.route("/admin/manage-patients")
def manage_patients():
    pass

@app.route("/admin/manage-staff")
def manage_staff():
    pass

@app.route("/staff")
def staff():
    pass

@app.route("/admin")
def admin():
    return render_template("admin_dashboard.html")














if __name__ == "__main__":
    app.run(debug=True)