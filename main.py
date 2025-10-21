from datetime import date, time
from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean, Date, Text, Time
from flask_sqlalchemy import SQLAlchemy
from forms import RegisterForm, LoginForm, ContactForm, PatientProfileForm
from functools import wraps
from enum import IntEnum

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
    role_level: Mapped[int] = mapped_column(Integer, nullable=False)
    patient_profile = relationship("PatientProfile", back_populates="patient", uselist=False)
    appointments = relationship("Appointment", primaryjoin="or_(User.id==Appointment.doctor_id,"
                                                           "User.id==Appointment.patient_id)", viewonly=True)

class PatientProfile(db.Model):
    __tablename__ = "patients"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    gender: Mapped[str] = mapped_column(String)
    dob: Mapped[date] = mapped_column(Date)
    cultural: Mapped[str] = mapped_column(Text)
    dietary: Mapped[str] = mapped_column(Text)
    allergens: Mapped[str] = mapped_column(Text)
    medical_history: Mapped[str] = mapped_column(Text)
    user_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))
    patient = relationship("User", back_populates="patient_profile")
    patient_logs = relationship("PatientLog", back_populates="patient")

class Appointment(db.Model):
    __tablename__ = "appointments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    time: Mapped[time] = mapped_column(Time, nullable=False)
    created_by: Mapped[str] = mapped_column(String)
    reason: Mapped[str] = mapped_column(Text)
    completed: Mapped[bool] = mapped_column(Boolean)
    doctor_id: Mapped[int] = mapped_column(db.ForeignKey("users.id"), nullable=False)
    patient_id: Mapped[int] = mapped_column(db.ForeignKey("users.id"), nullable=False)
    doctor = relationship("User", foreign_keys=doctor_id)
    patient = relationship("User", foreign_keys=patient_id)

class PatientLog(db.Model):
    __tablename__ = "patient_logs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    time: Mapped[time] = mapped_column(Time, nullable=False)
    created_by: Mapped[str] = mapped_column(String)
    medical: Mapped[str] = mapped_column(Text)
    emotional: Mapped[str] = mapped_column(Text)
    dietary: Mapped[str] = mapped_column(Text)
    cultural: Mapped[str] = mapped_column(Text)
    story: Mapped[str] = mapped_column(Text)
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
    if request.method == "POST":
        if form.validate_on_submit():
            account = db.session.execute(db.select(User).where(User.email == form.email.data)).scalar()
            if account:
                if check_password_hash(account.password, form.password.data):
                    login_user(account)
                    flash("Successfully logged in", "success")
                    return redirect(url_for("home"))
                else:
                    flash("Invalid credentials", "danger")
                    return redirect(url_for("login"))
            else:
                flash("That email has not been registered. Try signing up instead.", "danger")
                return redirect(url_for("login"))
    return render_template("account.html", form=form, type="login")

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
    patient_log = []
    for log in patient_profile.patient_logs:
        log.append(
            {
                ""
            }
        )
    return render_template("profile.html", role=role, patient_profile=patient_profile, patient_log=patient_log)

@app.route("/profile/create", methods=["GET", "POST"])
def create_profile():
    form = PatientProfileForm()
    if request.method == "POST":
        if form.validate_on_submit():
            new_profile = PatientProfile(
                gender = form.gender.data,
                dob = form.dob.data,
                cultural = form.cultural.data,
                dietary = form.dietary.data,
                allergens = form.allergens.data,
                medical_history = form.medical_history.data,
                user_id = current_user.id
            )
            db.session.add(new_profile)
            db.session.commit()
        return redirect(url_for("profile"))
    return render_template("profile_edit.html", form=form)

@app.route("/profile/edit", methods=["GET", "POST"])
def edit_patient_profile():
    cur_profile = current_user.patient_profile
    form = PatientProfileForm(
        gender=cur_profile.gender,
        dob=cur_profile.dob,
        cultural=cur_profile.cultural,
        dietary=cur_profile.dietary,
        allergens=cur_profile.allergens,
        medical_history=cur_profile.medical_history
    )
    if request.method == "POST":
        if form.validate_on_submit():
            cur_profile.gender = form.gender.data
            cur_profile.dob = form.dob.data
            cur_profile.cultural = form.cultural.data
            cur_profile.dietary = form.dietary.data
            cur_profile.allergens = form.allergens.data
            cur_profile.medical_history = form.medical_history.data

            db.session.commit()
        return redirect(url_for("profile"))
    return render_template("profile_edit.html", form=form, editing=True)

@app.route("/appointment")
def appointment():
    return render_template("appointments.html")

@app.route("/appointment/create")
def create_appointment():
    pass


@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if request.method == "GET":
        if form.validate_on_submit():
            print(form.email.data)
            print(form.feedback.data)

    return render_template("contact.html", form=form)

@app.route("/staff")
def staff():
    pass

@app.route("/admin")
def admin():
    return render_template("admin_home.html")




















if __name__ == "__main__":
    app.run(debug=True)