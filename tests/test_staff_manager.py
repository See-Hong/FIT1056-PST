import pytest
from flask import Flask
import datetime as dt
from app.models import db, User, Role, PatientProfile, PatientLog, Appointment
from app.staff_manager import search_patients, log_edit, patient_log_create

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

def test_search_patient(session):
    # Age 10
    patient1 = User(username="Alice", email="alice@test.com", gender="Female", role_level=Role.PATIENT, password="123",
                 dob=dt.date.today() - dt.timedelta(days= 365 * 10))
    # Age 20
    patient2 = User(username="Bob", email="bob@test.com", gender="Male", role_level=Role.PATIENT, password="123",
                 dob=dt.date.today() - dt.timedelta(days= 365 * 20))
    session.add_all([patient1, patient2])
    session.commit()

    patient1_profile = PatientProfile(user_id=patient1.id, risk_level="Low")
    session.add(patient1_profile)
    session.commit()

    result = search_patients(search="Bob")

    assert len(result) == 1
    assert result[0].username == "Bob"

    result = search_patients(gender="Female")

    assert len(result) == 1
    assert result[0].gender == "Female"

    result = search_patients(min_age=11)
    assert len(result) == 1
    assert result[0].dob <= dt.date.today() - dt.timedelta(days=365 * 11)

    result = search_patients(max_age=19)
    assert len(result) == 1
    assert result[0].dob >= dt.date.today() - dt.timedelta(days=365 * 19)

    result = search_patients(risk="Low")
    assert len(result) == 1
    assert result[0].patient_profile.risk_level == "Low"

def test_search_patient_no_result(session):
    result = search_patients(search="Bob")

    assert len(result) == 0

def test_log_edit(session):
    log = PatientLog(date=dt.date.today(), time=dt.datetime.now().time(), created_by=1, profile_id=1)
    session.add(log)
    session.commit()
    result = log_edit(log.id, medical="ab", emotional="bc", note="cd")

    assert result is not None
    assert log.emotional == "bc"
    assert log.medical == "ab"
    assert log.note == "cd"

def test_log_edit_invalid_log(session):
    with pytest.raises(ValueError):
        log_edit(1, "a", "b", "c")

def test_patient_log_create(session):
    log = patient_log_create(
        date=dt.date.today(),
        time=dt.datetime.now().time(),
        medical="medical",
        emotional="emotional",
        note="note",
        created_by=1,
        profile_id=1
    )
    assert log is not None
    assert log.medical == "medical"
    assert log.emotional == "emotional"
    assert log.note == "note"

