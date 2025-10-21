from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField, SelectField, DateField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from flask_ckeditor import CKEditorField
import email_validator

class RegisterForm(FlaskForm):
    name = StringField("Username", validators=[DataRequired(), Length(min=5, max=20)])
    email = EmailField("Email", validators=[DataRequired(), Email("Please enter a valid email.")])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=30)])
    r_pass = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password", "Please re-enter your password.")])
    submit = SubmitField("Create Account")

class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email("Please enter a valid email.")])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")

class ContactForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email("Please enter a valid email.")])
    feedback = CKEditorField("Feedback", validators=[DataRequired()])
    submit = SubmitField("Send Feedback")

class PatientProfileForm(FlaskForm):
    gender = SelectField("Gender", choices=[("M", "Male"), ("F", "Female")], validators=[DataRequired()])
    dob = DateField("Date of Birth", validators=[DataRequired()])
    cultural = CKEditorField("Cultural Preferences")
    dietary = CKEditorField("Dietary Preferences")
    allergens = CKEditorField("Allergens")
    medical_history = CKEditorField("Medical History")
    submit = SubmitField("Confirm")