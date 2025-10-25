from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField, SelectField, DateField, IntegerField, TelField, DateTimeField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional, NumberRange, Regexp
from flask_ckeditor import CKEditorField
import email_validator

class RegisterForm(FlaskForm):
    name = StringField("Username", validators=[DataRequired(), Length(min=5, max=20)])
    email = EmailField("Email", validators=[DataRequired(), Email("Please enter a valid email.")])
    gender = SelectField("Gender", choices=[("Male", "Male"), ("Female", "Female")], validators=[DataRequired()])
    dob = DateField("Date of Birth", validators=[DataRequired()])
    tel = TelField("Telephone No. (Optional)", validators=[Optional(), Regexp(r'^\+?[\d\s\-]{7,15}$', message="Invalid phone number format.")])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=30)])
    r_pass = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password", "Please re-enter your password.")])
    submit = SubmitField("Create Account")

class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email("Please enter a valid email.")])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")

class FeedbackForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email("Please enter a valid email.")])
    feedback = CKEditorField("Feedback", validators=[DataRequired()])
    submit = SubmitField("Send Feedback")

class EditProfileForm(FlaskForm):
    name = StringField("Username", validators=[DataRequired()])
    gender = SelectField("Gender", choices=[("Male", "Male"), ("Female", "Female")], validators=[DataRequired()])
    dob = DateField("Date of Birth", validators=[DataRequired()])
    tel = TelField("Telephone No. (Optional)", validators=[Optional(), Regexp(r'^\+?[\d\s\-]{7,15}$', message="Invalid phone number format.")])
    submit = SubmitField("Submit Changes")

class PasswordChangeForm(FlaskForm):
    old_pass = PasswordField("Old Password", validators=[DataRequired(), Length(min=8, max=30)])
    password = PasswordField("New Password", validators=[DataRequired(), Length(min=8, max=30)])
    r_pass = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password", "Please re-enter your password.")])
    submit = SubmitField("Change Password")

class PatientProfileForm(FlaskForm):
    cultural = CKEditorField("Cultural Preferences")
    dietary = CKEditorField("Dietary Preferences")
    allergens = CKEditorField("Allergens")
    medical_history = CKEditorField("Medical History")
    submit = SubmitField("Confirm")

class SearchPatientForm(FlaskForm):
    search = StringField("Search", validators=[Optional()])
    min_age = IntegerField("Age", validators=[Optional()])
    max_age = IntegerField("   ", validators=[Optional()])
    gender = SelectField("Gender", choices=[("", "None"), ("Male", "Male"), ("Female", "Female")], validators=[Optional()], coerce=lambda x: x or None)
    risk_level = SelectField("Risk", choices=[("", "None"), ("Low", "Low"), ("Moderate", "Moderate"), ("High", "High")], validators=[Optional()], coerce=lambda x: x or None)
    submit = SubmitField("Search")

class CreateAppointmentForm(FlaskForm):
    datetime = DateTimeField("Appointment Date and Time", validators=[DataRequired()])
    reason = StringField("Appointment Reason", validators=[DataRequired()])
    submit = SubmitField("Confirm")