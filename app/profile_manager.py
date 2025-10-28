from app.models import db, PatientLog, User, PatientProfile
from flask import url_for
from flask_login import current_user

def build_patient_log_table_data(patient_log):
    """Builds a list of dicts representing log info for table display."""
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
            "add": f"<a href='{url_for("profile.patient_patient_notes_page", log_id=log.id)}' class='btn btn-primary btn-sm'>Add Notes</a>",
        })
    return log_list

def update_profile(user_id, name=None, gender=None, dob=None, contact=None):
    """Updates a user's profile with the given parameters"""
    user = db.session.get(User, user_id)
    if not user:
        raise ValueError("User not found")
    if name:
        user.username = name
    if gender:
        user.gender = gender
    if dob:
        user.dob = dob
    if contact:
        user.contact = contact

    db.session.commit()
    return user

def patient_profile_create(cultural, dietary, allergens, medical_history, user_id, risk_level):
    """Lets a patient create a new patient profile"""
    new_profile = PatientProfile(
        cultural=cultural,
        dietary=dietary,
        allergens=allergens,
        medical_history=medical_history,
        user_id=user_id,
        risk_level=risk_level
    )
    db.session.add(new_profile)
    db.session.commit()
    return new_profile

def patient_profile_edit(profile_id=None, cultural=None, dietary=None, allergens=None, medical_history=None, risk=None):
    """Edits a patient's profile with the given parameters."""
    profile = db.session.get(PatientProfile, profile_id)
    if not profile:
        raise ValueError("Profile not found")
    if cultural:
        profile.cultural = cultural
    if dietary:
        profile.dietary = dietary
    if allergens:
        profile.allergens = allergens
    if medical_history:
        profile.medical_history = medical_history
    if risk:
        profile.risk_level = risk
    db.session.commit()
    return profile

def patient_note_add(log_id, note):
    """Adds a patient note to the given log"""
    log = db.session.get(PatientLog, log_id)
    if not log:
        raise ValueError("Log not found")
    log.patient_note = note
    db.session.commit()
    return log