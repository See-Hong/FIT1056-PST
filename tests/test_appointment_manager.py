import pytest
from flask import Flask
import datetime as dt
from app.models import db, Appointment
from app.appointment_manager import create_new_appointment, appointment_accept, appointment_cancel, appointment_complete


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

def test_create_new_appointment(session):
    appointment = create_new_appointment(
        date=dt.date.today(),
        time=dt.datetime.now().time(),
        reason="abc",
        created_by=1,
        status="Pending",
        patient_id=1
    )
    assert appointment is not None
    assert appointment.date == dt.date.today()
    assert appointment.time.replace(second=0, microsecond=0) == dt.datetime.now().time().replace(second=0, microsecond=0)
    assert appointment.reason == "abc"
    assert appointment.created_by == 1
    assert appointment.status == "Pending"
    assert appointment.patient_id == 1

def test_appointment_accept(session):
    appointment = Appointment(
        date=dt.date.today(),
        time=dt.datetime.now().time(),
        created_by=1,
        reason="a",
        status="Pending",
    )
    session.add(appointment)
    session.commit()
    appointment_accept(appointment.id, 1)

    assert appointment.status == "Scheduled"

def test_appointment_accept_invalid_log(session):
    with pytest.raises(ValueError):
        appointment_accept(1, 1)

def test_appointment_complete(session):
    appointment = Appointment(
        date=dt.date.today(),
        time=dt.datetime.now().time(),
        created_by=1,
        reason="a",
        status="Pending",
    )
    session.add(appointment)
    session.commit()

    appointment_complete(appointment.id)

    assert appointment.status == "Completed"

def test_appointment_complete_invalid_log(session):
    with pytest.raises(ValueError):
        appointment_complete(1)

def test_appointment_cancel(session):
    appointment = Appointment(
        date=dt.date.today(),
        time=dt.datetime.now().time(),
        created_by=1,
        reason="a",
        status="Pending",
    )
    session.add(appointment)
    session.commit()
    appointment_cancel(appointment.id)

    assert appointment.status == "Cancelled"

def test_appointment_cancel_invalid_log(session):
    with pytest.raises(ValueError):
        appointment_cancel(1)