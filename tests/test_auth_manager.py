import pytest
from flask import Flask
import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, User, Role
from app.auth_manager import verify_user, register_user, find_user_by_email, change_user_password


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

@pytest.fixture
def sample_user(app, session):
    """Create and return a sample user in the test database."""
    with app.app_context():
        user = User(
            username="Test User",
            email="test@example.com",
            gender="Male",
            dob=dt.date(year=2000, month=1, day=1),
            contact="0123456789",
            password=generate_password_hash("password123", salt_length=8),
            role_level=Role.PATIENT
        )
        db.session.add(user)
        db.session.commit()
        return user

def test_find_user_by_email(sample_user):
    user = find_user_by_email("test@example.com")
    assert user is not None
    assert user.email == "test@example.com"

def test_find_user_by_email_no_email(sample_user):
    user = find_user_by_email("123@gmail.com")
    assert user is None

def test_register_user(sample_user):
    user = register_user(name="Bob",
                         email="123@gmail.com",
                         gender="Male",
                         dob=dt.date.today(),
                         tel="0123456789",
                         password=generate_password_hash("password12345", salt_length=8)
                         )
    assert user is not None
    assert user.username == "Bob"
    assert user.email == "123@gmail.com"
    assert user.gender == "Male"
    assert user.dob == dt.date.today()
    assert user.contact == "0123456789"

def test_register_user_same_email(sample_user):
    with pytest.raises(ValueError):
        register_user(name="Test User",
            email="test@example.com",
            gender="Male",
            dob=dt.date(year=2000, month=1, day=1),
            tel="0123456789",
            password=generate_password_hash("password123", salt_length=8)
                             )

def test_verify_user(sample_user):
    user = verify_user("test@example.com", "password123")
    assert user is not None
    assert user.email == "test@example.com"

def test_verify_user_wrong_email(sample_user):
    user = verify_user("123@gmail.com", "123")
    assert user is None

def test_verify_user_wrong_pass(sample_user):
    user = verify_user("test@example.com", "12312312")
    assert user is None

def test_change_user_password(session):
    user = User(
        username="Bob",
        email="test@gmail.com",
        password=generate_password_hash("123", salt_length=8),
        gender="Male",
        dob=dt.date.today(),
        role_level=0
    )
    db.session.add(user)
    db.session.commit()
    result = change_user_password(user.id, "123", "abcde")
    assert result == True
    assert check_password_hash(user.password, "abcde") == True

def test_change_user_password_invalid_user(session):
    with pytest.raises(ValueError):
        change_user_password(1, "123", "abc")

def test_change_user_password_wrong_password(session):
    user = User(
        username="Bob",
        email="test@gmail.com",
        password=generate_password_hash("123", salt_length=8),
        gender="Male",
        dob=dt.date.today(),
        role_level=0
    )
    db.session.add(user)
    db.session.commit()
    result = change_user_password(user.id, "1", "abcde")
    assert result == False
    assert check_password_hash(user.password, "123") == True


