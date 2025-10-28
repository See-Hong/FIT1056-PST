from flask import url_for
from flask_login import current_user
from app.models import db, User, PatientLog, PatientProfile, Role
import datetime as dt

def search_patients(search=None, gender=None, min_age=None, max_age=None, risk=None):
    """Returns a list of patients filtered by search criteria."""

    # Search query conditions
    query = db.select(User).where(User.role_level == Role.PATIENT)
    if search and search.strip():
        query = query.where(User.username.ilike(f"%{search.strip()}%"))
    if gender:
        query = query.where(User.gender == gender)
    if min_age:
        query = query.where(User.dob <= dt.date.today() - dt.timedelta(days=365 * min_age))
    if max_age:
        query = query.where(User.dob >= dt.date.today() - dt.timedelta(days=365 * max_age))
    if risk:
        query = query.join(User.patient_profile).where(PatientProfile.risk_level == risk)

    patients = db.session.execute(query).scalars().all()
    return patients

def build_patient_table_data(patients):
    """Builds a list of dicts representing patient info for table display."""

    patient_list = []
    for patient in patients:
        if patient.patient_profile:
            risk = patient.patient_profile.risk_level
        else:
            risk = None
        # Url for the patient's profile
        profile_url = url_for("staff.staff_patient_details_page", patient_id=patient.id)
        patient_list.append(
            {
                "name": patient.username,
                "dob": patient.dob,
                "gender": patient.gender,
                "risk_level": risk,
                "profile": f"<a href='{profile_url}' class='btn btn-primary btn-sm'>Profile</a>"
            }
        )
    return patient_list

def build_log_table_data(patient_id):
    """Builds a list of dicts representing patient logs for table display."""

    profile = db.session.get(User, patient_id).patient_profile
    log_list = []
    if profile:
        logs = profile.patient_logs
        for log in logs:
            log_list.append({
                "date": log.date,
                "time": log.time,
                "created_by": current_user.username,
                "medical": log.medical,
                "emotional": log.emotional,
                "notes": log.note,
                "patient_note": log.patient_note,
                "edit": f"<a href='{url_for("staff.staff_log_editor_page", patient_id=patient_id, log_id=log.id)}' class='btn btn-primary btn-sm'>Edit</a>",
            })
    return log_list

def patient_log_create(date, time, medical, emotional, note, created_by, profile_id):
    """Creates a new patient log with the given conditions and commits to db"""
    new_log = PatientLog(
        date=date,
        time=time,
        medical=medical,
        emotional=emotional,
        note=note,
        created_by=created_by,
        profile_id=profile_id
    )
    db.session.add(new_log)
    db.session.commit()
    return new_log

def log_edit(log_id, medical=None, emotional=None, note=None):
    """Edits a logs contents"""
    log = db.session.get(PatientLog, log_id)
    if not log:
        raise ValueError
    if medical:
        log.medical = medical
    if emotional:
        log.emotional = emotional
    if note:
        log.note = note
    db.session.commit()
    return log

