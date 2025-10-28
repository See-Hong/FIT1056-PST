from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, User, Role

def find_user_by_email(email):
    """Find a user from db using email"""
    return db.session.execute(db.select(User).where(User.email == email.strip().lower())).scalar()

def register_user(name, email, gender, dob, tel, password):
    """Registers a new user. Returns the created user object."""
    if find_user_by_email(email):
        raise ValueError("Email already registered")

    # Hash given password
    hashed_pw = generate_password_hash(password, salt_length=8)
    new_user = User(
        username=name,
        email=email,
        gender=gender,
        dob=dob,
        contact=tel,
        password=hashed_pw,
        role_level=Role.PATIENT,
    )
    db.session.add(new_user)
    db.session.commit()
    return new_user

def verify_user(email, password):
    """Checks if a user exists and password is valid."""
    user = find_user_by_email(email)
    if not user:
        return None
    if not check_password_hash(user.password, password):
        return None
    return user

def change_user_password(user_id, old_pass, new_pass):
    """Changes a users password"""
    user = db.session.get(User, user_id)
    if not user:
        raise ValueError("User not found")
    # Check if given password is correct
    if verify_user(user.email, old_pass):
        user.password = generate_password_hash(new_pass, salt_length=8)
        db.session.commit()
        return True
    else:
        return False