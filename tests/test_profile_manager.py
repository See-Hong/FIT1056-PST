import pytest
from flask import Flask
import datetime as dt
from app.models import db, User, PatientLog
from app.profile_manager import patient_note_add, update_profile, patient_profile_create, patient_profile_edit

@pytest.fixture(scope="function")
def app():
    """Create and configure a new app instance for each test."""
    app = Flask(__name__)
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        WTF_CSRF_ENABLED=False,
        SECRET_KEY="test_secret",
    )

    db.init_app(app)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope="function")
def client(app):
    return app.test_client()

@pytest.fixture(scope="function")
def session(app):
    """Provide a fresh database session for each test."""
    with app.app_context():
        yield db.session
        db.session.rollback()

def test_patient_note_add(session):
    log = PatientLog(
        date=dt.date.today(),
        time=dt.datetime.now().time(),
        created_by=1,
        profile_id=1
    )
    db.session.add(log)
    db.session.commit()
    result = patient_note_add(log.id, "Hello")
    assert result is not None
    assert result.patient_note == "Hello"

def test_patient_note_add_invalid_log(session):
    with pytest.raises(ValueError):
        patient_note_add(1, "123")

def test_update_profile(session):
    profile = User(
        username="Bob",
        email="test@gmail.com",
        password="123",
        gender="Male",
        dob=dt.date.today(),
        role_level=0
    )
    db.session.add(profile)
    db.session.commit()
    update_profile(
        profile.id,
        name="Tom",
        gender="Female",
        dob=dt.date.today() - dt.timedelta(days=1),
        contact="123456789"
    )
    assert profile.username == "Tom"
    assert profile.gender == "Female"
    assert profile.dob == dt.date.today() - dt.timedelta(days=1)
    assert profile.contact == "123456789"

def test_update_profile_invalid_user(session):
    with pytest.raises(ValueError):
        update_profile(1, "Tom", "Female", dt.date.today(), "123")

def test_patient_profile_create(session):
    profile = patient_profile_create("ab", "bc", "cd", "de", 1, "Low")

    assert profile is not None
    assert profile.cultural == "ab"
    assert profile.dietary == "bc"
    assert profile.allergens == "cd"
    assert profile.medical_history == "de"
    assert profile.user_id == 1
    assert profile.risk_level == "Low"

def test_patient_profile_edit(session):
    profile = patient_profile_create("ab", "bc", "cd", "de", 1, "Low")
    edit = patient_profile_edit(profile.id, "cultural", "dietary", "allergens", "medical_history")
    assert edit is not None
    assert profile.cultural == "cultural"
    assert profile.dietary == "dietary"
    assert profile.allergens == "allergens"
    assert profile.medical_history == "medical_history"

def test_patient_profile_edit_invalid_profile(session):
    with pytest.raises(ValueError):
        patient_profile_edit(1, "a", "b", "c", "d")