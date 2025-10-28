import pytest
from flask import Flask
import datetime as dt
from app.models import db, User, Role
from app.admin_manager import search_accounts, change_user_role

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

def test_search_accounts(session):
    user1 = User(username="Alice", email="alice@test.com", gender="Female", role_level=Role.PATIENT, password="123", dob=dt.date.today())
    user2 = User(username="Bob", email="bob@test.com", gender="Male", role_level=Role.NURSE, password="123", dob=dt.date.today())
    session.add_all([user1, user2])
    session.commit()

    results = search_accounts(search="Alice")
    assert len(results) == 1
    assert results[0].username == "Alice"

    results = search_accounts(gender="Male")
    assert len(results) == 1
    assert results[0].gender == "Male"

    results = search_accounts(role=Role.PATIENT)
    assert len(results) == 1
    assert results[0].role_level == Role.PATIENT

def test_search_accounts_no_match(session):
    user1 = User(username="Alice", email="alice@test.com", gender="Female", role_level=Role.PATIENT, password="123", dob=dt.date.today())
    user2 = User(username="Bob", email="bob@test.com", gender="Male", role_level=Role.NURSE, password="123", dob=dt.date.today())
    session.add_all([user1, user2])
    session.commit()

    results = search_accounts(search="Tom")
    assert len(results) == 0

def test_change_user_role(session):
    user = User(username="John", email="john@test.com", gender="Male", role_level=Role.NURSE, password="123", dob=dt.date.today())
    session.add(user)
    session.commit()

    updated = change_user_role(user.id, Role.PATIENT)
    assert updated.role_level == Role.PATIENT

def test_change_user_role_invalid_user(session):
    with pytest.raises(ValueError):
        change_user_role(121, Role.PATIENT)

def test_change_user_role_invalid_role(session):
    user = User(username="John", email="john@test.com", gender="Male", role_level=Role.NURSE, password="123", dob=dt.date.today())
    session.add(user)
    session.commit()
    with pytest.raises(ValueError):
        change_user_role(user.id, 123)
