from faker import Faker
import random
import datetime as dt
from app.models import db, User, PatientProfile, Appointment, PatientLog, Role

fake = Faker()

def seed_users(n=10):
    users = []
    for _ in range(n):
        gender = random.choice(["Male", "Female"])
        user = User(
            username=fake.user_name(),
            email=fake.unique.email(),
            password="hashed_password",
            gender=gender,
            dob=fake.date_of_birth(minimum_age=18, maximum_age=80),
            contact=fake.phone_number(),
            role_level=0
        )
        db.session.add(user)
        users.append(user)
    db.session.commit()

    # Add PatientProfiles
    for user in users:
        profile = PatientProfile(
            user_id=user.id,
            risk_level=random.choice(["Low", "Moderate", "High"]),
            cultural=fake.sentence(),
            dietary=fake.sentence(),
            allergens=fake.word(),
            medical_history=fake.text(100)
        )
        db.session.add(profile)
    db.session.commit()

    print(f"✅ Seeded {len(users)} users with profiles.")
    return users

def seed_receptionist(n=5):
    receptionists = []
    for _ in range(n):
        gender = random.choice(["Male", "Female"])
        receptionist = User(
            username=f"dr_{fake.user_name()}",
            email=fake.unique.email(),
            password="hashed_password",
            gender=gender,
            dob=fake.date_of_birth(minimum_age=28, maximum_age=70),
            contact=fake.phone_number(),
            role_level=1
        )
        db.session.add(receptionist)
        receptionists.append(receptionist)

    db.session.commit()
    print(f"✅ Seeded {len(receptionists)} doctors.")
    return receptionists

def seed_nurses(n=5):
    nurses = []
    for _ in range(n):
        gender = random.choice(["Male", "Female"])
        nurse = User(
            username=f"dr_{fake.user_name()}",
            email=fake.unique.email(),
            password="hashed_password",
            gender=gender,
            dob=fake.date_of_birth(minimum_age=28, maximum_age=70),
            contact=fake.phone_number(),
            role_level=2
        )
        db.session.add(nurse)
        nurses.append(nurse)

    db.session.commit()
    print(f"✅ Seeded {len(nurses)} doctors.")
    return nurses

def seed_doctors(n=5):
    doctors = []
    for _ in range(n):
        gender = random.choice(["Male", "Female"])
        doctor = User(
            username=f"dr_{fake.user_name()}",
            email=fake.unique.email(),
            password="hashed_password",  # Replace with real hash later
            gender=gender,
            dob=fake.date_of_birth(minimum_age=28, maximum_age=70),
            contact=fake.phone_number(),
            role_level=3  # ✅ DOCTOR role
        )
        db.session.add(doctor)
        doctors.append(doctor)

    db.session.commit()
    print(f"✅ Seeded {len(doctors)} doctors.")
    return doctors

def seed_appointments(users, n=15):
    patients = [u for u in users if u.role_level == 0]
    doctors = [u for u in users if u.role_level != 0] or patients  # fallback if no doctors

    for _ in range(n):
        doctor = random.choice(doctors)
        patient = random.choice(patients)
        date = fake.date_between(start_date="+3d", end_date="+30d")
        time = dt.time(hour=random.randint(9, 17), minute=random.choice([0, 30]))

        appointment = Appointment(
            date=date,
            time=time,
            created_by=doctor.id,
            reason=fake.sentence(),
            status=random.choice(["Pending", "Confirmed", "Completed", "Cancelled"]),
            doctor_id=doctor.id,
            patient_id=patient.id
        )
        db.session.add(appointment)

    db.session.commit()
    print(f"✅ Seeded {n} appointments.")


def seed_patient_logs(profiles, count_per_profile=3):
    # Get doctors and nurses
    staff_users = User.query.filter(User.role_level.in_([2, 3])).all()

    if not staff_users:
        print("⚠ No doctors/nurses found — patient logs cannot be seeded.")
        return

    logs_created = 0

    for profile in profiles:
        for _ in range(count_per_profile):
            staff = random.choice(staff_users)

            log = PatientLog(
                date=fake.date_between(start_date="-6m", end_date="today"),
                time=fake.time_object(),
                created_by=staff.id,  # ✅ doctor or nurse id
                medical=fake.sentence(nb_words=8),
                emotional=random.choice([
                    "Stable",
                    "Anxious",
                    "Stressed",
                    "Calm",
                    "Improving"
                ]),
                note=fake.paragraph(nb_sentences=2),
                patient_note=random.choice([
                    fake.sentence(),
                    None  # Some logs may not have patient feedback
                ]),
                profile_id=profile.id
            )

            db.session.add(log)
            logs_created += 1

    db.session.commit()
    print(f"✅ Seeded {logs_created} patient logs!")

def seed_all():
    doctors = seed_doctors(5)
    nurses = seed_nurses(5)
    receptionists = seed_receptionist(5)
    users = seed_users(10)
    profiles = PatientProfile.query.all()
    seed_appointments(users, 15)
    seed_patient_logs(profiles, 20)

